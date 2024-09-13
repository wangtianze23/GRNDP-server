#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 16:49:54 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel
from model.optimization.Result import OptimizedRegulation, OptimizedTarget
from model.optimization.Visualization import VisualizedPath


class ExperimentResult(BaseModel):
    optimizedEdgeList: list[OptimizedRegulation]
    optimizedTargetList: list[OptimizedTarget]
    visualizedPathList: list[VisualizedPath]
