#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/3
# @Author  : yanxiaodong
# @File    : intput_output.py
"""
from typing import List

from gaea_operator.artifacts import Variable

eval_inputs: List[Variable] = \
    [
        Variable(type="model", name="input_model_uri", value="train.output_model_uri")
    ]
eval_outputs: List[Variable] = \
    [
        Variable(type="dataset",
                 name="output_dataset_uri",
                 displayName="模型评估的数据集",
                 value="eval.output_dataset_uri"),
        Variable(type="model",
                 name="output_model_uri",
                 displayName="模型评估后的模型",
                 value="eval.output_model_uri")
    ]