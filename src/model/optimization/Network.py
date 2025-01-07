#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 19:08:21 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class Node:
    """
    The container class for nodes in a network.
    """
    def __init__(self, index: int, name: str, entityType: str):
        """
        Initialize a Node object.

        Parameters
        ----------
        index : int
            An integer indicating the index of the node.
        name : str
            The name of the node.
        entityType : str
            A string representing the type of the physical entity represented 
            by the node.

        Returns
        -------
        None.
        """
        self.index = index
        self.name = name
        self.entityType = entityType

class Path:
    """
    The container class for paths in a network.
    """
    def __init__(self, sourceIndex: int, targetIndex: int):
        """
        Initialize a Path object.

        Parameters
        ----------
        sourceIndex : int
            An integer indicating the index of the source node connected by 
            the edge.
        targetIndex : int
            An integer indicating the index of the target node connected by 
            the edge.

        Returns
        -------
        None.
        """
        self.sourceIndex = sourceIndex
        self.targetIndex = targetIndex

class Edge(Path):
    """
    The container class for edges in a network.
    """
    def __init__(self, sourceIndex: int, targetIndex: int, regulationType:str):
        """
        Initialize an Edge object.

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

        Returns
        -------
        None.
        """
        super().__init__(sourceIndex, targetIndex)
        self.regulationType = regulationType

class Parameter:
    """
    The container class for a parameter of an edge in a network.
    """
    def __init__(self, index: int, name: str, value: float):
        """
        Initialize a Parameter object.

        Parameters
        ----------
        index : int
            An integer indicating the index of the parameter.
        name : str
            The name of the parameter.
        value : float
            A numeric value representing the value of the parameter.

        Returns
        -------
        None.
        """
        self.index = index
        self.name = name
        self.value = value

class Regulation(Edge):
    """
    The container class for parameters of an edge in a network.
    """
    def __init__(self, sourceIndex: int, targetIndex: int, regulationType: str,
                 parameters: list[Parameter]):
        """
        Initialize a Regulation object.

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
        parameters : list[Parameter]
            A list of Parameter object representing the parameters associated 
            with the regulation.

        Returns
        -------
        None.
        """
        super().__init__(sourceIndex, targetIndex, regulationType)
        self.parameters = parameters

class OptimizedRegulation(Regulation):
    """
    The container class for optimized parameters of an edge in a network.
    """
    def __init__(self, sourceIndex: int, targetIndex: int, regulationType: str,
                 parameters: list[Parameter], ID: str):
        """
        Initialize an OptimizedRegulation object.

        Parameters
        ----------
        regulationType : str
            A string representing the type of the regulation represented by 
            the edge.
        sourceIndex : int
            An integer indicating the index of the source node connected by 
            the edge.
        targetIndex : int
            An integer indicating the index of the target node connected by 
            the edge.
        parameters : list[Parameter]
            A list of Parameter object representing the parameters associated 
            with the regulation.
        ID : str
            A string representing the identity of the parameter set.

        Returns
        -------
        None.
        """
        super().__init__(sourceIndex, targetIndex, regulationType, parameters)
        self.ID = ID
