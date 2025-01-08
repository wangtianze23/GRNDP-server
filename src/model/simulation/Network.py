#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 20:56:34 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.simulation.NetworkException import NoPathException
from model.simulation.Regulation import BaseRegulation


class Regulation:
    """
    The container class holding the regulatory relationship between a list of 
    source nodes and a target node in a network.
    """
    def __init__(self, sourceIndexes: list[int], targetIndex: int, 
                 regulationType: int, parameters: list):
        """
        Initialize a Regulation object.

        Parameters
        ----------
        sourceIndexes : list[int]
            A list of integers representing the index of the source nodes of 
            a regulation.
        targetIndex : int
            An integer representing the index of the target node of a 
            regulation.
        regulationType : int
            An integer of either 1 (activation) or -1 (repression) indicating 
            the type of the regulation.
        parameters : list
            The parameters associated with the regulation.

        Returns
        -------
        None.
        """
        self.sourceIndexes = sourceIndexes
        self.targetIndex = targetIndex
        self.regulationType = regulationType
        self.parameters = parameters

class PairedRegulation:
    """
    The container class holding the regulatory relationship between a paried 
    of nodes in a network.
    """
    def __init__(self, sourceIndex: int, targetIndex: int, 
                 regulationType: int, parameters: list):
        """
        Initialize a PairedRegulation object.

        Parameters
        ----------
        sourceIndex : int
            The index of the source node of a regulation.
        targetIndex : int
            The index of the target node of a regulation.
        regulationType : int
            An integer of either 1 (activation) or -1 (repression) indicating 
            the type of the regulation.
        parameters : list
            The parameters associated with the regulation.

        Returns
        -------
        None.
        """
        self.sourceIndex = sourceIndex
        self.targetIndex = targetIndex
        self.regulationType = regulationType
        self.parameters = parameters

class NetworkParameterIndex:
    """
    The container class for indexing regulation parameters in a network.
    """
    def __init__(self, sourceIndexes: tuple, targetIndex: int, 
                 parameterIndex: int):
        """
        Initialize a NetworkParameterIndex object.

        Parameters
        ----------
        sourceIndexes : list[int]
            A list of integers representing the index of the source nodes of 
            a regulation.
        targetIndex : int
            An integer representing the index of the target node of a 
            regulation.
        parameterIndex : int
            An integer representing the index of a parameter in a regulation.

        Returns
        -------
        None.
        """
        self.sourceIndexes = sourceIndexes
        self.targetIndex = targetIndex
        self.parameterIndex = parameterIndex

class ParameterMapping(dict):
    """
    The container class for mapping the index of a parameter to the index of 
    corresponding regulation parameter in a network.
    """
    def __init__(self, originalIndexes: list[int], 
                 mappedIndexes: list[NetworkParameterIndex]):
        """
        Initialize a ParameterMapping object.

        Parameters
        ----------
        originalIndexes : list[int]
            A list of integers as dictionary keys representing the original 
            index of each mapped parameter.
        mappedIndexes : list[NetworkParameterIndex]
            A list of NetworkParameterIndex objects as dictionary values 
            representing the index of each parameter in a network. 
            Any NoneType value will be discard together with the corresponding 
            key in **originalIndexes**.

        Returns
        -------
        None.
        """
        super().__init__((X, Y) for X, Y in zip(originalIndexes, mappedIndexes)
                         if Y is not None)
    
    def __getitem__(self, originalIndex: int) -> NetworkParameterIndex:
        """
        Overrides dict.__getitem__().
        """
        return super().__getitem__(originalIndex)

class BaseNetwork:
    """
    The base class for modeling directed regulatory networks.
    """
    def __init__(self, nodeCount: int):
        """
        Initialize a BaseNetwork object.

        Parameters
        ----------
        nodeCount : int
            The number of nodes in the network.

        Returns
        -------
        None.
        """
        self.regulation = [{} for i in range(0, nodeCount)]
    
    def setRegulation(self, sourceIndexes: tuple, targetIndex: int, 
                      regulation: BaseRegulation):
        """
        Set the regulation among multiple nodes.

        Parameters
        ----------
        sourceIndexes : tuple
            The index of the source nodes of the regulation.
        targetIndex : int
            The index of the target node of the regulation.
        regulation : BaseRegulation
            A BaseRegulation object representing the regulation exerted on 
            the target node by the source nodes.

        Returns
        -------
        None.
        """
        self.regulation[targetIndex][sourceIndexes] = regulation
    
    def updateRegulation(self, index: NetworkParameterIndex, parameter: float):
        """
        Update the value of a parameter in a network.

        Parameters
        ----------
        index : NetworkParameterIndex
            A NetworkParameterIndex object containing the location about 
            the parameter.
        parameter : float
            The new value of the parameter.

        Returns
        -------
        None.
        """
        if index.sourceIndexes in self.regulation[index.targetIndex]:
            self.regulation[index.targetIndex][index.sourceIndexes].\
                                setParameter(index.parameterIndex, parameter)
    
    def getParameter(self, index: NetworkParameterIndex) -> float:
        """
        Get the value of a parameter in a network.

        Parameters
        ----------
        index : NetworkParameterIndex
            A NetworkParameterIndex object containing the location about 
            the parameter.

        Returns
        -------
        float
            The value of the specified parameter.
        """
        if index.sourceIndexes in self.regulation[index.targetIndex]:
            return self.regulation[index.targetIndex][index.sourceIndexes].\
                                                parameter(index.parameterIndex)
    
    def getAssociatedNodes(self, sourceIndex: int, targetIndex: int) -> set:
        """
        Get the node associated with a specific subset of the network.

        Parameters
        ----------
        sourceIndex : int
            The index of the source node of a regulation chain.
        targetIndex : int
            The index of the target node of a regulation chain.

        Returns
        -------
        set
            A set of integers representing the index of nodes associated with 
            the regulation chain from the source node to the target node.
        """
        if sourceIndex == targetIndex:
            return [sourceIndex]
        subnodes = set(j 
                       for X in self.regulation[targetIndex].keys() for i in X 
                       for j in self.getAssociatedNodes(sourceIndex, i))
        if sourceIndex in subnodes:
            subnodes.add(targetIndex)
        return subnodes

class NetworkPath:
    """
    The class for modeling paths in a directed network.
    """
    def __init__(self, network: BaseNetwork, nodeIndexes: list):
        """
        Initialize a NetworkPath object.

        Parameters
        ----------
        network : BaseNetwork
            A reference to a BaseNetwork object containing nodes and 
            regulations.
        nodeIndexes : list
            A list of integers representing a path that satisfies 
            the regulatory relationships in the network. 

        Returns
        -------
        None.
        """
        self.network = network
        self.nodeIndexes = nodeIndexes
        self.nodeValues = [None] * len(self.nodeIndexes)
    
    def __call__(self, X: float) -> float:
        """
        Calculate the regulatory effect (output) along the path with an input.

        Parameters
        ----------
        X : float
            A numeric value representing the input to the path.

        Returns
        -------
        float
            A numeric value representing the effect (output) from the path.
        """
        nodeValues = self.nodeValues
        for i in self.nodeIndexes:
            if i == 0:
                nodeValues[i] = X
            else:
                nodeValues[i] = sum(T(tuple(nodeValues[j] for j in indexes)) 
                                    for indexes, T in 
                                    self.network.regulation[i].items())
        return nodeValues[-1]

class AcyclicNetwork(BaseNetwork):
    """
    The class for modeling acyclic and directed regulatory networks.
    """
    def getPath(self, sourceIndex: int, targetIndex: int) -> NetworkPath:
        """
        Get a path from a source node to a target node that satisfies 
        the regulatory relationships in the network. 

        Parameters
        ----------
        sourceIndex : int
            The index of the source node of a regulation chain.
        targetIndex : int
            The index of the target node of a regulation chain.
        
        Raises
        ------
        NoPathException
            Raised when no path found between the specified nodes.
        
        Returns
        -------
        NetworkPath
            A NetworkPath object containing the path from the source node to 
            the target node.
        """
        nodeIndexes = self.getAssociatedNodes(sourceIndex, targetIndex)
        connections = [None if i == targetIndex 
                       else list(set(i for Y in X.keys() for i in Y)) 
                       for i, X in enumerate(self.regulation) 
                       if i in nodeIndexes]
        
        # Topological sorting of the directed acyclic graph
        nodeOrders = []
        index = sourceIndex
        while True:
            nodeOrders.append(index)
            if index < len(connections):
                connections[index] = None
            else:
                raise NoPathException(sourceIndex, targetIndex)
            for connection in connections:
                if connection is not None and index in connection:
                    connection.remove(index)
            if index == targetIndex or \
               all(len(X) > 0 for X in connections if X is not None):
                break
            index = next(iter(i for i, X in enumerate(connections) 
                              if X is not None and len(X) == 0))
        
        return NetworkPath(self, nodeOrders)
