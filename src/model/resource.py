#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 19:33:04 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel
from model.optimization.space import EdgeParameterSpace, TargetSpace


class ExperimentResource(BaseModel):
    optimizationSpaceList: list[EdgeParameterSpace]
    optimizationTargetList: list[TargetSpace]
