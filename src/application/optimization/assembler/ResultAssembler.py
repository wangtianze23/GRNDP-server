#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assembler classes for constructing DTOs of optimization results.

Created on Sat Jan  4 22:03:15 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from base64 import b64encode
import tempfile
from matplotlib.figure import Figure
from application.optimization.DTO.Network import EdgeParameter
from application.optimization.DTO.Result import \
    OptimizedRegulation, OptimizedTarget, VisualizedPath
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
    def figureToBase64(figure: Figure) -> str:
        encodedImage = ''
        if figure is not None:
            with tempfile.NamedTemporaryFile('rb') as tempFile:
                figure.savefig(tempFile.name, format = 'png')
                encodedImage = b64encode(tempFile.read()).decode('utf-8')
                tempFile.close()
        return encodedImage

    @staticmethod
    def createFromFigure(figure: Figure, 
                         path: model.optimization.Network.Path) \
                        -> VisualizedPath:
        return VisualizedPath(sourceIndex = path.sourceIndex, 
                              targetIndex = path.targetIndex, 
                              image = 
                              VisualizedPathAssembler.figureToBase64(figure))
