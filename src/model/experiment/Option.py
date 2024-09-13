#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 19:33:04 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel
from model.network import Node
from model.optimization.Option import \
    EdgeConstraint, TargetConstraint, OptimizerOption
from model.optimization.Visualization import PathVisualization


class ExperimentOption(BaseModel):
    nodeList: list[Node]
    edgeList: list[EdgeConstraint]
    optimizationTargetList: list[TargetConstraint]
    optimizationOption: OptimizerOption
    visualizedPathList: list[PathVisualization]
