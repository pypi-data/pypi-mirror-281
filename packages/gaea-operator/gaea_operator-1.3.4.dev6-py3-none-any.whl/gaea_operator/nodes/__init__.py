#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/21
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from .train import Train, train_outputs
from .eval import Eval, eval_inputs, eval_outputs
from .transform import Transform, transform_inputs, transform_outputs
from .transform_eval import TransformEval, transform_eval_inputs, transform_eval_outputs
from .package import Package, package_inputs, package_outputs
from .inference import Inference, inference_inputs
from .types import Image, Properties
from .base_node import set_node_parameters

__all__ = ["train_outputs",
           "Train",
           "eval_inputs",
           "eval_outputs",
           "Eval",
           "transform_inputs",
           "transform_outputs",
           "Transform",
           "transform_eval_inputs",
           "transform_eval_outputs",
           "TransformEval",
           "package_inputs",
           "package_outputs",
           "Package",
           "inference_inputs",
           "Inference",
           "Image",
           "Properties",
           "set_node_parameters"]