#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/25
# @Author  : yanxiaodong
# @File    : types.py
"""
from typing import List, Dict
from pydantic import BaseModel


class Image(BaseModel):
    """
    Image
    """
    kind: str
    name: str


class Properties(BaseModel):
    """
    Properties
    """
    accelerator: str = None
    computeTips: Dict[str, List] = None
    flavourTips: Dict[str, str] = None
    images: List[Image] = None
    modelFormats: List[str] = None