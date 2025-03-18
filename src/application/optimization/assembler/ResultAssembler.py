#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assembler classes for constructing DTOs of optimization results.

Created on Sat Jan  4 22:03:15 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from base64 import b64encode
from application.optimization.DTO.File import ResultFile
from application.optimization.DTO.Network import EdgeParameter
from application.optimization.DTO.Option import OptimizationOption
from application.optimization.DTO.Result import \
    OptimizedRegulation, OptimizedTarget, VisualizedPath, VisualizedDensity, \
    OptimizationResultBody
from infrastructure.plot.StaticPlot import StaticFigure
from model.assemblage.Promoter import RegulationPromoterCollection
from model.optimization.Constraint import TargetConstraint
import model.optimization.Network
from model.optimization.Optimizer import OptimizationResult


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

class ResultFileAssembler:
    @staticmethod
    def createFromPromoters(promoters: RegulationPromoterCollection) \
                           -> ResultFile:
        return ResultFile(name = 'promoter.gb', fileType = 'promoters', 
                          mimeType = 'chemical/x-genbank', 
                          contentBase64 = 
                          b64encode(promoters.toGenbank().
                                    encode('utf-8')).decode('utf-8'))

class ResultBodyAssembler:
    @staticmethod
    def createEmptyObject() -> OptimizationResultBody:
        return OptimizationResultBody(optimizedEdgeList = [],
                                      optimizedTargetList = [], 
                                      visualizedPathList = [], 
                                      visualizedDensityList = [], 
                                      resultFileList = [])
    
    @staticmethod
    def createFromOptimizationResult(option: OptimizationOption, 
                                     targetSpaces: list[TargetConstraint], 
                                     result: OptimizationResult, 
                                     visualizedPaths: list[StaticFigure], 
                                     visualizedDensities: list[StaticFigure], 
                                     promoters: RegulationPromoterCollection) \
                                    -> OptimizationResultBody:
        # Assemble the result body
        return OptimizationResultBody(
                        optimizedEdgeList = 
                        [OptimizedRegulationAssembler.createFromModel(X, i) 
                         for i, X in enumerate(result.regulations)],
                        optimizedTargetList = 
                        [OptimizedTargetAssembler.
                         createFromConstraint(targetSpaces[i], i, X) 
                         for i, X in enumerate(result.targets)], 
                        visualizedPathList = 
                        [VisualizedPathAssembler.createFromFigure(X, Y) 
                         for X, Y in zip(visualizedPaths, 
                                         option.visualizedPathList)], 
                        visualizedDensityList = 
                        [VisualizedDensityAssembler.
                         createFromFigure(X, Y.nodeIndex)
                         for X, Y in zip(visualizedDensities, 
                                         option.visualizedDensityList)], 
                        resultFileList = [ResultFileAssembler.
                                          createFromPromoters(promoters)])
