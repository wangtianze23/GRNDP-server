#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 09:07:50 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import math
from model.evaluation.Functional import BaseFunctional, JointFunctional


class BaseOptimizationLoss:
    """
    The base class for optimization loss classes.
    """
    def __init__(self, functional: BaseFunctional):
        """
        Initialize a BaseOptimizationLoss object.

        Parameters
        ----------
        functional : BaseFunctional
            A BaseFunctional object representing the functional used to  
            evaluate the optimization loss on a given input function.

        Returns
        -------
        None.
        """
        self.functional = functional
    
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
        return self.functional(function)

class MSEOptimizationLoss(BaseOptimizationLoss):
    """
    The class for optimization losses with the mean squared error (MSE) metric.
    """
    def __init__(self, functional: BaseFunctional):
        """
        Initialize a MSEOptimizationLoss object.

        Parameters
        ----------
        functional : BaseFunctional
            A BaseFunctional object representing the functional used to  
            evaluate the optimization loss on a given input function.

        Returns
        -------
        None.
        """
        super().__init__(functional)
        self.expectedValue = 0
    
    def setExpectedValue(self, expectedValue: float):
        """
        Set the expected value of a component for optimization.

        Parameters
        ----------
        expectedValue : int or float
            A numeric value representing the expected value of the evaluated 
            functional.

        Returns
        -------
        None.
        """
        self.expectedValue = expectedValue
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseOptimizationLoss.__call__().
        """
        return (super().__call__(function) - self.expectedValue) ** 2

class CompoundOptimizationLoss(BaseOptimizationLoss):
    """
    The class for compound optimization losses.
    """
    def __init__(self, components: list[BaseOptimizationLoss], 
                 jointFunctional: JointFunctional = None, 
                 reduction: object = None):
        """
        Initialize a CompoundOptimizationLoss object.

        Parameters
        ----------
        components : list[BaseOptimizationLoss]
            A list of BaseOptimizationLoss representing the component 
            losses to evaluate.
        jointFunctional : JointFunctional or NoneType, optional
            A JointFunctional object used to associate the component 
            functionals for joint evaluation, or None if the component 
            functional shall be evaluated separately.
            The default is None.
        reduction : object, optional
            A callable object to reduce the component losses into a scalar 
            value, or None if the default reduction method (i.e. production) 
            shall be used.
            The default is None.

        Returns
        -------
        None.
        """
        self.components = components
        self.jointFunctional = jointFunctional
        self.reduction = reduction or math.prod
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseOptimizationLoss.__call__().
        """
        if self.jointFunctional is not None:
            self.jointFunctional.prepare(function)
        values = [X(function) for X in self.components]
        return self.reduction(X for X in values if math.isfinite(X))
