#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:05:03 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from collections import OrderedDict
import math
import scipy.optimize as Optimize
from infrastructure.math.number import centroid, geometricMean, kNN
from infrastructure.math.number import intersectRange, intersectRanges
from model.optimization.Constraint import RegulationConstraint
from model.optimization.Network import Parameter, OptimizedRegulation
from model.optimization.OptimizerException import \
    ParameterNotConvergedException, ParameterRangeEmptyException
from model.optimization.ParameterSpace import DiscreteRegulationParameterSpace
from model.optimization.RandomOptimizer import RandomBoundedStep
from model.simulation.Network import \
    NetworkParameterIndex, ParameterMapping, AcyclicNetwork


class AcyclicNetworkOptimizer:
    """
    The class for optimizing AcyclicNetwork objects.
    """
    def __init__(self):
        """
        Initialize a MixedNetworkOptimizer object.

        Returns
        -------
        None.
        """
        self.debugOutput = False
        self.maxIteration = 10
        self.maxIteration2 = 20
        self.relativeStepSize = 0.2
        self.neighbourCount = 5
        self.seed = 0
    
    def setDebugOutput(self, debugOutput = True):
        """
        Set the output of debug information.

        Parameters
        ----------
        debugOutput :bool, optional
            Whether to print detailed information about the optimization to 
            the standard output.
            The default is True.

        Returns
        -------
        None.
        """
        self.debugOutput = debugOutput
    
    def setMaximumIteration(self, maxIteration = 100):
        """
        Set the number of iteration for optimization.

        Parameters
        ----------
        maxIteration : int, optional
            An integer indicating the maximum number of iteration. 
            The default is 100.

        Returns
        -------
        None.
        """
        self.maxIteration = maxIteration
    
    def setSeed(self, seed = None):
        """
        Set the seed for the random number generator (RNG) when generating 
        sequences.

        Parameters
        ----------
        seed : int or NoneType
            An integer fed to the RNG, or None if no fixed seed is used.
            The default is None.

        Returns
        -------
        None.
        """
        self.seed = seed
    
    @staticmethod
    def updateModel(model: AcyclicNetwork, parameters: list[float], 
                    parameterIndexes: list[NetworkParameterIndex]):
        """
        Update the parameter of a model.

        Parameters
        ----------
        model : AcyclicNetwork
            An AcyclicNetwork object representing the network to optimize.
        parameters: list[float]
            A list of numeric values representing the network parameters to 
            update.
        parameterIndexes : list[NetworkParameterIndex]
            A list of NetworkParameterIndex objects representing the index of 
            parameters to update.

        Returns
        -------
        None.
        """
        for index, parameter in zip(parameterIndexes, parameters):
            if index.parameterIndex is not None and not math.isnan(parameter):
                model.updateRegulation(index, parameter)
    
    @staticmethod
    def lossFunction(model: AcyclicNetwork, parameters: list[float], 
                     parameterIndexes: list[NetworkParameterIndex], 
                     targetFunctions: list[object]) -> float:
        """
        Calculate the optimization loss on a model and a list of targets.

        Parameters
        ----------
        model : AcyclicNetwork
            An AcyclicNetwork object representing the network to optimize.
        parameters: list[float]
            A list of numeric values representing the network parameters to 
            update before evaluating the targets.
        parameterIndexes : list[NetworkParameterIndex]
            A list of NetworkParameterIndex objects representing the index of 
            parameters in a network.
        targetFunctions : list[object]
            A list of callable objects (wrapped functions) to evaluate after 
            the model has been updated.

        Returns
        -------
        float
            The optimization loss evaluated on the updated model.
        """
        if len(parameterIndexes) > 0:
            AcyclicNetworkOptimizer.updateModel(model, 
                                                parameters, parameterIndexes)
        return math.prod(X() for X in targetFunctions)
    
    def optimizeOnce(self, model: AcyclicNetwork, 
                     parameterIndexes: list[NetworkParameterIndex], 
                     initialParameters: list[float], 
                     parameterRanges: list[tuple], 
                     targetFunctions: list[object]) -> tuple:
        """
        Run a round of global optimization (minimization) of a list of targets 
        with respect to a given set of model parameters.

        Parameters
        ----------
        model : AcyclicNetwork
            An AcyclicNetwork object representing the network to optimize.
        parameterIndexes : list[NetworkParameterIndex]
            A list of NetworkParameterIndex objects representing the index of 
            parameters in a network to optimize.
        initialParameters : list[float]
            A list of numeric values representing the intial guess for each 
            parameter before optimization. The length of the list equals to 
            the length of **parameterIndexes**.
        parameterRanges : list[tuple]
            A list of tuple of (float, float) representing the boundary for 
            each parameter during optimization. The length of the list equals 
            to the length of **parameterIndexes**.
        targetFunctions : list[object]
            A list of callable objects (wrapped functions) whose values shall 
            be minimized.

        Returns
        -------
        tuple
            A tuple of the following items:
                - A float value representing the optimization loss.
                - A list of float values representing the optimized set of \
                  model parameters. The length of the list equals to \
                  the length of **parameterIndexes**.
        """
        if len(parameterIndexes) == 0:
            return (self.lossFunction(model, [], [], targetFunctions), [])
        
        # Determine the step size for updating parameters
        stepSizes = [(max(X) - min(X)) * self.relativeStepSize 
                     for X in parameterRanges]
        stepMaker = RandomBoundedStep(seed = self.seed, 
                                      maxStep = max(stepSizes), 
                                      stepBoundaries = [(-X, X) 
                                                        for X in stepSizes])
        
        result = Optimize.basinhopping(lambda X: 
                                       self.lossFunction(model, X, 
                                                         parameterIndexes, 
                                                         targetFunctions),
                                       initialParameters, 
                                       seed = self.seed, 
                                       niter = self.maxIteration, 
                                       take_step = stepMaker, 
                                       disp = self.debugOutput, 
                                       minimizer_kwargs = 
                                       {'method': 'L-BFGS-B', 
                                        'bounds': parameterRanges})
        self.updateModel(model, result['x'], parameterIndexes)
        return (result['fun'], result['x'].tolist())
    
    def optimizeClusters(self, model: AcyclicNetwork, 
                         discreteParameterGroups: list[list[list]], 
                         continuousParameterIndexes: 
                             list[NetworkParameterIndex], 
                         discreteParameterIndexes: 
                             list[list[NetworkParameterIndex]], 
                         initialContinuousParameters: list[float], 
                         initialDiscreteParameters: list[list[float]],
                         continuousParameterRanges: list[tuple], 
                         discreteParameterRanges: list[list[tuple]], 
                         targetFunctions: list[object]) -> tuple:
        # Iteratively refine the centroid of discrete parameters
        discreteParameters = initialDiscreteParameters
        historicalParameters = []
        historicalLoss = []
        iteration = 0
        while discreteParameters not in historicalParameters and \
              iteration < self.maxIteration2:
            iteration += 1
            historicalParameters.append(discreteParameters.copy())
            
            # Find neighbours around the current group of parameters
            clusters = [kNN(X, Y, self.neighbourCount) 
                        for X, Y in 
                            zip(discreteParameters, discreteParameterGroups)]
            
            # Run optimization once from the current group of parameters
            initialDiscreteParameters = [centroid([X[i] for i in Y]) for X,Y in
                                         zip(discreteParameterGroups,clusters)]
            loss, optimizedParameters = \
                self.optimizeOnce(model, 
                                  [*continuousParameterIndexes, 
                                   *(Y for X in discreteParameterIndexes 
                                     for Y in X)], 
                                  [*initialContinuousParameters, 
                                   *(Y for X in initialDiscreteParameters 
                                     for Y in X)],
                                  [*continuousParameterRanges,  
                                   *(Y for X in discreteParameterRanges 
                                     for Y in X)], 
                                  targetFunctions)
            historicalLoss.append(loss)
            if self.debugOutput:
                print('  Iteration {}, loss {}; minimum loss {}'.
                      format(iteration, loss, min(historicalLoss)))
            
            # Update with the optimized result
            initialContinuousParameters = \
                    optimizedParameters[:len(continuousParameterIndexes)]
            discreteParameterIterator = \
                iter(optimizedParameters[len(continuousParameterIndexes):])
            for i, X in enumerate(discreteParameters):
                discreteParameters[i] = [next(discreteParameterIterator) 
                                         for i in range(0, len(X))]
        
        index = historicalLoss.index(min(historicalLoss))
        return [kNN(X, Y, self.neighbourCount) for X, Y in 
                zip(historicalParameters[index], discreteParameterGroups)]
    
    def optimize(self, model: AcyclicNetwork, 
                 constraints: list[RegulationConstraint], 
                 parameterMapping: list[ParameterMapping], 
                 targetFunctions: list[object]) -> list[OptimizedRegulation]:
        """
        Optimize a model with a list of parameter constraints and targets.

        Parameters
        ----------
        model : AcyclicNetwork
            An AcyclicNetwork object representing the network to optimize.
        constraints : list[RegulationConstraint]
            A list of RegulationConstraint objects representing the space of 
            network parameters to optimize with respect to the targets defined 
            by **targetFunctions**.
        parameterMapping : list[ParameterMapping]
            A list of ParameterMapping objects representing the mapping of 
            regulation parameters in **constraints** to the actual parameters 
            in **model**. The length of the list equals to the length of 
            **constraints**.
        targetFunctions : list[object]
            A list of callable objects (wrapped functions) whose values shall 
            be minimized.

        Returns
        -------
        list[OptimizedRegulation]
            A list of OptimizedRegulation objects representing the optimized 
            parameters. The length of the list equals to the length of 
            **constraints**.
        """
        # Map parameters in the constraints to those in the network
        continuousParameterMapping = OrderedDict()
        discreteParameterMappings = [OrderedDict() 
                                     for i in range(0, len(constraints))]
        isDiscrete = [isinstance(constraint.parameterSpace, 
                                 DiscreteRegulationParameterSpace) 
                      for constraint in constraints]
        for i, constraint in enumerate(constraints):
            mapping = parameterMapping[i]
            for j in range(0, constraint.parameterSpace.dimension):
                if j in mapping:
                    if isDiscrete[i]:
                        discreteParameterMappings[i][j] = mapping[j]
                    else:
                        continuousParameterMapping[(i, j)] = mapping[j]
        
        # Determine the initial values and ranges for continuous parameters
        initialContinuousParameters = \
            [geometricMean(constraints[i].parameterSpace.boundaries[j]) 
             for (i, j) in continuousParameterMapping.keys()]
        continuousParameterRanges = \
            [intersectRanges([constraints[i].parameterSpace.boundaries[j], 
                              *(X.toTuple() 
                                for X in constraints[i].parameterConstraints 
                                if X.index == j)]) 
             for (i, j) in continuousParameterMapping.keys()]
        if any(X is None for X in continuousParameterRanges):
            (i, j) = next(iter((i, j) for (i, j), Y in 
                               zip(continuousParameterMapping.keys(), 
                                   continuousParameterRanges) if Y is None))
            raise ParameterRangeEmptyException(
                            constraints[i].parameterSpace.dimensionNames[j], 
                            constraints[i].parameterSpace.name)
        
        # Determine the initial values and ranges for discrete parameters
        discreteParameterGroups = [[tuple(Z[j] for j in Y.keys()) 
                                    for Z in X.parameterSpace.values] 
                                   if len(Y) > 0 else [] 
                                   for X, Y in zip(constraints, 
                                                   discreteParameterMappings)]
        initialDiscreteParameters = [centroid(X) 
                                     for X in discreteParameterGroups]
        discreteParameterRanges = []
        for i, constraint in enumerate(constraints):
            parameterGroups = discreteParameterGroups[i]
            if len(parameterGroups) == 0:
                discreteParameterRanges.append([])
                continue
            parameterRanges = [(min(X[i] for X in parameterGroups), 
                                max(X[i] for X in parameterGroups))
                               for i in range(0, len(parameterGroups[0]))]
            for parameterConstraint in constraint.parameterConstraints:
                j = parameterConstraint.index
                newRange = intersectRange(parameterRanges[j], 
                                          (parameterConstraint.minValue, 
                                           parameterConstraint.maxValue))
                if newRange is None or \
                   not any(newRange[0] <= X <= newRange[1] 
                           for X in constraint.parameterSpace.values[j]):
                    raise ParameterRangeEmptyException(
                                constraint.parameterSpace.name, 
                                constraint.parameterSpace.dimensionNames[j])
                parameterRanges[j] = newRange
            discreteParameterRanges.append(parameterRanges)
            discreteParameterGroups[i] = [X for X in parameterGroups 
                                          if all(Z[0] <= Y <= Z[1] for Y, Z in 
                                                 zip(X, parameterRanges))]
            if len(discreteParameterGroups[i]) == 0:
                raise ParameterRangeEmptyException(constraint.parameterSpace.
                                                   name)
        
        # Optimize the discrete parameters group-by-group
        continuousParameters = initialContinuousParameters
        discreteParameters = initialDiscreteParameters
        groupIndexes = [i for i, X in enumerate(discreteParameterMappings) 
                        if len(X) > 0]
        groupIndexes = sorted(groupIndexes, 
                              key = lambda i:len(discreteParameterGroups[i]) / 
                                             len(discreteParameterMappings[i]))
        oldGroupIndexes = groupIndexes.copy()
        while len(groupIndexes) > 0:
            # Update the clusters around the current group of parameters
            if self.debugOutput:
                print('Optimizing discrete parameter clusters for groups '
                      '{}...'.format(groupIndexes))
            initialContinuousParameters = continuousParameters
            discreteParameterClusters = \
                self.optimizeClusters(model, 
                                      [discreteParameterGroups[i] 
                                       for i in groupIndexes], 
                                      continuousParameterMapping.values(), 
                                      [discreteParameterMappings[i].values()  
                                       for i in groupIndexes], 
                                      initialContinuousParameters, 
                                      [discreteParameters[i] 
                                       for i in groupIndexes], 
                                      continuousParameterRanges, 
                                      [discreteParameterRanges[i] 
                                       for i in groupIndexes], 
                                      targetFunctions)
            
            # Pick a discrete parameter group to optimize
            oldLoss = math.inf
            clusterIndex = None
            i = groupIndexes.pop(0)
            clusterIndexes = discreteParameterClusters.pop(0)
            if self.debugOutput:
                print('Optimizing the parameter group {}:'.format(i))
            for j in clusterIndexes:
                self.updateModel(model, discreteParameterGroups[i][j], 
                                 discreteParameterMappings[i].values())
                loss, optimizedParameters = \
                    self.optimizeOnce(model, 
                                      continuousParameterMapping.values(),
                                      initialContinuousParameters, 
                                      continuousParameterRanges, 
                                      targetFunctions)
                if self.debugOutput:
                    print('  Loss {} with parameter {}'.
                          format(loss, discreteParameterGroups[i][j]))
                if loss < oldLoss:
                    continuousParameters = optimizedParameters
                    clusterIndex = j
                    oldLoss = loss
            if clusterIndex is not None:
                if self.debugOutput:
                    print('  Best parameter found for group {} with loss {}.'.
                          format(i, oldLoss))
                discreteParameters[i] = \
                    discreteParameterGroups[i][clusterIndex]
                oldGroupIndexes = groupIndexes.copy()
            else:
                if self.debugOutput:
                    print('  Optimization failed for group {}.'.format(i))
                groupIndexes.append(i)
                discreteParameterClusters.append(clusterIndexes)
                if groupIndexes == oldGroupIndexes:
                    spaceName = ','.join('"{}"'.format(constraints[i].
                                                       parameterSpace.name) 
                                         for i in groupIndexes)
                    raise ParameterNotConvergedException(spaceName)
            self.updateModel(model, continuousParameters, 
                             continuousParameterMapping.values())
            self.updateModel(model, discreteParameters[i], 
                             discreteParameterMappings[i].values())
        
        # Assemble the optimization result
        regulations = []
        for i, constraint in enumerate(constraints):
            if isDiscrete[i]:
                parameters = [None if X is None else model.getParameter(X) 
                              for X in discreteParameterMappings[i].values()]
                matchedIndexes = [j for j, X in 
                                  enumerate(constraint.parameterSpace.values) 
                                  if all(Y for Y, Z in zip(X, parameters)
                                         if Z is not None)]
                j = matchedIndexes[0]
                ID = constraint.parameterSpace.valueIDs[j]
                parameters = [Parameter(index = k, 
                                        name = constraint.parameterSpace.
                                               dimensionNames[k], 
                                        value = constraint.parameterSpace.
                                                values[j][k] if X is None 
                                                else X) 
                              for k, X in enumerate(parameters)]
            else:
                parameters = [Parameter(index = k, 
                                        name = constraint.parameterSpace.
                                               dimensionNames[k], 
                                        value = constraint.parameterSpace.
                                                boundaries[k][0] if X is None 
                                                else model.getParameter(X)) 
                              for (j, k), X in 
                                  continuousParameterMapping.items() if i == j]
                ID = ''
            regulations.append(OptimizedRegulation(constraint.sourceIndex, 
                                                   constraint.targetIndex,
                                                   constraint.regulationType, 
                                                   parameters, ID))
        return regulations
