#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 19:33:04 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel
from model.network import Node
from model.optimization.option import \
    EdgeConstraint, TargetConstraint, OptimizerOption
from model.optimization.result import OptimizedEdge, OptimizedTarget
from model.visualization import PathVisualization, VisualizedPath


class OptimizationOption(BaseModel):
    nodeList: list[Node]
    edgeList: list[EdgeConstraint]
    optimizationTargetList: list[TargetConstraint]
    optimizationOption: OptimizerOption
    visualizedPathList: list[PathVisualization]
    
class OptimizationResult(BaseModel):
    optimizedEdgeList: list[OptimizedEdge]
    optimizedTargetList: list[OptimizedTarget]
    visualizedPathList: list[VisualizedPath]
