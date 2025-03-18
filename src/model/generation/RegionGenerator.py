#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 18:45:47 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.generation.PropertyMapper import NearestNeighbourPropertyMapper


class FeaturedRegion:
    """
    The container class for a region sequence with features.
    """
    def __init__(self, name: str, sequence: str, properties: dict[str, float], 
                 regionType = ''):
        """
        Initialize a FeaturedRegion object.

        Parameters
        ----------
        name : str
            A string indicating the name of the region.
        sequence : str
            A string representing a region sequence.
        properties : dict[str, float]
            A dictionary with strings as keys pointing to numeric values, 
            representing the name and value of the properties associate with 
            the promoter.
        regionType : str, optional
            A string representing the type of the region.
            The default is an empty string.

        Returns
        -------
        None.
        """
        self.name = name
        self.sequence = sequence
        self.properties = properties
        self.regionType = regionType
    
    def __str__(self) -> str:
        """
        Get a string representation of the region.

        Returns
        -------
        str
            A string representing the sequence of the region.
        """
        return self.sequence

class PromoterRegionGenerator:
    """
    The class for generating regions in promoter sequences.
    """
    def __init__(self, regionType: str, propertyNames: list[str], 
                 propertyValues: list[tuple[float]], sequences: list[str], 
                 sequenceIDs = None):
        """
        Initialize a PromoterRegionGenerator object.

        Parameters
        ----------
        regionType : str
            A string indicating the type of the region in generated promoters.
        propertyNames : list[str]
            A list of strings representing the name of properties associated 
            with the region.
        propertyValues : list[tuple[float]]
            A list of tuples of numeric values representing the property 
            values of each possible choices of region sequence. The length of 
            the outer list equals to the number of choices of region, and 
            the length of the inner tuple equals to the number of properties.
        sequences : list[str]
            A list of strings representing the possible choices of sequences 
            for the region.
        sequenceIDs : list[str] or NoneType, optional
            A list of strings representing the identity of each element in 
            **sequence**, or NoneType if their identities are not available.
            The default is None.

        Returns
        -------
        None.
        """
        self.regionType = regionType
        self.propertyNames = propertyNames
        self.propertyValues = propertyValues
        self.sequences = sequences
        self.sequenceIDs = sequenceIDs
        self.mapper = NearestNeighbourPropertyMapper(propertyNames, 
                                                     propertyValues)
    
    def generateWithProperty(self, properties: dict[str, float]) \
                            -> FeaturedRegion:
        """
        Generate a region with specific properties.

        Parameters
        ----------
        properties : dict[str, float]
            A dictionary of string as keys pointing to numeric values, 
            representing the name and the desired value of specific properties 
            for the generated region sequence.

        Returns
        -------
        FeaturedRegion
            A FeaturedRegion object containing the generated region and its 
            associated properties.
        """
        properties = self.mapper.mapMultiple(properties)
        matchedIndex = next(iter(i for i, X in enumerate(self.propertyValues)
                                 if all(X[self.propertyNames.index(key)] == 
                                        value 
                                        for key, value in properties.items())))
        return FeaturedRegion(self.sequenceIDs[matchedIndex] 
                              if self.sequenceIDs is not None else '', 
                              self.sequences[matchedIndex], 
                              {X: Y 
                               for X, Y in 
                                   zip(self.propertyNames, 
                                       self.propertyValues[matchedIndex])}, 
                              regionType = self.regionType)
