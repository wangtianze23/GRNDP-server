#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:05:03 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from collections import OrderedDict
import math
import multiprocessing
import scipy.optimize as Optimize
from infrastructure.math.number import centroid, geometricMean, kNN
from infrastructure.math.number import intersectRange, intersectRanges
from model.optimization.Constraint import RegulationConstraint
from model.optimization.Network import Parameter, OptimizedRegulation
from model.optimization.OptimizerException import \
    ParameterNotConvergedException, ParameterRangeEmptyException
from model.optimization.OptimizerTarget import \
    DynamicNetworkSimulationInput, NetworkPathInput, OptimizationLossTarget
from model.optimization.ParameterSpace import DiscreteRegulationParameterSpace
from model.optimization.RandomOptimizer import RandomBoundedStep
from model.simulation.Network import \
    NetworkParameterIndex, ParameterMapping, BaseNetwork
from model.simulation.DynamicNetwork import BaseDynamicNetwork


class BaseNetworkParameterOptimizer:
    """
    The base class for optimizing BaseNetwork objects.
    """
    def __init__(self):
        """
        Initialize a BaseNetworkParameterOptimizer object.

        Returns
        -------
        None.
        """
        self.debugOutput = False
        self.maxIteration = 10
        self.maxIteration2 = 20
        self.maxLocalSearches = 5
        self.maxProcess = -1
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
    def updateModel(model: BaseNetwork, parameters: list[float], 
                    parameterIndexes: list[NetworkParameterIndex]):
        """
        Update the parameter of a model.

        Parameters
        ----------
        model : BaseNetwork
            A BaseNetwork object representing the network to optimize.
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
    def lossFunction(model: BaseNetwork, parameters: list[float], 
                     parameterIndexes: list[NetworkParameterIndex], 
                     targetFunctions: list[OptimizationLossTarget]) -> float:
        """
        Calculate the optimization loss on a model and a list of targets.

        Parameters
        ----------
        model : BaseNetwork
            A BaseNetwork object representing the network to optimize.
        parameters: list[float]
            A list of numeric values representing the network parameters to 
            update before evaluating the targets.
        parameterIndexes : list[NetworkParameterIndex]
            A list of NetworkParameterIndex objects representing the index of 
            parameters in a network.
        targetFunctions : list[OptimizationLossTarget]
            A list of OptimizationLossTarget objects to evaluate after 
            the model has been updated.

        Returns
        -------
        float
            The optimization loss evaluated on the updated model.
        """
        if len(parameterIndexes) > 0:
            BaseNetworkParameterOptimizer.updateModel(model, parameters, 
                                                      parameterIndexes)
        return math.prod(X() for X in targetFunctions)
    
    def optimizeOnce(self, model: BaseNetwork, 
                     parameterIndexes: list[NetworkParameterIndex], 
                     initialParameters: list[float], 
                     parameterRanges: list[tuple[float]], 
                     targetFunctions: list[OptimizationLossTarget]) -> tuple:
        """
        Run a round of global optimization (minimization) of a list of targets 
        with respect to a given set of model parameters.

        Parameters
        ----------
        model : BaseNetwork
            A BaseNetwork object representing the network to optimize.
        parameterIndexes : list[NetworkParameterIndex]
            A list of NetworkParameterIndex objects representing the index of 
            parameters in a network to optimize.
        initialParameters : list[float]
            A list of numeric values representing the intial guess for each 
            parameter before optimization. The length of the list equals to 
            the length of **parameterIndexes**.
        parameterRanges : list[tuple[float]]
            A list of tuple of (float, float) representing the boundary for 
            each parameter during optimization. The length of the list equals 
            to the length of **parameterIndexes**.
        targetFunctions : list[OptimizationLossTarget]
            A list of OptimizationLossTarget objects whose evaluated values 
            shall be minimized.

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
        
        # Exclude fixed parameters
        freeParameterIndexes = [i for i, X in enumerate(parameterRanges) 
                                if min(X) < max(X)]
        initialParameters = [X if i in freeParameterIndexes 
                             else min(parameterRanges[i]) 
                             for i, X in enumerate(initialParameters)]
        if len(freeParameterIndexes) == 0:
            return (self.lossFunction(model, initialParameters, 
                                      parameterIndexes, targetFunctions), 
                    initialParameters)
        self.updateModel(model, initialParameters, parameterIndexes)
        freeParameters = [initialParameters[i] for i in freeParameterIndexes]
        parameterRanges = [parameterRanges[i] for i in freeParameterIndexes]
        parameterIndexes = [parameterIndexes[i] for i in freeParameterIndexes]
        
        # Determine the step size for updating parameters
        stepSizes = [(max(X) - min(X)) * self.relativeStepSize 
                     for X in parameterRanges]
        stepMaker = RandomBoundedStep(seed = self.seed, 
                                      maxStep = max(stepSizes), 
                                      stepBoundaries = [(-X, X) 
                                                        for X in stepSizes])
        
        # Global optimization
        result = Optimize.basinhopping(lambda X: 
                                       self.lossFunction(model, X, 
                                                         parameterIndexes, 
                                                         targetFunctions),
                                       freeParameters, 
                                       seed = self.seed, 
                                       niter = self.maxIteration, 
                                       take_step = stepMaker, 
                                       disp = self.debugOutput, 
                                       minimizer_kwargs = 
                                       {'method': 'Nelder-Mead', 
                                        'bounds': parameterRanges, 
                                        'options': 
                                        {'maxiter': self.maxLocalSearches, 
                                         'disp': self.debugOutput}})
        
        # Update the model with the optimized parameters
        self.updateModel(model, result['x'], parameterIndexes)
        
        # Return the optimization loss and the optimized parameters
        fittedParameters = initialParameters
        for i, X in zip(freeParameterIndexes, result['x']):
            fittedParameters[i] = X
        return (result['fun'], fittedParameters)
    
    def optimizeOnceWorker(self, model: BaseNetwork, 
                           fixedParameters: tuple[float], 
                           parameterIndexes: list[NetworkParameterIndex], 
                           initialParameters: list[float], 
                           parameterRanges: list[tuple[float]], 
                           targetFunctions: list[OptimizationLossTarget]) \
                          -> tuple:
        """
        The worker function capable of parallely running 
        **BaseNetworkParameterOptimizer.optimizeOnce**.

        Parameters
        ----------
        fixedParameters : tuple[float]
            A tuple of numeric values representing the list of parameters 
            fixed during optimization; for debug purpose only.
        ...
            See **BaseNetworkParameterOptimizer.optimizeOnce** for details 
            about other arguments.

        Returns
        -------
        tuple
            See **BaseNetworkParameterOptimizer.optimizeOnce** for details 
            about the return value.
        """
        result = self.optimizeOnce(model, parameterIndexes, initialParameters, 
                                   parameterRanges, targetFunctions)
        if self.debugOutput:
            print('  Loss {} with parameter {}'.
                  format(result[0], fixedParameters))
        return result
    
    def optimizeDiscreteGroup(self, model: BaseNetwork, 
                              discreteParameterGroup: list[tuple[float]], 
                              continuousParameterIndexes: 
                                  list[NetworkParameterIndex], 
                              discreteParameterIndexes: 
                                  list[NetworkParameterIndex], 
                              initialContinuousParameters: list[float], 
                              continuousParameterRanges: list[tuple[float]], 
                              targetFunctions: list[OptimizationLossTarget]) \
                             -> tuple:
        """
        Run global optimization (minimization) on a group of discrete 
        parameters combined with a common set of continuous parameters.

        Parameters
        ----------
        model : BaseNetwork
            A BaseNetwork object representing the network to optimize.
        discreteParameterGroup : list[tuple[float]]
            A list of tuples of float values representing a group of 
            discrete parameters to choose from. The length of the list equals 
            to the number of choices, and the length of the tuple equals to 
            the number of discrete parameter (i.e. dimension) in each group.
        continuousParameterIndexes : list[NetworkParameterIndex]
            A list of NetworkParameterIndex objects representing the index of 
            continuous parameters in a network to optimize.
        discreteParameterIndexes : list[NetworkParameterIndex]
            A list of NetworkParameterIndex objects representing the index of 
            discrete parameters in a network to optimize.
        initialContinuousParameters : list[float]
            A list of numeric values representing the intial guess for each 
            continuous parameter before optimization. The length of the list 
            equals to the length of **continuousParameterIndexes**.
        continuousParameterRanges : list[tuple[float]]
            A list of tuple of (float, float) representing the boundary for 
            each continuous parameter during optimization. The length of 
            the list equals to the length of **continuousParameterIndexes**.
        targetFunctions : list[OptimizationLossTarget]
            A list of OptimizationLossTarget objects whose evaluated values 
            shall be minimized.

        Returns
        -------
        tuple
            A tuple of the following items:
                - A list of numeric values indicating the optimized continuous 
                  parameters that (when combined with the optimized discrete 
                  parameter group) yields the lowest loss, or None if 
                  optimization failed.
                - An integer indicating the index of the optimal discrete 
                  parameter group that yields the lowest loss, or None if 
                  optimization failed.
                - A float indicating the minimized loss value.
        """
        # Duplicate the model and fill with different discrete parameters
        newModels = []
        for parameters in discreteParameterGroup:
            newModel = model.clone()
            self.updateModel(newModel, parameters, discreteParameterIndexes)
            newModels.append(newModel)
        
        # Duplicate also the target functions
        newTargetFunctions = []
        for newModel in newModels:
            functions = []
            for targetFunction in targetFunctions:
                newTargetFunction = targetFunction.clone()
                inputFunction = newTargetFunction.inputFunction
                if isinstance(inputFunction, DynamicNetworkSimulationInput):
                    inputFunction.network = newModel
                elif isinstance(inputFunction, NetworkPathInput):
                    inputFunction.path.setNetwork(newModel)
                functions.append(newTargetFunction)
            newTargetFunctions.append(functions)
            
        # Optimize the models parallelly using multiprocessing
        taskCount = len(discreteParameterGroup)
        workerCount = self.maxProcess
        if workerCount < 1:
            workerCount = multiprocessing.cpu_count()
        if workerCount > 1:
            workers = multiprocessing.Pool(workerCount)
            result = \
                workers.starmap(BaseNetworkParameterOptimizer.optimizeOnceWorker, 
                                zip([self] * taskCount, newModels, 
                                    discreteParameterGroup, 
                                    [continuousParameterIndexes] * taskCount, 
                                    [initialContinuousParameters]* taskCount, 
                                    [continuousParameterRanges] * taskCount, 
                                    newTargetFunctions))
        else:
            # No multiprocessing needed
            result = [self.optimizeOnceWorker(X, Y, continuousParameterIndexes,
                                              initialContinuousParameters, 
                                              continuousParameterRanges, Z)
                      for X, Y, Z in zip(newModels, discreteParameterGroup, 
                                         newTargetFunctions)]
        
        losses = [X[0] for X in result]
        minLoss = min(losses)
        if math.isinf(minLoss):
            return (None, math.inf, None)
        minLossIndex = losses.index(minLoss)
        return (result[minLossIndex][1], minLossIndex, minLoss)
    
    def optimizeClusters(self, model: BaseNetwork, 
                         discreteParameterGroups: list[list[tuple[float]]], 
                         continuousParameterIndexes: 
                             list[NetworkParameterIndex], 
                         discreteParameterIndexes: 
                             list[list[NetworkParameterIndex]], 
                         initialContinuousParameters: list[float], 
                         initialDiscreteParameters: list[list[float]],
                         continuousParameterRanges: list[tuple[float]], 
                         discreteParameterRanges: list[list[tuple[float]]], 
                         targetFunctions: list[OptimizationLossTarget]) \
                        -> list[list[tuple[float]]]:
        """
        Run global optimization (minimization) to find a stable cluster of 
        groups of discrete parameters.

        Parameters
        ----------
        model : BaseNetwork
            A BaseNetwork object representing the network to optimize.
        discreteParameterGroups : list[list[tuple[float]]]
            A list of lists of tuples of float values representing multiple 
            groups of discrete parameters to choose from. The length of 
            the outer list equals to the number of groups, the length of 
            the inner list to the number of choices for each group, and 
            the length of the tuple equals to the number of discrete parameter 
            (i.e. dimension) in each group.
        continuousParameterIndexes : list[NetworkParameterIndex]
            A list of NetworkParameterIndex objects representing the index of 
            continuous parameters in a network to optimize.
        discreteParameterIndexes : list[list[NetworkParameterIndex]]
            A list of lists of NetworkParameterIndex objects representing 
            the index of discrete parameters in a network to optimize for each 
            group. The length of the outer list equals to the number of 
            discrete parameter groups, and the length of the inner list equals 
            to the number of parameters in each group.
        initialContinuousParameters : list[float]
            A list of numeric values representing the intial guess for each 
            continuous parameter before optimization. The length of the list 
            equals to the length of **continuousParameterIndexes**.
        initialDiscreteParameters : list[list[float]]
            A list of lists of numeric values representing the intial guess 
            for each discrete parameter in each group before optimization. 
            The length of the outer list equals to the numer of discrete 
            parameter groups, and the length of the inner list equals to 
            the number of parameters in each group.
        continuousParameterRanges : list[tuple[float]]
            A list of tuple of (float, float) representing the boundary for 
            each continuous parameter during optimization. The length of 
            the list equals to the length of **continuousParameterIndexes**.
        discreteParameterRanges : list[list[tuple[float]]]
            A list of lists of tuple of (float, float) representing 
            the boundary for each discrete parameter in each group during 
            optimization. The length of the outer list equals to the numer of 
            discrete parameter groups, and the length of the inner list equals 
            to the number of parameters in each group.
        targetFunctions : list[OptimizationLossTarget]
            A list of OptimizationLossTarget objects whose evaluated values 
            shall be minimized.

        Returns
        -------
        list[list[tuple[float]]]
            A list of lists of tuples of numeric values representing 
            the optimized cluster of discrete parameter groups. The length of 
            the outer list equals to the number of groups, the length of 
            the inner list equals to the size of cluster for each group, and 
            the length of the tuple equals to the number of discrete parameter 
            (i.e. dimension) in each group.
        """
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
    
    def optimize(self, model: BaseNetwork, 
                 constraints: list[RegulationConstraint], 
                 parameterMapping: list[ParameterMapping], 
                 targetFunctions: list[OptimizationLossTarget]) \
                -> list[OptimizedRegulation]:
        """
        Optimize a model with a list of parameter constraints and targets.

        Parameters
        ----------
        model : BaseNetwork
            A BaseNetwork object representing the network to optimize.
        constraints : list[RegulationConstraint]
            A list of RegulationConstraint objects representing the space of 
            network parameters to optimize with respect to the targets defined 
            by **targetFunctions**.
        parameterMapping : list[ParameterMapping]
            A list of ParameterMapping objects representing the mapping of 
            regulation parameters in **constraints** to the actual parameters 
            in **model**. The length of the list equals to the length of 
            **constraints**.
        targetFunctions : list[OptimizationLossTarget]
            A list of OptimizationLossTarget objects whose evaluated values 
            shall be minimized.

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
                   not any(newRange[0] <= X[j] <= newRange[1] 
                           for X in constraint.parameterSpace.values):
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
                                      list(continuousParameterMapping.
                                           values()), 
                                      [list(discreteParameterMappings[i].
                                            values()) 
                                       for i in groupIndexes], 
                                      initialContinuousParameters, 
                                      [discreteParameters[i] 
                                       for i in groupIndexes], 
                                      continuousParameterRanges, 
                                      [discreteParameterRanges[i] 
                                       for i in groupIndexes], 
                                      targetFunctions)
            
            # Pick a discrete parameter group to optimize
            clusterIndex = None
            i = groupIndexes.pop(0)
            clusterIndexes = discreteParameterClusters.pop(0)
            if self.debugOutput:
                print('Optimizing the parameter group {}:'.format(i))
            optimizedParameters, clusterIndex, loss = \
                self.optimizeDiscreteGroup(model, discreteParameterGroups[i], 
                                           list(continuousParameterMapping.
                                                values()), 
                                           list(discreteParameterMappings[i].
                                                values()), 
                                           initialContinuousParameters, 
                                           continuousParameterRanges, 
                                           targetFunctions)
            if clusterIndex is not None:
                if self.debugOutput:
                    print('  Best parameter found for group {} with loss {}.'.
                          format(i, loss))
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
                             list(continuousParameterMapping.values()))
            self.updateModel(model, discreteParameters[i], 
                             list(discreteParameterMappings[i].values()))
        
        # Assemble the optimization result
        regulations = []
        for i, constraint in enumerate(constraints):
            if isDiscrete[i]:
                parameters = [None if X is None else model.getParameter(X) 
                              for X in discreteParameterMappings[i].values()]
                matchedIndexes = [j for j, X in 
                                  enumerate(constraint.parameterSpace.values) 
                                  if all(Y == Z for Y, Z in zip(X, parameters)
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
                defaultParameters = [X[0] for X in 
                                     constraint.parameterSpace.boundaries]
                parameters = [Parameter(index = k, 
                                        name = constraint.parameterSpace.
                                               dimensionNames[k], 
                                        value = defaultParameters[k] 
                                                if X is None 
                                                else (model.getParameter(X) or 
                                                     defaultParameters[k])) 
                              for (j, k), X in 
                                  continuousParameterMapping.items() if i == j]
                ID = ''
            regulations.append(OptimizedRegulation(constraint.sourceIndex, 
                                                   constraint.targetIndex,
                                                   constraint.regulationType, 
                                                   parameters, ID))
        return regulations

class DynamicNetworkParameterOptimizer(BaseNetworkParameterOptimizer):
    """
    The base class for optimizing BaseDynamicNetwork objects.
    """
    def __init__(self):
        """
        Initialize a DynamicNetworkParameterOptimizer object.

        Returns
        -------
        None.
        """
        super().__init__()
        self.maxIteration = 5
        self.maxIteration2 = 10
        self.maxLocalSearches = 1
        self.neighbourCount = 10
    
    def optimizeOnce(self, model: BaseDynamicNetwork, 
                     parameterIndexes: list[NetworkParameterIndex], 
                     initialParameters: list[float], 
                     parameterRanges: list[tuple], 
                     targetFunctions: list[object]) -> tuple:
        """
        Run a round of global optimization (minimization) of a list of targets 
        with respect to a given set of model parameters.

        Parameters
        ----------
        model : BaseDynamicNetwork
            A BaseDynamicNetwork object representing the network to optimize.
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
        
        # Exclude fixed parameters
        freeParameterIndexes = [i for i, X in enumerate(parameterRanges) 
                                if min(X) < max(X)]
        initialParameters = [X if i in freeParameterIndexes 
                             else min(parameterRanges[i]) 
                             for i, X in enumerate(initialParameters)]
        if len(freeParameterIndexes) == 0:
            return (self.lossFunction(model, initialParameters, 
                                      parameterIndexes, targetFunctions), 
                    initialParameters)
        self.updateModel(model, initialParameters, parameterIndexes)
        freeParameters = [initialParameters[i] for i in freeParameterIndexes]
        parameterRanges = [parameterRanges[i] for i in freeParameterIndexes]
        parameterIndexes = [parameterIndexes[i] for i in freeParameterIndexes]
        
        # Global optimization
        try:
            result = Optimize.dual_annealing(lambda X: 
                                             self.lossFunction(
                                                 model, X, parameterIndexes, 
                                                 targetFunctions),
                                             bounds = parameterRanges, 
                                             x0 = freeParameters, 
                                             seed = self.seed, 
                                             maxiter = self.maxIteration, 
                                             no_local_search = 
                                             (self.maxLocalSearches < 2), 
                                             minimizer_kwargs = 
                                             {'method': 'Nelder-Mead', 
                                              'options': 
                                              {'maxiter':self.maxLocalSearches, 
                                               'disp': self.debugOutput}})
        except ValueError:
            return (math.inf, initialParameters)
        
        # Update the model with the optimized parameters
        self.updateModel(model, result['x'], parameterIndexes)
        
        # Return the optimization loss and the optimized parameters
        fittedParameters = initialParameters
        for i, X in zip(freeParameterIndexes, result['x']):
            fittedParameters[i] = X
        return (result['fun'], fittedParameters)
