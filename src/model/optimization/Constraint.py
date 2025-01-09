#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 19:30:38 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.optimization.Network import Edge
from model.optimization.ParameterSpace import RegulationParameterSpace
from model.optimization.Target import BaseTarget


class ParameterConstraint:
    """
    The container class for constraints of parameters.
    """
    def __init__(self, index: int, minValue: float, maxValue: float):
        """
        Initialize a ParameterConstraint object.

        Parameters
        ----------
        index : int
            The index of the parameter.
        minValue : float
            The lower bound of the parameter.
        maxValue : float
            The upper bound of the parameter.

        Returns
        -------
        None.
        """
        self.index = index
        self.minValue = minValue
        self.maxValue = maxValue
    
    def toTuple(self) -> tuple:
        """
        Get a tuple reprsentation of the constraint.

        Returns
        -------
        tuple
            A tuple of (float, float) representing the lower and upper 
            boundary of the parameter.
        """
        return (self.minValue, self.maxValue)

class RegulationConstraint(Edge):
    """
    The container class for constraints of regulations.
    """
    def __init__(self, sourceIndex: int, targetIndex: int, regulationType: str,
                 parameterSpace: RegulationParameterSpace, 
                 parameterConstraints = None):
        """
        Initialize a RegulationConstraint object.

        Parameters
        ----------
        sourceIndex : int
            An integer indicating the index of the source node connected by 
            the edge.
        targetIndex : int
            An integer indicating the index of the target node connected by 
            the edge.
        regulationType : str
            A string representing the type of the regulation represented by 
            the edge.
        parameterSpace : RegulationParameterSpace
            A RegulationParameterSpace object representing the parameter space 
            of the regulation.
        parameterConstraints : list[ParameterConstraint] or NoneType, optional
            A list of ParameterConstraint objects representing the extra 
            constraint on each component parameter, or None if no extra 
            constraint shall be applied. 
            The default is None.

        Returns
        -------
        None.
        """
        super().__init__(sourceIndex, targetIndex, regulationType)
        self.parameterSpace = parameterSpace
        self.parameterConstraints = parameterConstraints or []

class TargetConstraint:
    """
    The container class for constraints of targets.
    """
    def __init__(self, nodeIndexes: list[int], space: BaseTarget, 
                 valueRanges = None):
        """
        Initialize a TargetConstraint object.

        Parameters
        ----------
        nodeIndexes : list[int]
            A list of integers representing the index of nodes involved in 
            the target evaluation.
        space : TargetSpace
            A TargetSpace object representing the target to evaluate.
        valueRanges : list[tuple] or NoneType, optional
            A list of tuples of (float, float) representing the lower and 
            upper boundary for the value of each specified node, or None if 
            the default boundaries shall be used. The length of the list must 
            equal to the length of **nodeIndexes**.
            The default is None.

        Returns
        -------
        None.
        """
        self.nodeIndexes = nodeIndexes
        self.space = space
        self.valueRanges = valueRanges or [None] * len(nodeIndexes)
