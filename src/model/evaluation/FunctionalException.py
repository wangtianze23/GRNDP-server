#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 11:08:38 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class FunctionalTypeNotSupported(Exception):
    def __init__(self, typeName: str):
        self.actual = typeName
    
    def __str__(self) -> str:
        return 'The functional of type "{}" is not supported'.\
               format(self.actual)
