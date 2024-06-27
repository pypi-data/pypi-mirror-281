#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/12
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from typing import Dict, List
from paddleflow.pipeline import ContainerStep
from paddleflow.pipeline import Artifact

from .types import transform_inputs, transform_outputs
from ..base_node import BaseNode, set_node_parameters
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import Accelerator, get_accelerator


class Transform(BaseNode):
    """
    Transform
    """
    NAME = "transform"

    def __init__(self,
                 inputs: List[Variable] = transform_inputs,
                 outputs: List[Variable] = transform_outputs,
                 transform_skip: int = -1,
                 algorithm: str = "",
                 category: str = "",
                 accelerator: str = Accelerator.T4,
                 name_to_step: Dict[str, ContainerStep] = None):
        self.accelerator = accelerator
        accelerator = get_accelerator(kind=Accelerator.NVIDIA)
        compute_tips = {Accelerator.NVIDIA: ["training", "tags.usage=train"] + accelerator.suggest_resource_tips()}
        flavour_tips = {Accelerator.NVIDIA: accelerator.suggest_flavour_tips()}

        accelerator = get_accelerator(kind=Accelerator.KUNLUN)
        compute_tips[Accelerator.KUNLUN] = ["training", "tags.usage=train"] + accelerator.suggest_resource_tips()
        flavour_tips[Accelerator.KUNLUN] = "c4m16"
        properties = Properties(accelerator=self.accelerator,
                                computeTips=compute_tips,
                                flavourTips=flavour_tips,
                                model_format=["TensorRT", "PaddleLite"])
        super().__init__(inputs=inputs, outputs=outputs, properties=properties)

        self.transform_skip = transform_skip
        self.algorithm = algorithm
        self.category = category
        self.name_to_step = name_to_step

    def suggest_image(self):
        """
        suggest image
        """
        for image in self.properties.images:
            if image.kind == get_accelerator(self.properties.accelerator).get_kind:
                return image.name
        return ""

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 train_model_name: str = "",
                 transform_model_name: str = "",
                 transform_model_display_name: str = "",
                 advanced_parameters: str = ""):
        """
        call
        """
        transform_params = {"transform_skip": self.transform_skip,
                            "train_model_name": train_model_name,
                            "transform_model_name": transform_model_name,
                            "transform_model_display_name": transform_model_display_name,
                            "accelerator": self.accelerator,
                            "advanced_parameters": advanced_parameters}
        transform_env = {"TRAIN_MODEL_NAME": "{{train_model_name}}",
                         "TRANSFORM_MODEL_NAME": "{{transform_model_name}}",
                         "TRANSFORM_MODEL_DISPLAY_NAME": "{{transform_model_display_name}}",
                         "ACCELERATOR": "{{accelerator}}",
                         "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        transform_env.update(base_env)
        transform_params.update(base_params)

        transform = ContainerStep(name=Transform.name(),
                                  docker_env=self.suggest_image(),
                                  env=transform_env,
                                  parameters=transform_params,
                                  outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                                  command=f'cd /root && '
                                          f'python3 -m gaea_operator.nodes.transform.transform '
                                          f'--algorithm={self.algorithm} '
                                          f'--category={self.category} '
                                          f'--input-model-uri={{{{input_model_uri}}}} '
                                          f'--output-uri={{{{output_uri}}}} '
                                          f'--output-model-uri={{{{output_model_uri}}}}')
        set_node_parameters(skip=self.transform_skip,
                            skip_name="transform_skip",
                            step=transform,
                            inputs=self.inputs,
                            name_to_step=self.name_to_step)

        return transform
