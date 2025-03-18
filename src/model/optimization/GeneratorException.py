#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 17:20:08 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class RegulationNotExistException(Exception):
    def __init__(self, nodeIndex: int):
        self.actual = nodeIndex
    
    def __str__(self) -> str:
        return 'The regulation on node {} does not exist'.format(self.actual)

class RegulationTypeNotSupportedException(Exception):
    def __init__(self, providedType: str):
        self.actual = providedType
    
    def __str__(self) -> str:
        return 'The regulation of type "{}" is not supported'.\
               format(self.actual)
