#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   export_pipeline.py
"""

import sys
import os
import time

import bcelogger
import ray.data
from ray.data.read_api import read_datasource

__work_dir__ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from windmillartifactv1.client.artifact_api_artifact import parse_artifact
from windmillendpointv1.client.endpoint_api import parse_endpoint_name

from vistudio_image_analysis.datasource.image_datasource import CityscapesImageDatasource
from vistudio_image_analysis.operator.infer import Infer
from vistudio_image_analysis.pipeline.base_infer_pipeline import BaseInferPipeline

sys.path.insert(0, __work_dir__)
from windmillartifactv1.client.artifact_client import ArtifactClient
from windmillcomputev1.filesystem import init_py_filesystem
from windmilltrainingv1.client.training_api_dataset import DatasetName

from vistudio_image_analysis.datasink.filename_provider import MultiFilenameProvider
from vistudio_image_analysis.config.arg_parser import ArgParser
from vistudio_image_analysis.processor.exporter.coco.coco_preprocessor import CocoFormatPreprocessor, \
    CocoMergePreprocessor
from vistudio_image_analysis.processor.cutter.cut_preprocessor import VistudioCutterPreprocessor
from .base_export_pipeline import BaseExportPipeline


class BatchInferPipeline(BaseInferPipeline):
    """
    exporter coco pipeline
    """

    def __init__(self, args):
        super().__init__(args)
        self._py_fs = init_py_filesystem(self.config.filesystem)
        self.artifact_client = ArtifactClient(
            endpoint=self.config.windmill_endpoint,
            ak=self.config.windmill_ak,
            sk=self.config.windmill_sk
        )

    def run(self, parallelism: int = 10):
        """
        pipeline_coco
        :return:
        """
        endpoint_local_name = None,
        artifact_name = None,
        endpoint_workspace_id = None

        try:
            # step 1: datasource
            ds = read_datasource(self.datasource, parallelism=parallelism)
            file_uris = ds.unique(column="file_uri")
            bcelogger.info("read data from mongo.dataset count = {}".format(ds.count()))
            if ds.count() <= 0:
                return

            endpointName = parse_endpoint_name(name=self.endpoint_name)
            endpoint_workspace_id = endpointName.workspace_id
            endpoint_hub_name = endpointName.endpoint_hub_name
            endpoint_local_name = endpointName.local_name
            endpoint_info = self.get_endpoint_info(workspace_id=endpoint_workspace_id,
                                                   endpoint_hub_name=endpoint_hub_name,
                                                   endpoint_name=endpoint_local_name)
            if endpoint_info is None:
                self.update_annotation_job("未正常获取到推理服务信息，请检查服务")
                return
            artifact_name = parse_artifact(endpoint_info.lastJob["modelName"])

            infer_operator = Infer(windmill_ak=self.config.windmill_ak,
                                   windmill_sk=self.config.windmill_sk,
                                   windmill_endpoint=self.config.windmill_endpoint)
            start_time = time.time()
            deploy_suc = None
            while time.time() - start_time < 120:
                deploy_suc = infer_operator.check_status(workspace_id=endpoint_workspace_id,
                                                         endpoint_hub_name=endpoint_hub_name,
                                                         endpoint_name=endpoint_local_name,
                                                         deployment=self.deployment)
                if deploy_suc is None:
                    continue
                elif deploy_suc:
                    break
                else:
                    self.update_annotation_job("推理服务未正常启动，请检查服务")
                    return

            if deploy_suc is None or not deploy_suc:
                self.update_annotation_job("推理服务未正常启动，请检查服务")
                bcelogger.info("模型部署失败 endpoint_name:{}".format(self.endpoint_name))
                return

            # 删除该模型下面的 模型标注数据
            delete_query = {
                "artifact_name": artifact_name,
                "task_kind": "Model",
                "annotation_set_id": self.annotation_set_id
            }
            self.mongodb.delete_many(delete_query)

            # 进行推理

            server_uri = os.path.join(endpoint_info.uri.replace("http://", ""), "http")
            batch_infer = Infer(windmill_ak=self.config.windmill_ak,
                                windmill_sk=self.config.windmill_sk,
                                windmill_endpoint=self.config.windmill_endpoint)
            cityscapes_datasource = CityscapesImageDatasource(paths=file_uris, filesystem=self._py_fs)
            infer_annotation_ds = ray.data.read_datasource(datasource=cityscapes_datasource) \
                .map(lambda row: batch_infer.triton_inference_picture(image=row['image'],
                                                                      file_name=row['image_name'],
                                                                      server_uri=server_uri),
                     concurrency=32)
            annotaction_dict = batch_infer.to_vistudio_v1(ds=infer_annotation_ds
                                                          , artifact_name=artifact_name,
                                                          annotation_set_id=self.annotation_set_id)
            annotation_ds = annotaction_dict.get("annotation_ds")
            bcelogger.info("write mongo. annotation ds count:{}".format(annotation_ds.count))
            # 数据入库

            annotation_ds.write_mongo(uri=self.mongo_uri,
                                      database=self.config.mongodb_database,
                                      collection=self.config.mongodb_collection)
        except Exception as e:
            bcelogger.error("BatchInferPipeline run error", e)
        finally:
            self.create_deploy_endpoint_job(workspace_id=endpoint_workspace_id,
                                            endpoint_hub_name=endpoint_hub_name,
                                            endpoint_name=endpoint_local_name,
                                            artifact_name=artifact_name,
                                            spec_name=self.deployment,
                                            kind="Undeploy"
                                            )






def run(args):
    """
    main
    :param args:
    :return:
    """

    pipeline = BatchInferPipeline(args)
    pipeline.run()


if __name__ == "__main__":
    arg_parser = ArgParser(kind='Infer')
    args = arg_parser.parse_args()
    run(args)
