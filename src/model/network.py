#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 19:37:13 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel


class Node(BaseModel):
    index: int
    name: str
    entityType: str

class Edge(BaseModel):
    index: int
    regulationType: str
    sourceIndex: int
    targetIndex: int

class EdgeParameter(BaseModel):
    index: int
    name: str
    value: float
