#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/12
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from typing import List, Dict
from paddleflow.pipeline import ContainerStep

from ..base_node import BaseNode
from .types import eval_inputs, eval_outputs
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import Accelerator, get_accelerator


class Eval(BaseNode):
    """
    Train
    """
    NAME = "eval"

    def __init__(self,
                 inputs: List[Variable] = eval_inputs,
                 outputs: List[Variable] = eval_outputs,
                 eval_skip: int = -1,
                 name_to_step: Dict[str, ContainerStep] = None):
        accelerator = get_accelerator(kind=Accelerator.NVIDIA)
        compute_tips = {Accelerator.NVIDIA: ["training", "tags.usage=train"] + accelerator.suggest_resource_tips()}
        flavour_tips = {Accelerator.NVIDIA: accelerator.suggest_flavour_tips()}
        properties = Properties(computeTips=compute_tips,
                                flavourTips=flavour_tips,
                                model_format=["PaddlePaddle", "PyTorch"])
        super().__init__(inputs=inputs, outputs=outputs, properties=properties)
        self.eval_skip = eval_skip
        self.name_to_step = name_to_step

    def suggest_image(self):
        """
        suggest image
        """
        for image in self.properties.images:
            if image.kind == Accelerator.NVIDIA:
                return image.name
        return ""

    def __call__(self, *args, **kwargs):
        pass