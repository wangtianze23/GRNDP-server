#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 11:15:51 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.assemblage.Sequence import AnnotatedSequence, RegionAnnotation
from model.assemblage.Promoter import FeaturedPromoter
from model.generation.RegionGenerator import PromoterRegionGenerator


class StructuredPromoterGenerator:
    """
    The base class for structured promoter generator classes.
    """
    def __init__(self, name: str, regionNames: list[str], 
                 regionGenerators: list[PromoterRegionGenerator]):
        """
        Initialize a StructuredPromoterGenerator object.

        Parameters
        ----------
        name : str
            A string representing the name of the generator.
        regionNames : list[str]
            An integer indicating the number of regions in a generated 
            promoter sequence.
        propertyMappers : list[PromoterRegionGenerator]
            A list of PromoterRegionGenerator objects used to map requested 
            properties to region sequences.

        Returns
        -------
        None.
        """
        self.name = name
        self.regionNames = regionNames
        self.regionGenerators = regionGenerators
    
    def mapRegionToRegulation(self, index: int) -> int:
        """
        Map a region to a regulatory component.

        Parameters
        ----------
        index : int
            An integer indicating the index of a region.

        Returns
        -------
        int or NoneType
            An integer representing the index of a regulatory component 
            associated with the specified region, or NoneType if the specified 
            region cannot be mapped to any regulatory component.
        """
        raise NotImplementedError(StructuredPromoterGenerator.
                                  mapRegionToRegulation)
    
    def regionCount(self) -> int:
        """
        Get the total number of regions in a generated promoter sequences.

        Returns
        -------
        int
            An integer representing the total number of regions.
        """
        return len(self.regionGenerators)
    
    def regionPropertyNames(self, index: int) -> list[str]:
        """
        Get the name of properties associated with a specific region.

        Parameters
        ----------
        index : int
            An integer indicating the index of a region.

        Returns
        -------
        list[str]
            A list of strings representing the name of properties associated 
            with the specified region.
        """
        raise NotImplementedError(StructuredPromoterGenerator.
                                  regionPropertyNames)
    
    def generateWithProperties(self, properties: list[dict[str, float]]) \
                              -> FeaturedPromoter:
        """
        Generate a list of promoter sequences of specific properties.

        Parameters
        ----------
        properties : list[dict[str, float]]
            A list of dictionaries of string as keys pointing to numeric 
            values, representing the name and the desired value of properties 
            for each region and for all generated promoters. The length of 
            the list equals to the number of regulatory components, and 
            the length of each dictionary equals to the number of properties 
            associated with the corresponding component.

        Returns
        -------
        list[FeaturedPromoter]
            A list of FeaturedPromoter objects representing the generated 
            promoter sequences and their associated properties.
        """
        regionCount = self.regionCount()
        regionPropertyNames = [self.regionPropertyNames(i) 
                               for i in range(0, regionCount)]
        regionPropertyMaps = [{Y: self.mapRegionToRegulation(i) for Y in X} 
                              for i, X in enumerate(regionPropertyNames)]
        regionProperties = [{X: properties[propertyMap[X]][X] for X in names} 
                            for names, propertyMap in 
                                zip(regionPropertyNames, regionPropertyMaps)]
        regionSequences = [generator.generateWithProperty(properties) 
                           for generator, properties in 
                               zip(self.regionGenerators, regionProperties)]
        regionPositionRanges = [(sum(len(X.sequence) 
                                     for X in regionSequences[:i]), 
                                 sum(len(X.sequence) 
                                     for X in regionSequences[:i + 1]))
                                for i, X in enumerate(regionSequences)]
        regionMasks = [len(X.sequence) > 0 for X in regionSequences]
        sequence = AnnotatedSequence(''.join(str(X) for X in regionSequences), 
                                     [RegionAnnotation(region.name, 
                                                       positionRanges[0],
                                                       positionRanges[1], 
                                                       region.regionType) 
                                      for mask, region, positionRanges in 
                                          zip(regionMasks, regionSequences, 
                                              regionPositionRanges) if mask])
        return FeaturedPromoter(sequence, 
                                {x: y 
                                 for X, mask in 
                                     zip(regionSequences, regionMasks) if mask 
                                 for x, y in X.properties.items()})
