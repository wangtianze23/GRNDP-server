#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 17:03:38 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.generation.PromoterGeneratorFactory import \
    BaseHillPromoterGeneratorFactory, ParameterCollection, RegionSequence
from model.assemblage.Promoter import \
    FeaturedPromoter, RegulationPromoterCollection
from model.optimization.GeneratorException import \
    RegulationNotExistException, RegulationTypeNotSupportedException
from model.optimization.Network import Node, Regulation
from model.optimization.ParameterSpace import \
    RegulationParameterSpace, DiscreteRegulationParameterSpace
from model.optimization.SequenceSpace import RegulationSequenceSpace


class RegulationPromoterGenerator:
    """
    The class for generation of promoter sequences based on regulations in 
    a network.
    """
    def __init__(self, nodes: list[Node], regulations: list[Regulation], 
                 parameterSpaces: list[RegulationParameterSpace], 
                 sequenceSpaces: list[RegulationSequenceSpace]):
        """
        Initialize a RegulationPromoterGenerator object.

        Parameters
        ----------
        nodes : list[Node][Regulation]
            A list of Node objects indicating all entities in the network.
        regulations : list[Regulation]
            A list of regulations objects containing the parameters for 
            all regulatory relationships in the network.
        parameterSpaces : list[RegulationParameterSpace]
            A list of RegulationParameterSpace objects representing 
            the parameter spaces for each regulation. The length of the list 
            must equal to the length of **regulations**.
        parameterSpaces : list[RegulationSequenceSpace]
            A list of RegulationSequenceSpace objects representing 
            the sequence spaces for each regulation. The length of the list 
            must equal to the length of **regulations**.

        Returns
        -------
        None.
        """
        self.nodes = nodes
        self.regulations = regulations
        self.parameterSpaces = parameterSpaces
        self.sequenceSpaces = sequenceSpaces
    
    def generate(self, targetIndex: int) -> FeaturedPromoter:
        """
        Generate a promoter pertaining to a specific regulation.

        Parameters
        ----------
        targetIndex : int
            The index of a node that accept the regulation.

        Returns
        -------
        FeaturedPromoter or NoneType
            A FeaturedPromoter object containing the sequence and parameters 
            associated with a promoter that can be used to implement 
            the regulatory relationship on the specified node, or NoneType 
            if no promoter shall be used.
        """
        # Get regulations associated with the specified node
        regulationIndexes = [i for i, X in enumerate(self.regulations) 
                             if X.targetIndex == targetIndex]
        if len(regulationIndexes) == 0:
            raise RegulationNotExistException(targetIndex)
        
        # Determine the type of the generator to use
        generatorType = None
        regulations = [self.regulations[i] for i in regulationIndexes]
        if len(regulations) == 1:
            if regulations[0].regulationType == 'activation':
                generatorType = 'HillA'
            elif regulations[0].regulationType == 'repression':
                generatorType = 'HillR'
            elif regulations[0].regulationType == 'constant':
                return None
        elif len(regulations) == 2:
            regulationIndexes = \
                [next(iter(j for i, j in enumerate(regulationIndexes) 
                           if regulations[i].regulationType == 'activation'), 
                      None), 
                 next(iter(j for i, j in enumerate(regulationIndexes) 
                           if regulations[i].regulationType == 'repression'), 
                      None)]
            if all(X is not None for X in regulationIndexes):
                generatorType = 'HillAR'
        if generatorType is None:
            raise RegulationTypeNotSupportedException(
                            ','.join(X.regulationType for X in regulations))
        
        # Prepare parameters and sequences for the generators
        parameterSpaces = [self.parameterSpaces[i] for i in regulationIndexes]
        sequenceSpaces = [self.sequenceSpaces[i] for i in regulationIndexes]
        parameters = [ParameterCollection(X.dimensionNames,X.valueIDs,X.values)
                      for X in parameterSpaces]
        sequences = [[next(iter(RegionSequence(ID, S) 
                                for Z, S in zip(Y.sequenceIDs, Y.sequences) 
                                if Z == ID), '') 
                      for ID in X.valueIDs] 
                     for X, Y in zip(parameterSpaces, sequenceSpaces)]
        generator = BaseHillPromoterGeneratorFactory.createFromParameters(
                                        generatorType, parameters, sequences)
        
        # Generate a sequence with properties determined by the regulations
        regulations = [self.regulations[i] for i in regulationIndexes]
        return generator.generateWithProperties([{Y.name: Y.value 
                                                  for Y in X.parameters} 
                                                 for X in regulations])
    
    def generateAll(self) -> RegulationPromoterCollection:
        """
        Generate promoters pertaining to all the regulations in the network.

        Returns
        -------
        RegulationPromoterCollection
            A RegulationPromoterCollection object containing all the promoters 
            that can be used to implement the regulatory relationships in 
            the network.
        """
        # Get all nodes associated with at least one regulation
        nodeIndexes = sorted(set(X.targetIndex for X in self.regulations))
        promoters = [self.generate(i) for i in nodeIndexes]
        
        # Exlucde nodes without a promoter
        nodeIndexes = [X for X, Y in zip(nodeIndexes, promoters) 
                       if Y is not None]
        promoters = [X for X in promoters if X is not None]
        
        return RegulationPromoterCollection(promoters, nodeIndexes, 
                                            ['P_{}'.format(self.nodes[i].name) 
                                             for i in nodeIndexes])
