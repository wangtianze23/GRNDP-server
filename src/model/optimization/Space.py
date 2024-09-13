#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 19:45:31 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel


class ParameterSpace(BaseModel):
    index: int
    name: str
    min: float
    max: float

class RegulationParameterSpace(BaseModel):
    ID: int
    name: str
    optimizationType: str
    regulationType: str
    parameterList: list[ParameterSpace]

class TargetSpace(BaseModel):
    index: int
    name: str
    description: str
    nodeCount: int
