#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assembler classes for constructing DTOs of optimization spaces.

Created on Sat Jan  4 18:12:10 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from application.optimization.DTO.Space import \
    ParameterSpace, RegulationParameterSpace, TargetSpace
import model.optimization.Space


class RegulationParameterSpaceAssembler:
    @staticmethod
    def createFromModel(model: model.optimization.Space.
                               RegulationParameterSpace) \
                       -> RegulationParameterSpace:
        parameterList = []
        for i in range(model.dimension):
            parameterList.append(
                        ParameterSpace(index = i, 
                                       name = model.dimensionNames[i], 
                                       min = model.boundaries[i][0], 
                                       max = model.boundaries[i][1]))
        result = RegulationParameterSpace(ID = model.ID, 
                                          name = model.name, 
                                          optimizationType = model.source, 
                                          regulationType=model.regulationType, 
                                          parameterList = parameterList)
        return result

class TargetSpaceAssembler:
    @staticmethod
    def createFromModel(model: model.optimization.Space.TargetSpace) \
                       -> TargetSpace:
        return TargetSpace(index = model.ID, name = model.name, 
                           description = model.description, 
                           nodeCount = model.variableCount)
