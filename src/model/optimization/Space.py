#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 16:53:54 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class BaseSpace:
    """
    The base class for optimization space classes.
    """
    def __init__(self, name = ''):
        """
        Initialize a BaseSpace object.

        Parameters
        ----------
        name : str, optional
            The name of the space. The default is an empty string.
        
        Returns
        -------
        None.
        """
        self.name = name

class ParameterSpace(BaseSpace):
    """
    The base class for parameter space classes.
    """
    def __init__(self, name = '', minValue = 0, maxValue = 0):
        """
        Initialize a ParameterSpace object.

        Parameters
        ----------
        name : str, optional
            The name of the space. The default is an empty string.
        minValue : int or float, optional
            The minimum possible value in the space. The default is 0.
        maxValue : int or float, optional
            The maximum possible value in the space. The default is 0.

        Returns
        -------
        None.
        """
        super().__init__(name)
        self.minValue = minValue
        self.maxValue = maxValue

class RegulationParameterSpace(BaseSpace):
    """
    The class for parameter spaces.
    """
    def __init__(self, ID: int, regulationType: str, name = '', source = ''):
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
        source : str, optional
            A string representing the source of the space. 
            The default is empty string.

        Returns
        -------
        None.
        """
        super().__init__(name)
        self.ID = ID
        self.regulationType = regulationType
        self.source = source
        self.parameterList = []

class TargetSpace(BaseSpace):
    """
    The base class for optimization target classes.
    """
    def __init__(self, ID: int, variableCount: int, name = '', 
                 description = ''):
        """
        Initialize a TargetSpace object.

        Parameters
        ----------
        ID : int
            A integer representing the identity of the space.
        variableCount : int
            The number of variables of the function object.
        name : str
            The name of the target. 
            The default is an empty string.
        descrption : str, optional
            A string representing the description of the target. 
            The default is an empty string.

        Returns
        -------
        None.
        """
        super().__init__(name)
        self.ID = ID
        self.variableCount = variableCount
        self.description = description
