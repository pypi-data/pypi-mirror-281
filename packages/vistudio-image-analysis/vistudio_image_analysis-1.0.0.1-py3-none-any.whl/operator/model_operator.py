#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   infer.py
"""
import os

from windmillartifactv1.client.artifact_api_artifact import parse_artifact
from windmillmodelv1.client.model_client import ModelClient
import bcelogger
from windmillmodelv1.client.model_api_model import parse_model_name

from vistudio_image_analysis.util import string
from windmillendpointv1.client.endpoint_client import EndpointClient


class ModelOperator(object):
    """
    ImageNetFormatter
    """

    def __init__(self,
                 windmill_ak: str,
                 windmill_sk: str,
                 windmill_endpoint: str,
                 ):
        self.endpointClient = EndpointClient(
            ak=windmill_ak,
            sk=windmill_sk,
            endpoint=windmill_endpoint
        )
        self.modelClient = ModelClient(
            ak=windmill_ak,
            sk=windmill_sk,
            endpoint=windmill_endpoint
        )

    def get_model(self, workspace_id: str, model_store_name: str, model_local_name: str):
        """
        get model
        """
        response = self.modelClient.get_model(workspace_id=workspace_id,
                                              model_store_name=model_store_name,
                                              local_name=model_local_name)

        return response
