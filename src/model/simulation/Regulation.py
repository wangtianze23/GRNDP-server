#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 20:55:46 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class BaseRegulation:
    """
    The base class for modeling regulatory interactions among genes.
    """
    parameterIndexes = {}
    
    @classmethod
    def parameterCount(ClassType) -> int:
        """
        Get the number of parameter associated with the regulation.

        Returns
        -------
        int
            The number of parameter.
        """
        return len(ClassType.parameterIndexes)
    
    def parameter(self, index: int) -> float:
        """
        Get the value of a parameter associated with the regulation.

        Parameters
        ----------
        index : int
            An integer representing the index of the parameter.

        Returns
        -------
        float
            The value of the specified parameter.
        """
        raise NotImplementedError(BaseRegulation.parameter)
    
    def setParameter(self, index: int, parameter):
        """
        Set the value of a parameter associated with the regulation.

        Parameters
        ----------
        index : int
            An integer representing the index of the parameter.
        parameter : TYPE
            A numeric value representing the value of the parameter.

        Returns
        -------
        None.
        """
        raise NotImplementedError(BaseRegulation.setParameter)

    def __call__(self, X: list) -> float:
        """
        Get the effect of the regulation with a vector of input values.

        Parameters
        ----------
        X : list
            A list of numeric values representing the input to the regulation.

        Returns
        -------
        float
            A numeric value representing the effect (output) of the regulation.
        """
        raise NotImplementedError(BaseRegulation.__call__)

class ConstantRegulation(BaseRegulation):
    """
    The class for regulations of constant output.
    """
    parameterIndexes = {
        0: 'y'
    }
    
    def __init__(self, y: float):
        """
        Initialize a ConstantRegulation object.

        Parameters
        ----------
        y : float
            The constant value of the effect of the regulation.

        Returns
        -------
        None.
        """
        self.y = y
    
    def parameter(self, index: int) -> float:
        """
        Overrides BaseRegulation.parameter().
        """
        if index == 0:
            return self.y
        return 0
    
    def setParameter(self, index: int, parameter: float):
        """
        Overrides BaseRegulation.setParameter().
        """
        if index == 0:
            self.y = parameter

    def __call__(self, X: list) -> float:
        """
        Overrides BaseRegulation.__call__().
        """
        return self.y
