#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 19:33:04 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from application.experiment.DTO.Resource import ExperimentResource
from application.optimization.DTO.Space \
    import RegulationParameterSpace, TargetSpace


class OptimizationResource(ExperimentResource):
    optimizationSpaceList: list[RegulationParameterSpace]
    optimizationTargetList: list[TargetSpace]
