#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 09:52:42 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.simulation.Graph import AdjacencyMatrix
from model.simulation.HillRegulationFactory import HillRegulationFactory
from model.simulation.Network import \
    Regulation, PairedRegulation, NetworkParameterIndex, ParameterMapping, \
    BaseNetwork, AcyclicNetwork
from model.simulation.Regulation import ConstantRegulation


class BaseNetworkFactory:
    """
    The factory class for BaseNetwork classes.
    """
    @staticmethod
    def createFromRegulations(nodeCount: int, 
                              regulations: list[Regulation]) -> BaseNetwork:
        """
        Construct a BaseNetwork object from regulation parameters.

        Parameters
        ----------
        nodeCount : int
            The number of nodes in a network.
        regulations : list[Regulation]
            A list of Regulation objects representing the complete regulatory 
            relationships in a network. The length of the list equals to 
            the number of regulations.

        Returns
        -------
        BaseNetwork
            A BaseNetwork object created with the given regulations and 
            parameters.
        """
        # Determine the network type
        adjacencyMatrix = AdjacencyMatrix([[0] * nodeCount 
                                           for i in range(0, nodeCount)])
        for regulation in regulations:
            for sourceIndex in regulation.sourceIndexes:
                adjacencyMatrix[regulation.targetIndex][sourceIndex] = 1
        if adjacencyMatrix.acyclic():
            network = AcyclicNetwork(nodeCount)
        else:
            network = BaseNetwork(nodeCount)
        
        # Add regulations to the network
        for regulation in regulations:
            if regulation.regulationType == 0:
                regulationObject = ConstantRegulation(regulation.parameters[0])
            else:
                regulationObject = HillRegulationFactory.createFromParameters(
                                                    regulation.regulationType, 
                                                    regulation.parameters)
            network.setRegulation(regulation.sourceIndexes, 
                                  regulation.targetIndex, regulationObject)
        
        return network
    
    @staticmethod
    def createFromPairedRegulations(nodeCount: int, 
                                    regulations: list[PairedRegulation]) \
                                   -> (BaseNetwork, list[ParameterMapping]):
        """
        Construct a BaseNetwork object from paried regulation parameters.

        Parameters
        ----------
        nodeCount : int
            The number of nodes in a network.
        regulations : list[PairedRegulation]
            A list of PairedRegulation objects representing the regulatory 
            relationships for node pairs in a network. The length of the list 
            equals to the number of node pairs involved in regulation.

        Returns
        -------
        (BaseNetwork, list[ParameterMapping])
            A tuple of the following items:
                - A BaseNetwork object created with the given regulations and \
                  parameters.
                - A list of ParameterMapping objects representing the mapping \
                  of the corresponding parameter in the regulations added to \
                  the network for each parameter in the original paired \
                  regulations. The length of the list equals to the length of \
                  **regulations**, and the length of ParameterMapping objects \
                  equals to the number of parameters associated with \
                  the network for each element in **regulations**.
        """
        # Extract regulations and parameters
        connectionMatrix = [[0] * nodeCount for i in range(0, nodeCount)]
        indexMatrix = [[None] * nodeCount for i in range(0, nodeCount)]
        regulationMatrix = [[None] * nodeCount for i in range(0, nodeCount)]
        for i, regulation in enumerate(regulations):
            connectionMatrix[regulation.targetIndex][regulation.sourceIndex] =\
                                    1 if regulation.regulationType > 0 else \
                                    -1 if regulation.regulationType < 0 else 0
            indexMatrix[regulation.targetIndex][regulation.sourceIndex] = i
            regulationMatrix[regulation.targetIndex][regulation.sourceIndex] =\
                                                                    regulation
        
        # Determine the network type
        adjacencyMatrix = AdjacencyMatrix([[abs(Y) for Y in X] 
                                           for X in connectionMatrix])
        if adjacencyMatrix.acyclic():
            network = AcyclicNetwork(len(connectionMatrix))
        else:
            network = BaseNetwork(len(connectionMatrix))
          
        # Assign parameters to pairwise regulatory relationships
        parameterIndexMapping = [None] * len(regulations)
        for i, connections in enumerate(connectionMatrix):
            # Add constant regulations
            sourceIndexes = [j for j, X in enumerate(connections) 
                             if indexMatrix[i][j] is not None and X == 0]
            for j in sourceIndexes:
                regulation = ConstantRegulation(regulationMatrix[i][j].
                                                parameters[0])
                network.setRegulation((j,), i, regulation)
                parameterIndexMapping[indexMatrix[i][j]] = \
                    ParameterMapping([0], [NetworkParameterIndex((j,), i, 0)])
            
            # Add non-constant regulations
            sourceIndexes = [j for j, X in enumerate(connections) if X != 0]
            while len(sourceIndexes) > 0:
                activationIndexes = [k for k in sourceIndexes 
                                     if connections[k] > 0]
                repressionIndexes = [k for k in sourceIndexes 
                                     if connections[k] < 0]
                if len(activationIndexes) > 0 and len(repressionIndexes) > 0:
                    subsetIndexes = (activationIndexes[0],repressionIndexes[0])
                    components = [HillRegulationFactory.
                                  createFromParameters([connections[j]], 
                                                       regulationMatrix[i][j].
                                                       parameters) 
                                  for j in subsetIndexes]
                    parameterIndexes = [list(X.parameterIndexes.keys()) 
                                        for X in components]
                    regulation, newParameterIndexes = \
                        HillRegulationFactory.createFromCombination(components)
                else:
                    if len(activationIndexes) > 0:
                        j = activationIndexes[0]
                    else:
                        j = repressionIndexes[0]
                    regulation = HillRegulationFactory.createFromParameters(
                                            [connections[j]], 
                                            regulationMatrix[i][j].parameters)
                    parameterIndexes = [list(regulation.
                                             parameterIndexes.keys())]
                    newParameterIndexes = parameterIndexes
                    subsetIndexes = (j,)
                network.setRegulation(subsetIndexes, i, regulation)
                for j, indexes, newIndexes in \
                    zip(subsetIndexes, parameterIndexes, newParameterIndexes):
                    parameterIndexMapping[indexMatrix[i][j]] = \
                        ParameterMapping(indexes, 
                                         [NetworkParameterIndex(subsetIndexes, 
                                                                i, k) 
                                          for k in newIndexes])
                    sourceIndexes.remove(j)
        
        return (network, parameterIndexMapping)
