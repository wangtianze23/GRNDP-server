#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 22:28:22 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class NoPathException(Exception):
    def __init__(self, sourceIndex: int, targetIndex: int):
        self.actual = (sourceIndex, targetIndex)
    
    def __str__(self) -> str:
        return 'No path found from node {} to node {}'.\
               format(self.actual[0], self.actual[1])
