#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 20:17:34 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel
from model.network import EdgeParameter


class OptimizedEdge(BaseModel):
    index: int
    ID: int
    parameters:list[EdgeParameter]

class OptimizedTarget(BaseModel):
    index: int
    name: str
    description: str
    nodeIndexes: list[int]
    value: float
