#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 16:29:11 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class OptimizationFailedException(Exception):
    def __str__(self) -> str:
        return 'Unknown error occurred during optimization.'

class NetworkTypeNotSupportedException(OptimizationFailedException):
    def __init__(self, providedType: str):
        self.actual = providedType
    
    def __str__(self) -> str:
        return 'The network of type "{}" is not supported'.format(self.actual)

class TargetTypeNotSupportedException(OptimizationFailedException):
    def __init__(self, providedType: str):
        self.actual = providedType
    
    def __str__(self) -> str:
        return 'The target of type "{}" is not supported'.format(self.actual)

class ParameterRangeEmptyException(OptimizationFailedException):
    def __init__(self, parameterName: str, spaceName = ''):
        self.actual = parameterName
        self.reference = spaceName
    
    def __str__(self) -> str:
        return 'The range of parameter "{}" in space{} is empty under '\
               'the given constraints'.format(self.actual, 
                                              ' "{}"'.format(self.reference) 
                                              if self.reference else '')

class ParameterNotConvergedException(OptimizationFailedException):
    def __init__(self, spaceName = ''):
        self.reference = spaceName
    
    def __str__(self) -> str:
        return 'The parameters in space{} were not converged'.\
               format(' {}'.format(self.reference) if self.reference else '')
