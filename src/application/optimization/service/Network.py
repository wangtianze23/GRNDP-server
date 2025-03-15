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
    ResultBodyAssembler
from application.optimization.DTO.Option import \
    OptimizationOption, OptimizerOption
from application.optimization.DTO.Resource import OptimizationResource
from application.optimization.DTO.Result import \
    OptimizedRegulation, OptimizationResult, OptimizationResultBody
from infrastructure.config.Service import BaseServiceConfig
from infrastructure.database.StaticResource import RegulatorDB, TargetDB
from infrastructure.plot.StaticPlot import BaseStaticPlot, StaticFigure
from model.optimization.Constraint import \
    ParameterConstraint, RegulationConstraint, TargetConstraint
from model.optimization.Network import Node, Path
from model.optimization.NetworkRepresentation import \
    PathRepresentation, DensityRepresentation
from model.optimization.Optimizer import \
    NetworkOptimizer, DynamicSimulationOption
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
        self.config = config
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
                                         repository.retrieveByID(target.ID or 
                                                                 target.index),
                                         target.expectedValue) 
                        for target in option.optimizationTargetList]
        
        # Set up an optimizer
        optimizer = NetworkOptimizer()
        optimizer.setDebugOutput(self.config.debugOutput)
        optimizer.setMaximumIteration(option.optimizationOption.maxIteration)
        optimizer.setSeed(option.optimizationOption.seed 
                          if option.optimizationOption.useSeed else None)
        optimizer.setSimulationOption(
            DynamicSimulationOption(option.optimizationOption.minNoise, 
                                    option.optimizationOption.relativeNoise, 
                                    option.optimizationOption.timeSpan, 
                                    option.optimizationOption.trajectoryCount))
        
        # Run optimization
        try:
            result = optimizer.optimizeWithSpaceAndTarget(nodes, 
                                                          parameterSpaces, 
                                                          targetSpaces)
        except OptimizationFailedException as e:
            return OptimizationResult(
                    message = 'Optimization failed due to "{}"'.format(str(e)),
                    processId = option.processId, 
                    data = ResultBodyAssembler.createEmptyObject())
        
        # Visualize the optimized network
        visualizedPaths = [self.visualizePath(nodes, result.regulations, 
                                              X.sourceIndex, X.targetIndex) 
                           for X in option.visualizedPathList]
        visualizedDensities = [self.visualizeDensity(nodes, result.regulations,
                                                     X.nodeIndex, 
                                                     option.optimizationOption)
                           for X in option.visualizedDensityList]
        
        # Assemble the optimization result
        resultBody = ResultBodyAssembler.createFromOptimizationResult(
                                        option, targetSpaces, result, 
                                        visualizedPaths, visualizedDensities)
        return OptimizationResult(message = result.message, 
                                  processId = option.processId, 
                                  data = resultBody)
    
    def visualizePath(self, nodeList: list[Node], 
                      regulationList: list[OptimizedRegulation], 
                      sourceIndex: int, targetIndex: int) -> StaticFigure:
        """
        Visualize the response function along a path in an optimized network.

        Parameters
        ----------
        nodeList : list[Node]
            A list of Node objects representing the nodes in the network.
        regulationList : list[OptimizedRegulation]
            A list of OptimizedRegulation objects representing the optimized 
            regulation (edges) in the network.
        sourceIndex : int
            An integer indicating the index of the source node of a path to 
            visualize.
        targetIndex : int
            An integer indicating the index of the target node of a path to 
            visualize.

        Returns
        -------
        StaticFigure
            A StaticFigure object holding the visualized path.
        """
        # Set up visualizers for the optimized network
        representator = PathRepresentation(self.canvas)
        
        return representator.response(nodeList, regulationList, 
                                      Path(sourceIndex, targetIndex))
    
    def visualizeDensity(self, nodeList: list[Node], 
                         regulationList: list[OptimizedRegulation], 
                         nodeIndex: int, option: OptimizerOption) \
                        -> StaticFigure:
        """
        Visualize the probability density of the value of a node in 
        an optimized network.

        Parameters
        ----------
        nodeList : list[Node]
            A list of Node objects representing the nodes in the network.
        regulationList : list[OptimizedRegulation]
            A list of OptimizedRegulation objects representing the optimized 
            regulation (edges) in the network.
        nodeIndex : int
            An integer indicating the index of the node to visualize.
        option : OptimizerOption
            An OptimizerOption object holding the additional parameters used 
            during optimization.

        Returns
        -------
        StaticFigure
            A StaticFigure object holding the visualized probability density.
        """
        # Set up visualizers for the optimized network
        representator = DensityRepresentation(self.canvas)
        representator.setSampleCount(option.optimizationOption.trajectoryCount)
        representator.setSamplingTime(option.optimizationOption.timeSpan)
        
        return representator.density(nodeList, regulationList, nodeIndex, 
                                     minNoise = option.minNoise, 
                                     relativeNoise = option.relativeNoise)
