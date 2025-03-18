#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 19:46:11 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel


class ResultFile(BaseModel):
    name: str
    fileType: str
    mimeType: str
    contentBase64: str
