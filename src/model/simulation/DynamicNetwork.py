#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 12:14:22 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from infrastructure.simulation import TRaNS
from model.simulation.Network import BaseNetwork, NetworkParameterIndex
from model.simulation.Regulation import BaseRegulation


class BaseDynamicNetwork(BaseNetwork):
    """
    The base class for modeling directed regulatory networks with dynamics.
    """
    def __init__(self, nodeCount: int):
        """
        Initialize a BaseDynamicNetwork object.

        Parameters
        ----------
        nodeCount : int
            The number of nodes in the network.

        Returns
        -------
        None.
        """
        super().__init__(nodeCount)
        self.networkID = TRaNS.newNetwork(nodeCount)
        self.regulationIDs = [{} for i in range(0, nodeCount)]
        self.seed = None
    
    def __del__(self):
        """
        Destruct the BaseDynamicNetwork object.

        Returns
        -------
        None.
        """
        TRaNS.deleteNetwork(self.networkID)
    
    @classmethod
    def fromBaseNetwork(ClassType: type, base: BaseNetwork, 
                        minNoise: float, relativeNoise: float) -> object:
        """
        Construct a BaseDynamicNetwork from a BaseNetwork object.

        Parameters
        ----------
        base : BaseNetwork
            A BaseNetwork object based on which a new network shall be created.
        minNoise : float
            A float indicating the minimum noise level for all regulations.
        relativeNoise : float
            A float indicating the ratio of noise to all regulated strength.

        Returns
        -------
        object
            A BaseDynamicNetwork object with the same topology and parameters 
            as **base**.
        """
        newObject = ClassType(len(base.regulation))
        for targetIndex, regulations in enumerate(base.regulation):
            for sourceIndexes, regulation in regulations.items():
                newObject.setRegulation(sourceIndexes, targetIndex, regulation)
                newObject.setRegulationNoise(sourceIndexes, targetIndex, 
                                             minNoise, relativeNoise)
        return newObject
    
    def setRegulation(self, sourceIndexes: tuple, targetIndex: int, 
                      regulation: BaseRegulation):
        """
        Overrides BaseNetwork.setRegulation().
        """
        super().setRegulation(sourceIndexes, targetIndex, regulation)
        regulatorID = TRaNS.setRegulationType(self.networkID, sourceIndexes, 
                                              targetIndex, regulation.name)
        TRaNS.setRegulationParameters(regulatorID, 
                                      [regulation.parameter(i) 
                                       for i in 
                                           regulation.parameterIndexes.keys()])
        self.regulationIDs[targetIndex][sourceIndexes] = regulatorID
    
    def setRegulationNoise(self, sourceIndexes: tuple, targetIndex: int, 
                           minNoise: float, relativeNoise: float):
        """
        Set the noise level of regulation for simulation.

        Parameters
        ----------
        sourceIndexes : tuple
            The index of the source nodes of the regulation.
        targetIndex : int
            The index of the target node of the regulation.
        minNoise : float
            A float indicating the minimum noise level.
        relativeNoise : float
            A float indicating the ratio of noise to regulation strength.

        Returns
        -------
        None.
        """
        if sourceIndexes in self.regulationIDs[targetIndex]:
            regulatorID = self.regulationIDs[targetIndex][sourceIndexes]
            TRaNS.setRegulationNoise(regulatorID, relativeNoise, minNoise)
    
    def updateRegulation(self, index: NetworkParameterIndex, parameter: float):
        """
        Overrides BaseNetwork.updateRegulation().
        """
        super().updateRegulation(index, parameter)
        if index.sourceIndexes in self.regulationIDs[index.targetIndex]:
            regulatorID = \
                self.regulationIDs[index.targetIndex][index.sourceIndexes]
            TRaNS.setRegulationParameter(regulatorID, index.parameterIndex, 
                                         parameter)
    
    def setSeed(self, seed = None):
        """
        Set the seed for the random number generator (RNG) when simulating  
        network dynamics.

        Parameters
        ----------
        seed : int or NoneType
            An integer fed to the RNG, or None if no fixed seed is used.
            The default is None.

        Returns
        -------
        None.
        """
        self.seed = seed
    
    def evolve(self, X0: list, time: float, count: int) -> list:
        """
        Evolve the state of the network within a time span.

        Parameters
        ----------
        X0 : list
            A list of numeric values representing the initial state of 
            each node in the network.
        time : float
            A float value indicating the length of time span.
        count : int
            An positive integer indicating the total number of trajectories 
            to simulate parallelly.

        Returns
        -------
        list
            A list of list of float values representing the final state of 
            each node in each trajectory. The length of the outer list equals 
            to the number of trajectories, and the length of the inner list 
            equals to the number of node in the network.
        """
        TRaNS.setSeed(self.networkID, -1 if self.seed is None else self.seed)
        return TRaNS.evolveMultipleNetwork(self.networkID, X0, time, count)
