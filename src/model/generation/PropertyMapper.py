#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 17:22:22 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import math


class BasePropertyMapper:
    """
    The base class for mapping properties.
    """
    def __init__(self, propertyNames: list[str]):
        """
        Initialize a BasePropertyMapper objects.

        Parameters
        ----------
        propertyNames : list[str]
            A list of string representing the name of properties to map.

        Returns
        -------
        None.
        """
        self.propertyNames = propertyNames

    def mapMultiple(self, expected: dict[str, float]) -> dict[str, float]:
        """
        Map a series of expected values of properties to their actual ones.

        Parameters
        ----------
        expected : dict[str, float]
            A dictionary of strings pointing to numeric values, representing 
            the name and the expected value of each property.

        Returns
        -------
        dict[str, float]
            A dictionary of strings pointing to numeric values, representing 
            the name and the mapped value of each property.
        """
        raise NotImplementedError(BasePropertyMapper.mapMultiple)

class NearestNeighbourPropertyMapper(BasePropertyMapper):
    """
    The class for mapping properties by finding the nearest neighbour.
    """
    def __init__(self, propertyNames: list[str], 
                 propertyValues: list[list[float]], relativeTolerances = None):
        """
        Initialize a NearestNeighbourPropertyMapper object.

        Parameters
        ----------
        propertyNames : list[str]
            A list of string representing the name of properties to map.
        propertyValues : list[list[float]]
            A lists of lists of numeric values representing the possible 
            choices of property values. The length of the outer list 
            equals to the number of choices, and the length of the inner 
            list equals to the number of properties for each choice.
        relativeTolerances : list[float] or NoneType
            A list of numeric values representing the relative tolerance of 
            deviation of mapped values from expected ones for each property, 
            or NoneType if any deviation is tolerated.
            The default is None.

        Returns
        -------
        None.
        """
        super().__init__(propertyNames)
        self.properties = dict(zip(propertyNames, zip(*propertyValues)))
        if relativeTolerances is None:
            self.relativeTolerances = {}
        else:
            self.relativeTolerances = {X: relativeTolerances[X] 
                                       for X in self.properties.keys() 
                                       if X in relativeTolerances.keys()}
    
    def mapMultiple(self, expected: dict[str, float]) -> dict[str, float]:
        """
        Overrides BasePropertyMapper.mapMultiple().
        """
        if any(X not in self.properties.keys() for X in expected.keys()):
            return {}
        
        # Get choices with property values within the deviation tolerance
        choiceCount = min(len(X) for X in self.properties.values())
        matchedIndexes = [i for i in range(0, choiceCount)
                          if all(abs(Y - self.properties[X][i]) <= 
                                 Y * self.relativeTolerances[X] 
                                 if X in self.relativeTolerances 
                                 else True 
                                 for X, Y in expected.items())]
        if len(matchedIndexes) == 0:
            return {}
        
        # Calculate the deviation for each property and for each choice
        deviations = [[abs(Y - self.properties[X][i]) 
                       for X, Y in expected.items() 
                       if Y != self.properties[X][i]]
                      for i in matchedIndexes]
        
        # Select the choice with minimum geometric mean of deviation
        meanDeviations = [math.prod(X) ** (1 / len(X)) if len(X) > 0 else 0 
                          for X in deviations]
        choiceIndex = matchedIndexes[meanDeviations.index(min(meanDeviations))]
        return {X: self.properties[X][choiceIndex] for X in expected.keys()}
