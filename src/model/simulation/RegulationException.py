#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 17:22:06 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

def RegulationInvalidTypeException(Exception):
    def __init__(self, providedType: str):
        self.actual = providedType
    
    def __str__(self) -> str:
        return 'Invalid type provided: {}'.format(self.actual)
