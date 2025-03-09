#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assembler classes for constructing DTOs of optimization results.

Created on Sat Jan  4 22:03:15 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from application.optimization.DTO.Network import EdgeParameter
from application.optimization.DTO.Result import \
    OptimizedRegulation, OptimizedTarget, VisualizedPath, VisualizedDensity
from infrastructure.plot.StaticPlot import StaticFigure
import model.optimization.Network
from model.optimization.Constraint import TargetConstraint


class OptimizedRegulationAssembler:
    @staticmethod
    def createFromModel(model: model.optimization.Network.OptimizedRegulation, 
                        index: int) -> OptimizedRegulation:
        return OptimizedRegulation(index = index, ID = model.ID, 
                                   parameters = [EdgeParameter(index = X.index,
                                                               name = X.name, 
                                                               value = X.value)
                                                 for X in model.parameters])

class OptimizedTargetAssembler:
    @staticmethod
    def createFromConstraint(constraint: TargetConstraint, index: int, 
                             value: float) -> OptimizedTarget:
        return OptimizedTarget(index = index, name = constraint.space.name, 
                               description = constraint.space.description, 
                               nodeIndexes = constraint.nodeIndexes,
                               value = value)

class VisualizedPathAssembler:
    @staticmethod
    def createFromFigure(figure: StaticFigure, 
                         path: model.optimization.Network.Path) \
                        -> VisualizedPath:
        return VisualizedPath(sourceIndex = path.sourceIndex, 
                              targetIndex = path.targetIndex, 
                              image = figure.toBase64())

class VisualizedDensityAssembler:
    @staticmethod
    def createFromFigure(figure: StaticFigure, 
                         nodeIndex: int) -> VisualizedPath:
        return VisualizedDensity(nodeIndex = nodeIndex, 
                                 image = figure.toBase64())
