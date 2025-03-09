#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 09:07:50 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import math
from model.evaluation.Functional import BaseFunctional


class BaseOptimizationLoss:
    """
    The base class for optimization loss classes.
    """
    def __init__(self, components: list[BaseFunctional]):
        """
        Initialize a BaseOptimizationLoss object.

        Parameters
        ----------
        components : list[BaseFunctional]
            A list of BaseFunctional objects representing the components 
            (subtargets) of the optimization loss.

        Returns
        -------
        None.
        """
        self.components = components
        self.reduction = sum
        self.ignoreInvalid = True
    
    def __call__(self, function: object) -> float:
        """
        Calculate the optimization loss.
        
        Parameters
        ----------
        function : object
            A callable object representing the function to be evaluated 
            by each component.
            
        Returns
        -------
        float
            A float number representing the current loss.
        """
        if len(self.components) == 1:
            return self.components[0](function)
        return self.reduction([F(function) for F in self.components])
    
    def setComponent(self, index: int, functional: BaseFunctional):
        """
        Set the component of the optimization loss.

        Parameters
        ----------
        index : int
            An integer indicating the index of the component.
        functional : BaseFunctional
            A BaseFunctional object representing the component to calculate.

        Returns
        -------
        None.
        """
        if index < len(self.components):
            self.components[index] = functional

class MSEOptimizationLoss(BaseOptimizationLoss):
    """
    The class for optimization losses with the mean squared error (MSE) metric.
    """
    def __init__(self, components: list[BaseFunctional]):
        """
        Initialize a MSEOptimizationLoss object.

        Parameters
        ----------
        components : list[BaseFunctional]
            A list of BaseFunctional objects representing the components 
            (subtargets) of the optimization loss.

        Returns
        -------
        None.
        """
        super().__init__(components)
        self.expectedValues = [None] * len(components)
    
    def setExpectedValue(self, index: int, expectedValue: float):
        """
        Set the expected value of a component for optimization.

        Parameters
        ----------
        index : int
            An integer indicating the index of the component.
        expectedValue : int or float
            A numeric value representing the expected value of a component.

        Returns
        -------
        None.
        """
        if index < len(self.expectedValues):
            self.expectedValues[index] = expectedValue
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseOptimizationLoss.__call__().
        """
        targetValues = (F(function) for F in self.components)
        return self.reduction([(X - (Y or 0)) ** 2 
                               for X,Y in zip(targetValues,self.expectedValues)
                               if math.isfinite(X)])
