#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/3
# @Author  : yanxiaodong
# @File    : input_output.py
"""
from typing import List

from gaea_operator.artifacts import Variable


train_outputs: List[Variable] = \
    [
        Variable(type="model", name="output_model_uri", displayName="模型训练后的模型", value="train.output_model_uri")
    ]
