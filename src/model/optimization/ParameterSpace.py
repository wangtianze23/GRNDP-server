#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 16:53:54 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import math


class ParameterSpace:
    """
    The base class for parameter space classes.
    """
    def __init__(self, name = '', dimension = 1):
        """
        Initialize a ParameterSpace object.

        Parameters
        ----------
        name : str, optional
            The name of the space. The default is an empty string.
        dimension : int, optional
            An integer greater than 0 indicating the number of components 
            (dimensions) of the parameter space. 
            The default is 1.

        Returns
        -------
        None.
        """
        self.name = name
        self.dimension = dimension

class DiscreteSpace:
    """
    The mixin class for discrete parameter space classes.
    """
    def __contains__(self, value: list) -> bool:
        """
        Check if a vector value exists in the space.

        Parameters
        ----------
        value : list
            A list of numeric values representing a vector.

        Returns
        -------
        bool
            Whether the specified vector value exists in the space.
        """
        raise NotImplementedError(DiscreteSpace.__contains__)
    
    def __getitem__(self, index: int) -> float:
        """
        Get a parameter by its index.

        Parameters
        ----------
        index : int
            The index of a parameter.

        Returns
        -------
        float
            The value of the specified parameter.
        """
        raise NotImplementedError(DiscreteSpace.__getiem__)
    
    def __len__(self) -> int:
        """
        Get the number of parameters in the space.

        Returns
        -------
        int
            The total number of parameters in the space.
        """
        raise NotImplementedError(DiscreteSpace.__len__)

class RegulationParameterSpace(ParameterSpace):
    """
    The class for regulation parameter spaces.
    """
    def __init__(self, ID: int, regulationType: str, name = '', dimension = 1, 
                 dimensionNames = None, boundaries = None, source = ''):
        """
        Initialize a RegulationParameterSpace object.

        Parameters
        ----------
        ID : int
            A integer representing the identity of the space.
        regulationType : str
            A string of either 'activation' or 'repression' indicating 
            the type of the regulation.
        name : str, optional
            The name of the space. The default is an empty string.
        dimension : int, optional
            An integer greater than 0 indicating the number of components 
            (dimensions) of the parameter space. 
            The default is 1.
        dimensionNames : list[str] or NoneType, optional
            A list of string representing the name of each components of 
            the parameter space, or None if no names are specified. The length 
            of the list must equal to **dimension**.
            The default is None.
        boundaries : list[tuple] or NoneType, optional
            A list of tuples of (float, float) representing the lower and 
            upper boundary of each components of the parameter space, or None 
            if no boundaries are specified. The length of the list must equal 
            to **dimension**.
            The default is None.
        source : str, optional
            A string representing the source of the space. 
            The default is empty string.

        Returns
        -------
        None.
        """
        super().__init__(name, dimension)
        self.ID = ID
        self.regulationType = regulationType
        self.dimensionNames = dimensionNames or [''] * dimension
        self.boundaries = boundaries or [(-math.inf,math.inf)] * dimension
        self.source = source

class DiscreteRegulationParameterSpace(DiscreteSpace,RegulationParameterSpace):
    """
    The class for discrete regulation parameter spaces.
    """
    def __init__(self, ID: int, regulationType: str, name = '', 
                 dimension = 1, dimensionNames = None, source = '', 
                 values = None, valueIDs = None):
        """
        Initialize a DiscreteRegulationParameterSpace object.

        Parameters
        ----------
        ID : int
            A integer representing the identity of the space.
        regulationType : str
            A string of either 'activation' or 'repression' indicating 
            the type of the regulation.
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
            A list of tuple of numeric values representing the possible 
            choices of parameter values in the space, or None if the values 
            are not defined.
            The default is None.
        valueIDs : list[str] or NoneType, optional
            A list of strings representing the identity of each possible 
            choice of parameter values in the space when **values** is not 
            None, or None when **values** is None or the items in **values** 
            have no identity.
            The default is None.

        Returns
        -------
        None.
        """
        super().__init__(ID, regulationType, name, dimension, dimensionNames, 
                         source)
        self.values = values
        self.valueIDs = valueIDs
    
    def __contains__(self, item: list) -> bool:
        """
        Overrides DiscreteSpace.__getitem__().
        """
        if self.values is not None:
            return item in self.values
        return False
    
    def __getitem__(self, index: int) -> float:
        """
        Overrides DiscreteSpace.__getitem__().
        """
        if self.values is None:
            raise ValueError('no values defined in the space')
        if index < -len(self.values) or index >= len(self.values):
            raise IndexError('value index out of range')
        return self.values[index]
    
    def __len__(self) -> int:
        """
        Overrides DiscreteSpace.__len__().
        """
        if self.values is None:
            raise ValueError('no values defined in the space')
        return len(self.values)
