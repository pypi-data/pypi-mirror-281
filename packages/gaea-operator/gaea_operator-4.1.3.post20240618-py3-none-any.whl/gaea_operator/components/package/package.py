#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/23
# @Author  : yanxiaodong
# @File    : transform_component.py
"""
import copy
import json
import os
from argparse import ArgumentParser

from gaea_tracker import ExperimentTracker
from bcelogger.base_logger import setup_logger
import bcelogger
from windmillmodelv1.client.model_api_model import parse_model_name
from windmillmodelv1.client.model_api_modelstore import parse_modelstore_name
from windmillartifactv1.client.artifact_api_artifact import get_name, parse_artifact_name
from windmillclient.client.windmill_client import WindmillClient

from gaea_operator.config import Config
from gaea_operator.model import format_name
from gaea_operator.utils import read_file, \
    write_file, \
    get_accelerator, \
    ModelTemplate


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--windmill-ak", type=str, default=os.environ.get("WINDMILL_AK"))
    parser.add_argument("--windmill-sk", type=str, default=os.environ.get("WINDMILL_SK"))
    parser.add_argument("--windmill-endpoint", type=str, default=os.environ.get("WINDMILL_ENDPOINT"))
    parser.add_argument("--project-name", type=str, default=os.environ.get("PROJECT_NAME"))
    parser.add_argument("--scene", type=str, default=os.environ.get("SCENE"))
    parser.add_argument("--public-model-store",
                        type=str,
                        default=os.environ.get("PUBLIC_MODEL_STORE", "workspaces/public/modelstores/public"))
    parser.add_argument("--tracking-uri", type=str, default=os.environ.get("TRACKING_URI"))
    parser.add_argument("--experiment-name", type=str, default=os.environ.get("EXPERIMENT_NAME"))
    parser.add_argument("--experiment-kind", type=str, default=os.environ.get("EXPERIMENT_KIND"))
    parser.add_argument("--ensemble-model-name",
                        type=str,
                        default=os.environ.get("ENSEMBLE_MODEL_NAME"))
    parser.add_argument("--ensemble-model-display-name",
                        type=str,
                        default=os.environ.get("ENSEMBLE_MODEL_DISPLAY_NAME"))
    parser.add_argument("--accelerator", type=str, default=os.environ.get("ACCELERATOR", "t4"))
    parser.add_argument("--algorithm", type=str, default=os.environ.get("ALGORITHM", ""))
    parser.add_argument("--sub-extra-models",
                        type=str,
                        default=os.environ.get("SUB_MODELS"))

    parser.add_argument("--input-model-uri", type=str, default=os.environ.get("INPUT_MODEL_URI"))
    parser.add_argument("--output-model-uri", type=str, default=os.environ.get("OUTPUT_MODEL_URI"))
    parser.add_argument("--output-uri", type=str, default=os.environ.get("OUTPUT_URI"))

    args, _ = parser.parse_known_args()

    return args


def create_modify_model(windmill_client: WindmillClient,
                        model_uri: str,
                        model_name: str,
                        sub_extra_models: dict,
                        workspace_id: str,
                        template_workspace_id: str,
                        model_store_name: str,
                        template_model_store_name: str,
                        need_modify_connect_name: bool,
                        transform_model_name: str,
                        transform_model_display_name: str):
    """
    create model.
    """
    model_uri = os.path.join(model_uri, model_name, str(sub_extra_models[model_name]))

    bcelogger.info(f"get model workspace id: {template_workspace_id} "
                   f"model store name: {template_model_store_name} local name: {model_name}")
    response = windmill_client.get_model(workspace_id=template_workspace_id,
                                         model_store_name=template_model_store_name,
                                         local_name=model_name)
    local_name = response.localName
    display_name = response.displayName
    if need_modify_connect_name:
        if response.category["category"] == "Image/Preprocess":
            local_name = format_name(transform_model_name, "pre")
            display_name = format_name(transform_model_display_name, "预处理")
        if response.category["category"] == "Image/Postprocess":
            local_name = format_name(transform_model_name, "post")
            display_name = format_name(transform_model_display_name, "后处理")

    bcelogger.info(f"created model {local_name}")
    response = windmill_client.create_model(workspace_id=workspace_id,
                                            model_store_name=model_store_name,
                                            local_name=local_name,
                                            display_name=display_name,
                                            category=response.category["category"],  # need modify
                                            model_formats=response.modelFormats,  # need modify
                                            artifact_tags=response.artifact["tags"],
                                            artifact_uri=model_uri)
    bcelogger.info(f"Model {local_name} created response: {response}")

    return response.localName, response.artifact["version"]


def package(args):
    """
    Package component for ppyoloe_plus model.
    """
    windmill_client = WindmillClient(ak=args.windmill_ak,
                                     sk=args.windmill_sk,
                                     endpoint=args.windmill_endpoint)
    tracker_client = ExperimentTracker(windmill_client=windmill_client,
                                       tracking_uri=args.tracking_uri,
                                       experiment_name=args.experiment_name,
                                       experiment_kind=args.experiment_kind,
                                       project_name=args.project_name)
    setup_logger(config=dict(file_name=os.path.join(args.output_uri, "worker.log")))

    response = read_file(input_dir=args.input_model_uri)
    metadata = response["artifact"]["metadata"]
    transform_model_name = response["localName"]
    transform_model_version = response["artifact"]["version"]
    transform_model_display_name = response["displayName"]
    need_modify_connect_name = False
    is_new_ensemble_model = True

    model_name = parse_model_name(name=args.ensemble_model_name)
    workspace_id = model_name.workspace_id
    model_store_name = model_name.model_store_name
    ensemble_name = model_name.local_name

    try:
        response = windmill_client.get_artifact(object_name=args.ensemble_model_name, version="latest")
        sub_extra_models = response.metadata["subModels"]
        if response.metadata["extraModels"] is not None:
            sub_extra_models.update(response.metadata["extraModels"])
        assert transform_model_name in sub_extra_models, f"{transform_model_name} not in {sub_extra_models}"
        template_workspace_id = workspace_id
        template_model_store_name = model_store_name
        template_model_name = transform_model_name
        template_ensemble_name = ensemble_name
        dump_ensemble_name = response.name
        is_new_ensemble_model = False
    except Exception:
        model_template = ModelTemplate(windmill_client=windmill_client,
                                       scene=args.scene,
                                       accelerator=args.accelerator,
                                       model_store_name=args.public_model_store,
                                       algorithm=args.algorithm)
        template_model_name = parse_model_name(model_template.suggest_template_model()).local_name
        template_ensemble_name = parse_model_name(model_template.suggest_template_ensemble()).local_name
        dump_ensemble_name = get_name(object_name=model_template.suggest_template_ensemble(), version="latest")
        template_workspace_id = parse_modelstore_name(args.public_model_store).workspace_id
        template_model_store_name = parse_modelstore_name(args.public_model_store).local_name
        if args.scene is None or args.scene == '':
            need_modify_connect_name = True

    # 1. 下载ensemble template 模型
    bcelogger.info(f"Dumping model {dump_ensemble_name} to {args.output_model_uri}")
    windmill_client.dump_models(artifact_name=dump_ensemble_name,
                                location_style="Triton",
                                output_uri=args.output_model_uri)

    # 2. 生成打包配置文件
    response = windmill_client.get_artifact(object_name=dump_ensemble_name, version="latest")
    sub_models = response.metadata["subModels"]
    ensemble_create_extra_models = {}
    ensemble_create_sub_models = {}
    if template_model_name in sub_models:
        ensemble_create_sub_models = {transform_model_name: str(transform_model_version)}
    extra_models = response.metadata["extraModels"] if response.metadata["extraModels"] is not None else {}
    if template_model_name in extra_models:
        ensemble_create_extra_models = {transform_model_name: str(transform_model_version)}
    ensemble_version = response.version
    sub_extra_models = copy.deepcopy(sub_models)
    sub_extra_models.update(extra_models)
    bcelogger.info(f"ensemble {dump_ensemble_name} sub models: {sub_models} extra models: {extra_models}")
    config = Config(windmill_client=windmill_client, tracker_client=tracker_client, metadata=metadata)
    modify_sub_models, modify_extra_models = config.write_connect_config(
        model_repo=args.output_model_uri,
        template_model_name=template_model_name,
        model_name=transform_model_name,
        model_display_name=transform_model_display_name,
        template_ensemble_name=template_ensemble_name,
        ensemble_name=ensemble_name,
        template_ensemble_version=str(ensemble_version),
        sub_models=sub_models,
        extra_models=extra_models)
    bcelogger.info(f"modify sub models: {modify_sub_models} extra models: {modify_extra_models}")

    # 3. 上传修改模型
    model_name_pairs = {template_model_name: (transform_model_name, -1)}
    if is_new_ensemble_model:
        modify_sub_models = copy.deepcopy(sub_models)
        if template_model_name in modify_sub_models:
            modify_sub_models.pop(template_model_name)
        modify_extra_models = copy.deepcopy(extra_models)
        if template_model_name in modify_sub_models:
            modify_sub_models.pop(template_model_name)
    for name in modify_sub_models:
        local_name, version = create_modify_model(windmill_client=windmill_client,
                                                  model_uri=args.output_model_uri,
                                                  model_name=name,
                                                  sub_extra_models=sub_extra_models,
                                                  workspace_id=workspace_id,
                                                  template_workspace_id=template_workspace_id,
                                                  model_store_name=model_store_name,
                                                  template_model_store_name=template_model_store_name,
                                                  need_modify_connect_name=need_modify_connect_name,
                                                  transform_model_name=transform_model_name,
                                                  transform_model_display_name=transform_model_display_name)
        ensemble_create_sub_models[local_name] = str(version)
        model_name_pairs[name] = (local_name, -1)

    for name in modify_extra_models:
        local_name, version = create_modify_model(windmill_client=windmill_client,
                                                  model_uri=args.output_model_uri,
                                                  model_name=name,
                                                  sub_extra_models=sub_extra_models,
                                                  workspace_id=workspace_id,
                                                  template_workspace_id=template_workspace_id,
                                                  model_store_name=model_store_name,
                                                  template_model_store_name=template_model_store_name,
                                                  need_modify_connect_name=need_modify_connect_name,
                                                  transform_model_name=transform_model_name,
                                                  transform_model_display_name=transform_model_display_name)
        ensemble_create_extra_models[local_name] = str(version)
        model_name_pairs[name] = (local_name, -1)

    # 4. 修改 ensemble 配置文件
    config.write_ensemble_config(model_repo=args.output_model_uri,
                                 sub_models=sub_models,
                                 extra_models=extra_models,
                                 ensemble_name=template_ensemble_name,
                                 ensemble_version=str(ensemble_version),
                                 model_name_pairs=model_name_pairs)

    # 5. 解析指定的sub models 和 extra models
    sub_extra_models = args.sub_extra_models.split(',') if args.sub_extra_models is not None else []
    bcelogger.info(f"package sub and extra models: {sub_extra_models}")
    for name in sub_extra_models:
        artifact_name = parse_artifact_name(name=name)
        model_name = parse_model_name(name=artifact_name.object_name)
        local_name = model_name.local_name
        if local_name in sub_models:
            bcelogger.info(f"model {local_name} is sub model")
            if local_name not in ensemble_create_sub_models:
                ensemble_create_sub_models[local_name] = artifact_name.version
        elif local_name in extra_models:
            bcelogger.info(f"model {local_name} is extra model")
            if local_name not in ensemble_create_extra_models:
                ensemble_create_extra_models[local_name] = artifact_name.version
        else:
            raise ValueError(f"model {local_name} is neither a sub nor an extra model")

    # 6. 上传 ensemble 模型
    ensemble_model_uri = os.path.join(args.output_model_uri, template_ensemble_name, str(ensemble_version))
    accelerator = get_accelerator(name=args.accelerator)
    config.metadata = {"subModels": ensemble_create_sub_models, "extraModels": ensemble_create_extra_models}
    prefer_model_server_parameters = accelerator.suggest_model_server_parameters()
    artifact_tags = {"model_type": "model"}
    if not is_new_ensemble_model or (args.scene is not None and len(args.scene) > 0):
        response = windmill_client.get_model(workspace_id=template_workspace_id,
                                             model_store_name=template_workspace_id,
                                             local_name=template_ensemble_name)
        prefer_model_server_parameters = response.preferModelServerParameters
        artifact_tags.update(response.artifact["tags"])
    bcelogger.info(f"prefer model server parameters: {prefer_model_server_parameters}")
    response = windmill_client.create_model(
        workspace_id=workspace_id,
        model_store_name=model_store_name,
        local_name=ensemble_name,
        display_name=args.ensemble_model_display_name,
        prefer_model_server_parameters=prefer_model_server_parameters,
        category="Image/Ensemble",
        model_formats=["Python"],
        artifact_tags=artifact_tags,
        artifact_metadata=config.metadata,
        artifact_uri=ensemble_model_uri)
    bcelogger.info(f"Model {ensemble_name} created response: {response}")

    # 4. 输出文件
    write_file(obj=json.loads(response.raw_data), output_dir=args.output_model_uri)


if __name__ == "__main__":
    args = parse_args()
    package(args=args)
