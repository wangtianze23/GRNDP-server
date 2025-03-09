#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 20:03:55 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel


class PathVisualization(BaseModel):
    sourceIndex: int
    targetIndex: int

class VisualizedPath(PathVisualization):
    image: str

class DensityVisulization(BaseModel):
    nodeIndex: int

class VisualizedDensity(DensityVisulization):
    image: str
