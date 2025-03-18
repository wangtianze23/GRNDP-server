#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:36:59 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.optimization.ParameterSpace import RegulationParameterSpace


class GenerativeSpace:
    """
    The mixin class for generative parameter spaces.
    """
    def feasible(value: tuple) -> bool:
        """
        Check if a vector value can be generated.

        Parameters
        ----------
        value : list
            A tuple of numeric values representing a vector.

        Returns
        -------
        bool
            Whether the specified vector value can be generated.
        """
        raise NotImplementedError(GenerativeSpace.feasible)

class GenerativeRegulationParameterSpace(GenerativeSpace, 
                                         RegulationParameterSpace):
    """
    The class for regulation parameters in a generative space.
    """
    def __init__(self, ID: int, regulationType: str, name = '', 
                 dimension = 1, dimensionNames = None, source = '', 
                 values = None, valueIDs = None):
        """
        Initialize a GenerativeRegulationParameterSpace object.

        Parameters
        ----------
        ID : int
            A integer representing the identity of the space.
        regulationType : str
            A string of either 'activation', 'repression' or 'constant' 
            indicating the type of the regulation.
        name : str, optional
            The name of the space. The default is an empty string.
        dimension : int, optional
            An integer greater than 0 indicating the number of components 
            (dimensions) of the parameter space. 
            The default is 1.
        dimensionNames : list[str] or NoneType, optional
            A list of string representing the name of each components of 
            the parameter space, or None if no names are specified.
            The default is None.
        source : str, optional
            A string representing the source of the space. 
            The default is empty string.
        values : list[tuple] or NoneType, optional
            A list of tuple of numeric values representing the feasible  
            parameter values in the space, or None if all values are feasible.
            The default is None.
        valueIDs : list[str] or NoneType, optional
            A list of strings representing the identity of each feasible 
            parameter value in the space when **values** is not None, or 
            None when **values** is None or the items in **values** have no 
            identity.
            The default is None.

        Returns
        -------
        None.
        """
        super().__init__(ID, regulationType, name, dimension, dimensionNames, 
                         source)
        self.values = values
        self.valueIDs = valueIDs
    
    def feasible(self, value: tuple) -> bool:
        """
        Overrides GenerativeSpace.feasible().
        """
        if self.values is not None:
            return value in self.values
        return all(True if Y is None else X in Y 
                   for X, Y in zip(value, self.boundaries))
