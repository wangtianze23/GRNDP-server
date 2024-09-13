#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application classes providing the functionality of network optimization.

Created on Fri Sep 13 12:42:26 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from infrastructure.config.Service import BaseServiceConfig
from infrastructure.database.StaticResource import RegulatorDB, TargetDB
from model.experiment.Resource import ExperimentResource
from model.experiment.Option import ExperimentOption
from model.experiment.Result import ExperimentResult
from model.optimization.SpaceRepository import \
    RegulationParameterSpaceRepository, TargetSpaceRepository
from model.optimization.Optimizer import NetworkOptimizer


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
        repository = RegulationParameterSpaceRepository(self.parameterDatabase)
        regulationParameterSpaces = repository.retrieveAll()
        
        repository = TargetSpaceRepository(self.targetDatabase)
        targetSpaces = repository.retrieveAll()
        
        return ExperimentResource(optimizationSpaceList = 
                                  regulationParameterSpaces, 
                                  optimizationTargetList = targetSpaces)
    
    def optimize(self, option: ExperimentOption) -> ExperimentResult:
        """
        Optimize a network with specified options.

        Parameters
        ----------
        option : ExperimentOption
            An ExperimentOption object containing the option for 
            optimization.

        Returns
        -------
        ExperimentResult
            An ExperimentResult object containing the result from 
            a round of optimization.
        """
        repository = RegulationParameterSpaceRepository(self.parameterDatabase)
        regulationParameterSpaces = repository.retrieveAll()
        
        repository = TargetSpaceRepository(self.targetDatabase)
        targetSpaces = repository.retrieveAll()
        
        optimizer = NetworkOptimizer(regulationParameterSpaces, targetSpaces)
        result = \
            optimizer.optimizeWithSpaceAndTarget(option.nodeList, 
                                                 option.edgeList, 
                                                 option.optimizationTargetList)
        visualizedResult = [optimizer.visualize(option.nodeList, result, X) 
                            for X in option.visualizedPathList]
        return ExperimentResult(optimizedEdgeList = result.regulations, 
                                optimizedTargetList = result.targets, 
                                visualizedPathList = visualizedResult)
