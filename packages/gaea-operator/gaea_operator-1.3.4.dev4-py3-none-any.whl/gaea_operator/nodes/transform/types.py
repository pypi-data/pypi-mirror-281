#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/3
# @Author  : yanxiaodong
# @File    : intput_output.py
"""
from typing import List

from gaea_operator.artifacts import Variable

transform_inputs: List[Variable] = \
    [
        Variable(type="model", name="input_model_uri", value="train.output_model_uri")
    ]
transform_outputs: List[Variable] = \
    [
        Variable(type="model", name="output_model_uri", displayName="模型转换后的模型", value="transform.output_model_uri")
    ]
