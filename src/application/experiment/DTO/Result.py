#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 16:49:54 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pydantic import BaseModel, field_serializer


class ExperimentResultBody(BaseModel):
    pass

class ExperimentResult(BaseModel):
    message: str
    processId: str
    data: ExperimentResultBody
    
    @field_serializer('data', when_used='json')
    def serializeData(self, data: ExperimentResultBody):
        return data.model_dump_json()
