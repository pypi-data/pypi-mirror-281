#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/20
# @Author  : yanxiaodong
# @File    : base_node.py
"""
from typing import List, Dict
from abc import ABCMeta, abstractmethod
from paddleflow.pipeline import ContainerStep

from gaea_operator.artifacts import Variable
from .types import Properties


class BaseNode(metaclass=ABCMeta):
    """
    BaseNode
    """
    NAME = ""

    def __init__(self,
                 inputs: List[Variable] = None,
                 outputs: List[Variable] = None,
                 properties: Properties = None,
                 **kwargs):
        self._inputs = inputs
        self._outputs = outputs
        self._properties = properties

    @classmethod
    def name(cls):
        """
        name
        """
        return cls.NAME

    @property
    def inputs(self) -> List[Variable]:
        """
        input
        """
        return self._inputs

    @property
    def outputs(self) -> List[Variable]:
        """
        output
        """
        return self._outputs

    @property
    def properties(self) -> Properties:
        """
        properties
        """
        return self._properties

    @properties.setter
    def properties(self, values: Properties):
        if self._properties is None:
            self._properties = values
        else:
            properties_dict = self._properties.dict()
            properties_dict.update(values.dict())
            self._properties = Properties(**properties_dict)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


def set_node_parameters(skip: int,
                        skip_name: str,
                        step: ContainerStep,
                        inputs: List[Variable],
                        name_to_step: Dict[str, ContainerStep]):
    """
    set node parameters
    """
    if skip > 0:
        step.condition = f"{step.parameters[skip_name]} < 0"
    if isinstance(inputs[0], Variable):
        for variable in inputs:
            if variable.value != "":
                name, value = variable.value.split(".")
                step.inputs[variable.name] = getattr(name_to_step[name], "outputs")[value]
            else:
                step.parameters[variable.name] = ""