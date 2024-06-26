#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   base_pipeline.py
"""

import re
import bcelogger
import json

from windmillendpointv1.client.endpoint_monitor_client import EndpointMonitorClient
from windmilltrainingv1.client.training_api_job import parse_job_name
from windmilltrainingv1.client.training_client import TrainingClient
from windmillendpointv1.client.endpoint_client import EndpointClient

from vistudio_image_analysis.client.annotation_client import AnnotationClient

from vistudio_image_analysis.config.config import Config
from vistudio_image_analysis.datasource.sharded_mongo_datasource import parse_mongo_uri, get_mongo_collection
from vistudio_image_analysis.util import string

annotationset_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/annotationsets/" \
                             r"(?P<annotationset_local_name>[^/]+)$"


class BaseInferPipeline(object):
    """
    BaseImportPipline
    """

    def __init__(self, args: dict()):
        bcelogger.info("BaseInferPipline Init Start!")
        self.args = args
        self.annotation_set_name = args.get('annotation_set_name')
        self.endpoint_name = args.get("endpoint_name")
        self.deployment = args.get("deployment")
        self.config = Config(args)
        self.mongo_uri = self._get_mongo_uri()
        self._get_labels()
        self.mongodb = get_mongo_collection(config=self.config)
        self.annotation_client = AnnotationClient(endpoint=self.config.vistudio_endpoint,
                                                  ak=self.config.windmill_ak,
                                                  sk=self.config.windmill_sk)
        self.endpointClient = EndpointClient(
            ak=self.config.windmill_ak,
            sk=self.config.windmill_sk,
            endpoint=self.config.windmill_endpoint
        )
        self.endpointMonitorClient = EndpointMonitorClient(
            ak=self.config.windmill_ak,
            sk=self.config.windmill_sk,
            endpoint=self.config.windmill_endpoint
        )

        bcelogger.info("BaseInferPipline Init End!")

    def _get_mongo_uri(self):
        """
        get mongo uri
        :return:
        """
        uri = "mongodb://{}:{}@{}:{}".format(self.args.get('mongo_user'),
                                             self.args.get('mongo_password'),
                                             self.args.get('mongo_host'),
                                             self.args.get('mongo_port'))
        return uri

    def _get_labels(self):
        """
        get annotation labels
        :return:
        """

        try:
            annotation_client = AnnotationClient(endpoint=self.config.vistudio_endpoint,
                                                 ak=self.config.windmill_ak,
                                                 sk=self.config.windmill_sk)
            match = re.match(annotationset_name_pattern, self.annotation_set_name)
            annotationset_name_dict = match.groupdict()
            annotationset_workspace_id = annotationset_name_dict.get("workspace_id")
            annotationset_project_name = annotationset_name_dict.get("project_name")
            annotationset_local_name = annotationset_name_dict.get("annotationset_local_name")
            anno_res = annotation_client.get_annotation_set(workspace_id=annotationset_workspace_id,
                                                            project_name=annotationset_project_name,
                                                            local_name=annotationset_local_name)
            bcelogger.info("get_annotation_set anno_res={}".format(anno_res))
        except Exception as e:
            bcelogger.error("get annotation info exception.annotation_name:{}"
                            .format(self.annotation_set_name), e)
            raise Exception("Get annotation set info exception.annotation_set_name:{}".format(self.annotation_set_name))

        self.annotation_set_id = anno_res.id
        annotation_labels = anno_res.labels

        labels = {}
        if annotation_labels is not None:
            for label_elem in annotation_labels:
                label_local_name = label_elem.get('localName', None)
                label_display_name = label_elem.get('displayName', None)
                labels[label_local_name] = label_display_name

        sorted_labels = {k: v for k, v in sorted(labels.items(), key=lambda x: int(x[0]))}
        self.labels = sorted_labels
        return sorted_labels

    def get_endpoint_info(self, workspace_id: str, endpoint_hub_name: str, endpoint_name: str):
        """
        get_endpoint_info
        """
        try:
            endpoint_info = self.endpointClient.get_endpoint(workspace_id=workspace_id,
                                                             endpoint_hub_name=endpoint_hub_name,
                                                             endpoint_name=endpoint_name)
            bcelogger.info("get_endpoint_info "
                           "endpoint_info:{} "
                           "workspace_id:{} "
                           "endpoint_hub_name:{} "
                           "endpoint_name:{}".format(endpoint_info, workspace_id, endpoint_hub_name, endpoint_name))
            return endpoint_info
        except Exception as e:
            bcelogger.error("get_endpoint_info error"
                            "endpoint_info:{} "
                            "workspace_id:{} "
                            "endpoint_hub_name:{} "
                            "endpoint_name:{}".format(endpoint_info, workspace_id, endpoint_hub_name, endpoint_name), e)
            return None

    def update_annotation_job(self, err_msg):
        """
                更新标注任务状态
                """
        job_name = self.config.job_name
        bcelogger.info("update job name is {}".format(job_name))
        client_job_name = parse_job_name(self.config.job_name)
        update_job_resp = self.train_client.update_job(
            workspace_id=client_job_name.workspace_id,
            project_name=client_job_name.project_name,
            local_name=client_job_name.local_name,
            tags={"errMsg": err_msg},
        )
        bcelogger.info("update job resp is {}".format(update_job_resp))

    def create_deploy_endpoint_job(self, workspace_id: str, endpoint_hub_name: str, endpoint_name: str,
                                   artifact_name: str, spec_name: str, kind: str):
        """
        create_deploy_endpoint_job
        """
        self.endpointClient.create_deploy_endpoint_job(workspace_id=workspace_id,
                                                       endpoint_hub_name=endpoint_hub_name,
                                                       endpoint_name=endpoint_name,
                                                       artifact_name=artifact_name,
                                                       spec_name=spec_name,
                                                       kind=kind)

