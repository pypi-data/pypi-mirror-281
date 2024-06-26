#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/3
# @Author  : yanxiaodong
# @File    : intput_output.py
"""
from typing import List

from gaea_operator.artifacts import Variable

inference_inputs: List[Variable] = \
    [
        Variable(type="model", name="input_model_uri", value="package.output_model_uri"),
        Variable(type="dataset", name="input_dataset_uri", value="eval.output_dataset_uri")
    ]
