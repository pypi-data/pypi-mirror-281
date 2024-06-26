#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/12
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from typing import List

from ..base_node import BaseNode
from .types import train_outputs
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import Accelerator, get_accelerator


class Train(BaseNode):
    """
    Train
    """
    NAME = "train"

    def __init__(self,
                 outputs: List[Variable] = train_outputs,
                 train_skip: int = -1):
        accelerator = get_accelerator(kind=Accelerator.NVIDIA)
        compute_tips = {Accelerator.NVIDIA: ["training", "tags.usage=train"] + accelerator.suggest_resource_tips()}
        flavour_tips = {Accelerator.NVIDIA: accelerator.suggest_flavour_tips()}
        properties = Properties(computeTips=compute_tips,
                                flavourTips=flavour_tips,
                                model_format=["PaddlePaddle", "PyTorch"])
        super().__init__(outputs=outputs, properties=properties)
        self.train_skip = train_skip

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