#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/3
# @Author  : yanxiaodong
# @File    : intput_output.py
"""
from typing import List

from gaea_operator.artifacts import Variable

package_inputs: List[Variable] = \
    [
        Variable(type="model", name="input_model_uri", value="transform.output_model_uri")
    ]
package_outputs: List[Variable] = \
    [
        Variable(type="model", name="output_model_uri", displayName="模型组装后的模型", value="package.output_model_uri")
    ]