#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/21
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from typing import Dict, List
from paddleflow.pipeline import ContainerStep
from paddleflow.pipeline import Artifact

from .types import transform_eval_inputs, transform_eval_outputs
from ..base_node import BaseNode, set_node_parameters
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import get_accelerator, Accelerator


class TransformEval(BaseNode):
    """
    Transform
    """
    NAME = "transform_eval"

    def __init__(self,
                 inputs: List[Variable] = transform_eval_inputs,
                 outputs: List[Variable] = transform_eval_outputs,
                 transform_eval_skip: int = -1,
                 algorithm: str = "",
                 accelerator: str = "",
                 name_to_step: Dict[str, ContainerStep] = None):
        self.accelerator = accelerator
        accelerator = get_accelerator(kind=Accelerator.NVIDIA)
        compute_tips = {Accelerator.NVIDIA: ["training", "tags.usage=train"] + accelerator.suggest_resource_tips()}
        flavour_tips = {Accelerator.NVIDIA: accelerator.suggest_flavour_tips()}

        accelerator = get_accelerator(kind=Accelerator.KUNLUN)
        compute_tips[Accelerator.KUNLUN] = ["training", "tags.usage=train"] + accelerator.suggest_resource_tips()
        flavour_tips[Accelerator.KUNLUN] = accelerator.suggest_flavour_tips()
        properties = Properties(accelerator=self.accelerator,
                                computeTips=compute_tips,
                                flavourTips=flavour_tips,
                                model_format=["TensorRT", "PaddleLite"])
        super().__init__(inputs=inputs, outputs=outputs, properties=properties)

        self.transform_eval_skip = transform_eval_skip
        self.algorithm = algorithm
        self.name_to_step = name_to_step

    def suggest_image(self):
        """
        suggest image
        """
        for image in self.properties.images:
            if image.kind == self.accelerator:
                return image.name
        return ""

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 dataset_name: str = "",
                 transform_model_name: str = ""):
        transform_eval_params = {"transform_eval_skip": self.transform_eval_skip,
                                 "accelerator": self.accelerator,
                                 "dataset_name": dataset_name,
                                 "model_name": transform_model_name,
                                 "advanced_parameters": '{"conf_threshold":"0.5",'
                                                        '"iou_threshold":"0.5"}'}
        transform_eval_env = {"ACCELERATOR": "{{accelerator}}",
                              "DATASET_NAME": "{{dataset_name}}",
                              "MODEL_NAME": "{{model_name}}",
                              "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        transform_eval_params.update(base_params)
        transform_eval_env.update(base_env)
        accelerator = get_accelerator(name=self.accelerator)
        transform_eval_env.update(accelerator.suggest_env())

        transform_eval = ContainerStep(name=TransformEval.name(),
                                       docker_env=self.suggest_image(),
                                       env=transform_eval_env,
                                       parameters=transform_eval_params,
                                       outputs={"output_uri": Artifact(), "output_dataset_uri": Artifact()},
                                       command=f'cd /root && '
                                               f'python3 -m gaea_operator.nodes.transform_eval.transform_eval '
                                               f'--algorithm={self.algorithm} '
                                               f'--input-model-uri={{{{input_model_uri}}}} '
                                               f'--input-dataset-uri={{{{input_dataset_uri}}}} '
                                               f'--output-dataset-uri={{{{output_dataset_uri}}}} '
                                               f'--output-uri={{{{output_uri}}}}')
        set_node_parameters(skip=self.transform_eval_skip,
                            skip_name="transform_eval_skip",
                            step=transform_eval,
                            inputs=self.inputs,
                            name_to_step=self.name_to_step)

        return transform_eval
