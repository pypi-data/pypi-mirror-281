#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   infer.py
"""
import os
from typing import Dict, Any

from ray.data import Dataset
from windmillartifactv1.client.artifact_api_artifact import parse_artifact
from windmillendpointv1.client.endpoint_monitor_client import EndpointMonitorClient
import bcelogger
from windmillmodelv1.client.model_api_model import parse_model_name

from vistudio_image_analysis.operator.model_operator import ModelOperator
from vistudio_image_analysis.util import string
from windmillendpointv1.client.endpoint_client import EndpointClient
from tritonclient.utils import triton_to_np_dtype
import numpy as np
from tritonv2.client_factory import TritonClientFactory
from tritonv2.constants import LimiterConfig, RequestRateDuration
from tritonv2.utils import list_stack_ndarray
import os
import cv2
import json
import tritonclient.http as http_client
import time

model_name = "ensemble"


class Infer(object):
    """
    ImageNetFormatter
    """

    def __init__(self,
                 windmill_ak: str,
                 windmill_sk: str,
                 windmill_endpoint: str,
                 ):
        self.windmill_ak = windmill_ak
        self.windmill_sk = windmill_sk
        self.windmill_endpoint = windmill_endpoint
        self.endpointClient = EndpointClient(
            ak=windmill_ak,
            sk=windmill_sk,
            endpoint=windmill_endpoint
        )
        self.endpointMonitorClient = EndpointMonitorClient(
            ak=windmill_ak,
            sk=windmill_sk,
            endpoint=windmill_endpoint
        )

    @staticmethod
    def triton_inference_picture(image, file_name, server_uri) -> Dict[str, Any]:
        """
        inference picture
        Args:
            image:
            file_name:
            args:
        Returns:

        """
        client = TritonClientFactory.create_http_client(
            server_url=server_uri,
            limiter_config=LimiterConfig(limit=1, interval=RequestRateDuration.SECOND, delay=True),
        )
        input_metadata, output_metadata, batch_size = client.get_inputs_and_outputs_detail(
            model_name=model_name)
        # 处理数据
        # 1. 读取图片
        repeated_image_data = []
        img_encode = cv2.imencode('.jpg', image)[1]
        img = np.frombuffer(img_encode.tobytes(), dtype=triton_to_np_dtype(input_metadata[0]['datatype']))
        repeated_image_data.append(np.array(img))
        batched_image_data = list_stack_ndarray(repeated_image_data)
        # 2. 添加meta信息
        meta_json = json.dumps({"image_id": str(file_name), "camera_id": "camera_id_string"})
        byte_meta_json = meta_json.encode()
        np_meta_json = np.frombuffer(byte_meta_json, dtype='uint8')
        send_meta_json = np.array(np_meta_json)
        send_meta_json = np.expand_dims(send_meta_json, axis=0)

        # build triton input
        inputs = [
            http_client.InferInput(input_metadata[0]["name"], list(
                batched_image_data.shape), input_metadata[0]["datatype"]),
            http_client.InferInput(input_metadata[1]["name"], send_meta_json.shape,
                                   input_metadata[1]["datatype"])
        ]
        inputs[0].set_data_from_numpy(batched_image_data, binary_data=False)
        inputs[1].set_data_from_numpy(send_meta_json)

        # build triton output
        output_names = [
            output["name"] for output in output_metadata
        ]
        outputs = []
        for output_name in output_names:
            outputs.append(
                http_client.InferRequestedOutput(output_name,
                                                 binary_data=True))

        # infer
        result = client.model_infer(model_name, inputs, outputs=outputs)
        # print detailed output
        output_dict = {}
        for output_name in output_names:
            output_dict[output_name] = eval(result.as_numpy(output_name))
        print(output_dict)

        # get model statistics
        model_statistics = client.model_statistics(model_name)
        print(model_statistics)
        return output_dict

    def check_status(self, workspace_id: str, endpoint_hub_name: str, endpoint_name: str, deployment: str) -> bool:
        endpoint_info = self.endpointClient.get_endpoint(workspace_id=workspace_id,
                                                         endpoint_hub_name=endpoint_hub_name,
                                                         endpoint_name=endpoint_name)

        monitor_info = self.endpointMonitorClient.get_endpoint_status(
            workspace_id=workspace_id,
            endpoint_hub_name=endpoint_hub_name,
            local_name=endpoint_name)

        if monitor_info.deploymentStatus == "Init" or monitor_info.deploymentStatus == "Progressing":
            bcelogger.info("endpoint 部署中....")
            return None

        if monitor_info.deploymentStatus == "Failed":
            bcelogger.info("endpoint 部署失败")
            return False

        if monitor_info.deploymentStatus == "NotFound" or monitor_info.deploymentStatus == "NeverDeploy":
            bcelogger.info("服务未上线，请先部署服务")
            return False

        if monitor_info.deploymentStatus == "Completed" and monitor_info.status == "NotAvailable":
            bcelogger.info("服务异常，请及时排查问题")
            return False

        if monitor_info.deploymentStatus == "Completed" and monitor_info.status == "Available":
            try:
                artifact_name = parse_artifact(endpoint_info.lastJob["modelName"])
                model_op = ModelOperator(windmill_ak=self.windmill_ak,
                                         windmill_sk=self.windmill_sk,
                                         windmill_endpoint=self.windmill_endpoint)
                model_name = parse_model_name(artifact_name.naming.object_name)
                model_category = model_op.get_model(
                    workspace_id=model_name.workspace_id,
                    model_store_name=model_name.model_store_name,
                    model_local_name=model_name.local_name
                ).category["category"]
                parts = model_category.lstrip('/').split('/')

            except Exception as e:
                return False

            if parts[0] != 'Image':
                bcelogger.error("仅图像类模型支持服务调试功能")
                return False
            else:

                resp = self.endpointClient.get_deployment(
                    workspace_id=workspace_id,
                    endpoint_hub_name=endpoint_hub_name,
                    local_name=deployment)
                server_kind = resp.serverKind
                if server_kind != 'Triton':
                    bcelogger.info("不支持的推理引擎")
                    return False

            return True
        else:
            return False

    def _convert_skill_output(self, row: Dict[str, Any], artifact_name: str, annotation_set_id: str) -> Dict[str, Any]:
        image_name = row['image_id']
        predictions = row['predictions']
        annotations = list()
        res_row = dict()
        res_row['image_id'] = string.generate_md5(image_name)
        res_row['artifact_name'] = artifact_name
        res_row['task_kind'] = 'Model'
        res_row['data_type'] = 'Annotation'
        res_row['user_id'] = ''
        res_row['annotation_set_id'] = annotation_set_id
        for element in predictions:
            bbox = element['bbox']
            area = element['area']
            id = string.generate_md5(str(time.time_ns()))
            labels = element['categories']
            annotation_element = {
                "id": id,
                "bbox": bbox,
                "area": area,
                "labels": labels
            }
            annotations.append(annotation_element)
        res_row['annotations'] = annotations
        return res_row

    def to_vistudio_v1(self, ds: Dataset, artifact_name: str, annotation_set_id: str) -> Dict[str, Dataset]:
        annotation_ds = ds.map(lambda row: self._convert_skill_output(row=row,
                                                                      artifact_name=artifact_name,
                                                                      annotation_set_id=annotation_set_id))
        return {"annotation_ds": annotation_ds}
