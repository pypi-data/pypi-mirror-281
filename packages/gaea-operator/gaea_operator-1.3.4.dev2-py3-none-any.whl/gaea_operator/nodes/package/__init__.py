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

from .types import package_inputs, package_outputs
from ..base_node import BaseNode, set_node_parameters
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import Accelerator


class Package(BaseNode):
    """
    Transform
    """
    NAME = "package"

    def __init__(self,
                 inputs: List[Variable] = package_inputs,
                 outputs: List[Variable] = package_outputs,
                 package_skip: int = -1,
                 algorithm: str = "",
                 accelerator: str = "",
                 name_to_step: Dict[str, ContainerStep] = None):
        compute_tips = {Accelerator.NVIDIA: ["training", "tags.usage=train"],
                        Accelerator.KUNLUN: ["training", "tags.usage=train"]}
        flavour_tips = {Accelerator.NVIDIA: "c4m16",
                        Accelerator.KUNLUN: "c4m16"}
        properties = Properties(accelerator=accelerator,
                                computeTips=compute_tips,
                                flavourTips=flavour_tips,
                                model_format=["TensorRT", "PaddleLite"])
        super().__init__(inputs=inputs, outputs=outputs, properties=properties)

        self.package_skip = package_skip
        self.algorithm = algorithm
        self.accelerator = accelerator
        self.name_to_step = name_to_step

    def suggest_image(self):
        """
        suggest image
        """
        for image in self.properties.images:
            if image.kind == Accelerator.NVIDIA:
                return image.name
        return ""

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 transform_model_name: str = "",
                 ensemble_model_name: str = "",
                 sub_extra_models: str = "",
                 ensemble_model_display_name: str = ""):
        package_params = {"package_skip": self.package_skip,
                          "accelerator": self.accelerator,
                          "transform_model_name": transform_model_name,
                          "ensemble_model_name": ensemble_model_name,
                          "sub_extra_models": sub_extra_models,
                          "ensemble_model_display_name": ensemble_model_display_name}
        package_env = {"ACCELERATOR": "{{accelerator}}",
                       "TRANSFORM_MODEL_NAME": "{{transform_model_name}}",
                       "ENSEMBLE_MODEL_NAME": "{{ensemble_model_name}}",
                       "SUB_EXTRA_MODELS": "{{sub_extra_models}}",
                       "ENSEMBLE_MODEL_DISPLAY_NAME": "{{ensemble_model_display_name}}"}
        package_params.update(base_params)
        package_env.update(base_env)

        package = ContainerStep(name=Package.name(),
                                docker_env=self.suggest_image(),
                                env=package_env,
                                parameters=package_params,
                                outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                                command=f'cd /root && '
                                        f'python3 -m gaea_operator.nodes.package.package '
                                        f'--algorithm={self.algorithm} '
                                        f'--input-model-uri={{{{input_model_uri}}}} '
                                        f'--output-uri={{{{output_uri}}}} '
                                        f'--output-model-uri={{{{output_model_uri}}}}')
        set_node_parameters(skip=self.package_skip,
                            skip_name="package_skip",
                            step=package,
                            inputs=self.inputs,
                            name_to_step=self.name_to_step)

        return package
