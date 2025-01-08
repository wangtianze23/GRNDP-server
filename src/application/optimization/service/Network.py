#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application classes providing the functionality of network optimization.

Created on Fri Sep 13 12:42:26 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from application.optimization.assembler.SpaceAssembler import \
    RegulationParameterSpaceAssembler, TargetSpaceAssembler
from application.optimization.assembler.ResultAssembler import \
    OptimizedRegulationAssembler, OptimizedTargetAssembler, \
    VisualizedPathAssembler
from application.optimization.DTO.Option import OptimizationOption
from application.optimization.DTO.Resource import OptimizationResource
from application.optimization.DTO.Result import \
    OptimizationResult, OptimizationResultBody
from infrastructure.config.Service import BaseServiceConfig
from infrastructure.database.StaticResource import RegulatorDB, TargetDB
from infrastructure.plot.StaticPlot import BaseStaticPlot
from model.optimization.Constraint import \
    ParameterConstraint, RegulationConstraint, TargetConstraint
from model.optimization.Network import Node
from model.optimization.NetworkRepresentation import PathRepresentation
from model.optimization.Optimizer import NetworkOptimizer
from model.optimization.OptimizerException import OptimizationFailedException
from model.optimization.ParameterSpaceRepository import \
    RegulationParameterSpaceRepository
from model.optimization.TargetRepository import BaseTargetRepository


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
        self.canvas = BaseStaticPlot(config.plotConfiguration)
    
    def getResource(self) -> OptimizationResource:
        """
        Get resources for optimization.

        Returns
        -------
        OptimizationResource
            An OptimizationResource object containing the resource for 
            launching a round of optimization.
        """
        repository = RegulationParameterSpaceRepository(self.parameterDatabase)
        parameterSpaces = [RegulationParameterSpaceAssembler.createFromModel(X)
                           for X in repository.retrieveAll()]
        
        repository = BaseTargetRepository(self.targetDatabase)
        targetSpaces = [TargetSpaceAssembler.createFromModel(X) 
                        for X in repository.retrieveAll()]
        
        return OptimizationResource(optimizationSpaceList = parameterSpaces, 
                                    optimizationTargetList = targetSpaces)
    
    def optimize(self, option: OptimizationOption) -> OptimizationResult:
        """
        Optimize a network with specified options.

        Parameters
        ----------
        option : ExperimentOption
            An ExperimentOption object containing the option for 
            optimization.

        Returns
        -------
        OptimizationResult
            An OptimizationResult object containing the result from 
            a round of optimization.
        """
        # Collect the resources for optimization
        nodes = [Node(X.index, X.name, X.entityType) for X in option.nodeList]
        
        repository = RegulationParameterSpaceRepository(self.parameterDatabase)
        parameterSpaces = \
            [RegulationConstraint(edge.sourceIndex, edge.targetIndex, 
                                  edge.regulationType, 
                                  repository.retrieveByID(edge.
                                                          optimizationSpaceID), 
                                  [ParameterConstraint(X.index, X.min, X.max) 
                                   for X in edge.optimizationConstraints]) 
             for edge in option.edgeList]
        
        repository = BaseTargetRepository(self.targetDatabase)
        targetSpaces = [TargetConstraint(target.nodeIndexes, 
                                         repository.retrieveByID(target.index)) 
                        for target in option.optimizationTargetList]
        
        # Set up an optimizer
        optimizer = NetworkOptimizer()
        optimizer.setMaximumIteration(option.optimizationOption.maxIteration)
        optimizer.setSeed(option.optimizationOption.seed 
                          if option.optimizationOption.useSeed else None)
        optimizer.setTrajectoryCount(option.optimizationOption.trajectoryCount)
        
        # Run optimization
        try:
            result = optimizer.optimizeWithSpaceAndTarget(nodes, 
                                                          parameterSpaces, 
                                                          targetSpaces)
        except OptimizationFailedException as e:
            return OptimizationResult(
                    message = 'Optimization failed due to "{}"'.format(str(e)),
                    processId = option.processId, 
                    data = OptimizationResultBody(optimizedEdgeList = [],
                                                  optimizedTargetList = [], 
                                                  visualizedPathList = []))
        
        # Visualize paths in the optimized network
        representator = PathRepresentation(self.canvas)
        visualizedResult = [representator.response(option.nodeList, 
                                                   result.regulations, X) 
                            for X in option.visualizedPathList]
        
        # Assemble the optimization result
        resultBody = OptimizationResultBody(
                        optimizedEdgeList = 
                        [OptimizedRegulationAssembler.createFromModel(X, i) 
                         for i, X in enumerate(result.regulations)],
                        optimizedTargetList = 
                        [OptimizedTargetAssembler.
                         createFromConstraint(targetSpaces[i], i, X) 
                         for i, X in enumerate(result.targets)], 
                        visualizedPathList = 
                        [VisualizedPathAssembler.createFromFigure(X, Y) 
                         for X, Y in zip(visualizedResult, 
                                         option.visualizedPathList)])
        return OptimizationResult(message = result.message, 
                                processId = option.processId, 
                                data = resultBody)
