#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 09:22:35 2026
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.simulation.DynamicNetwork import BaseDynamicNetwork
from model.simulation.Network import NetworkPath
from .Loss import BaseOptimizationLoss


class BaseInputFunction:
    """
    The class representing a component function in an optimization target.
    """
    def __call__(self, inputVariables: list[float] = None) -> float:
        """
        Calculate the function value (output) from a series of input variables.

        Parameters
        ----------
        inputVariables : list[float] or NoneType, optional
            A list of float values representing the input (independent) 
            variables, or None if no input is required.
            The default is None.

        Returns
        -------
        float
            The calculated output (dependent) value.
        """
        raise NotImplementedError(BaseInputFunction.__call__)
    
    def clone(self) -> "BaseInputFunction":
        """
        Create a copy of the input function.

        Returns
        -------
        BaseInputFunction
            A new BaseInputFunction object.
        """
        raise NotImplementedError(BaseInputFunction.clone)

class DynamicNetworkSimulationInput(BaseInputFunction):
    """
    The class evaluating the simulated result of a dynamic network as 
    a component in an optimization target.
    """
    def __init__(self, network: BaseDynamicNetwork, nodeIndex: int, 
                 initialValues: list[float], timeSpan: float, 
                 trajectoryCount: int):
        """
        Initialize a DynamicNetworkSimulationInput object.

        Parameters
        ----------
        network : BaseDynamicNetwork
            A BaseDynamicNetwork object used to run simulation.
        nodeIndex : int
            An integer representing the index of node in **network** whose 
            value are to evaluate.
        initialValues: list[float]
            A list of integer or float values representing the initial value 
            for all nodes in **network**.
        timeSpan : int or float
            A numeric value indicating the span of time for simulation.
        trajectoryCount : int
            An integer indicating the number of trajectories.

        Returns
        -------
        None.
        """
        self.network = network
        self.nodeIndex = nodeIndex
        self.initialValues = initialValues
        self.timeSpan = timeSpan
        self.trajectoryCount = trajectoryCount
    
    def __call__(self, inputVariables: list[float] = None) -> float:
        """
        Overrides BaseInputFunction.__call__().
        """
        output = self.network.evolve(self.initialValues, self.timeSpan, 
                                     self.trajectoryCount)
        return [X[self.nodeIndex] for X in output]
    
    def clone(self) -> "DynamicNetworkSimulationInput":
        """
        Overrides BaseInputFunction.clone().
        """
        return DynamicNetworkSimulationInput(self.network, self.nodeIndex, 
                                             self.initialValues.copy(), 
                                             self.timeSpan, 
                                             self.trajectoryCount)

class NetworkPathInput(BaseInputFunction):
    """
    The class evaluating the output of a network path as a component  
    in an optimization target.
    """
    def __init__(self, path: NetworkPath):
        """
        Initialize a NetworkPathInput object.

        Parameters
        ----------
        path : NetworkPath
            A NetworkPath object based on which the output is evaluated.

        Returns
        -------
        None.
        """
        self.path = path
    
    def __call__(self, inputVariables: list[float]) -> float:
        """
        Overrides BaseInputFunction.__call__().
        """
        return self.path(inputVariables[0])
    
    def clone(self) -> "NetworkPathInput":
        """
        Overrides BaseInputFunction.clone().
        """
        return NetworkPathInput(self.path.clone())

class OptimizationLossTarget:
    """
    The class representing an optimization target as the value of 
    a loss function.
    """
    def __init__(self, inputFunction: BaseInputFunction, 
                 lossFunction: BaseOptimizationLoss):
        """
        Initialize an OptimizationLossTarget object.

        Parameters
        ----------
        inputFunction : object
            A BaseInputFunction object based on which an optimization loss 
            is calculated.
        lossFunction : BaseOptimizationLoss
            A BaseOptimizationLoss object representing a loss function(al) 
            used to evaluate the actual loss value.

        Returns
        -------
        None.
        """
        self.inputFunction = inputFunction
        self.lossFunction = lossFunction
    
    def __call__(self) -> float:
        """
        Evaluate the optimization loss.

        Returns
        -------
        float
            The loss value calculated on the specified input function 
            with respect to the specified loss function.
        """
        return self.lossFunction(self.inputFunction)
    
    def clone(self) -> "OptimizationLossTarget":
        """
        Create a copy of the target.

        Returns
        -------
        OptimizationLossTarget
            A new OptimizationLossTarget object.
        """
        return OptimizationLossTarget(self.inputFunction.clone(), 
                                      self.lossFunction)
