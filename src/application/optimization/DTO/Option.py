#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 20:17:28 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel
from application.experiment.DTO.Option import ExperimentOption
from application.optimization.DTO.Network import Node, Edge
from application.optimization.DTO.Visualization import \
    DensityVisulization, PathVisualization


class ParameterConstraint(BaseModel):
    index: int
    min: float
    max: float

class RegulationConstraint(Edge):
    optimizationType: str
    optimizationSpaceID: int
    optimizationConstraints: list[ParameterConstraint] = []

class TargetConstraint(BaseModel):
    index: int
    nodeIndexes: list[int]
    expectedValue: float = None

class OptimizerOption(BaseModel):
    seed: int
    useSeed: bool
    trajectoryCount: int
    maxIteration: int
    minNoise: float = 0.001
    relativeNoise: float = 0.2
    timeSpan: float = 24

class OptimizationOption(ExperimentOption):
    nodeList: list[Node]
    edgeList: list[RegulationConstraint]
    optimizationTargetList: list[TargetConstraint]
    optimizationOption: OptimizerOption
    visualizedPathList: list[PathVisualization] = []
    visualizedDensityList: list[DensityVisulization] = []
