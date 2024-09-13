#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application classes providing the functionality of network optimization.

Created on Fri Sep 13 12:42:26 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from infrastructure.config.Service import BaseServiceConfig
from infrastructure.database.StaticResource import RegulatorDB, TargetDB
from model.optimization.SpaceRepository import \
    EdgeParameterSpaceRepository, TargetSpaceRepository
from model.experiment.Resource import ExperimentResource
from model.experiment.Option import ExperimentOption
from model.experiment.Result import ExperimentResult


class NetworkOptimization:
    """
    The service class that provides optimization of transcriptional 
    regulatory network (GRN).
    """
    def __init__(self, config = BaseServiceConfig()):
        """
        Initialize a NetworkOptimization object.

        Parameters
        ----------
        config : BaseServiceConfig, optional
            An object of BaseServiceConfig class or its sub-class. 
            The default is an object of BaseServiceConfig initialized with 
            default parameters.

        Returns
        -------
        None.
        """
        self.parameterDatabase = RegulatorDB(config.staticResource)
        self.targetDatabase = TargetDB(config.staticResource)
    
    def getResource(self) -> ExperimentResource:
        """
        Get resources for optimization.

        Returns
        -------
        ExperimentResource
            An ExperimentResource object containing the resource for 
            launching a round of optimization.
        """
        repository = EdgeParameterSpaceRepository(self.parameterDatabase)
        edgeParameterSpaces = repository.retrieveAll()
        
        repository = TargetSpaceRepository(self.targetDatabase)
        targetSpaces = repository.retrieveAll()
        
        return ExperimentResource(optimizationSpaceList = edgeParameterSpaces, 
                                  optimizationTargetList = targetSpaces)
    
    def optimize(self, option: ExperimentOption) -> ExperimentResult:
        return ExperimentResult()
