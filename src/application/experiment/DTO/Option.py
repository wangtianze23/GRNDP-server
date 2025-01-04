#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 19:33:04 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel


class ExperimentOption(BaseModel):
    processId: str = ''
    
    def isAsynchronous(self) -> bool:
        return len(self.processId) > 0
