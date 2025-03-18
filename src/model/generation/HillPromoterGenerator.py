#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 17:13:18 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.generation.PromoterGenerator import StructuredPromoterGenerator
from model.generation.RegionGenerator import PromoterRegionGenerator


class BaseHillPromoterGenerator(StructuredPromoterGenerator):
    """
    The class for generating promoters regulated by transcriptional regulators 
    in a manner that can be described by a Hill equation.
    """
    def __init__(self, regionNames: list[str], 
                 regionGenerators: list[PromoterRegionGenerator]):
        """
        Initialize a BaseHillPromoterGenerator object.

        Parameters
        ----------
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
        super().__init__('Hill', regionNames, regionGenerators)
    
    def mapRegionToRegulation(self, index: int) -> int:
        """
        Overrides StructuredPromoterGenerator.mapRegionToRegulation().
        """
        if index == 0:
            return 0
        return None
    
    def regionPropertyNames(self, index: int) -> list[str]:
        """
        Overrides StructuredPromoterGenerator.regionPropertyNames().
        """
        if index == 0:
            return ['y_min', 'y_max', 'K', 'n']
        return []

class HillActivationPromoterGenerator(BaseHillPromoterGenerator):
    """
    The class for generating promoters containing a single operator site 
    for transcriptional activators.
    """
    def __init__(self, regionGenerators: list[PromoterRegionGenerator]):
        """
        Initialize a HillActivationPromoterGenerator object.

        Parameters
        ----------
        regionGenerators : list[PromoterRegionGenerator]
            A list of list of strings representing the name of properties for 
            each generated promoter sequence.

        Returns
        -------
        None.
        """
        super().__init__(['Activator binding site'], regionGenerators)
        self.name = 'HillA'

class HillRepressionPromoterGenerator(BaseHillPromoterGenerator):
    """
    The class for generating promoters containing a single operator site 
    for transcriptional repressors.
    """
    def __init__(self, regionGenerators: list[PromoterRegionGenerator]):
        """
        Initialize a HillActivationPromoterGenerator object.

        Parameters
        ----------
        regionGenerators : list[PromoterRegionGenerator]
            A list of list of strings representing the name of properties for 
            each generated promoter sequence.

        Returns
        -------
        None.
        """
        super().__init__(['Repressor binding site'], regionGenerators)
        self.name = 'HillR'

class HillARPromoterGenerator(BaseHillPromoterGenerator):
    """
    The class for generating promoters containing an operator site for 
    transcriptional activators and another operator site for transcriptional 
    repressors.
    """
    def __init__(self, regionGenerators: list[PromoterRegionGenerator]):
        """
        Initialize a HillARPromoterGenerator object.

        Parameters
        ----------
        regionGenerators : list[PromoterRegionGenerator]
            A list of list of strings representing the name of properties for 
            each generated promoter sequence.

        Returns
        -------
        None.
        """
        super().__init__(['Repressor binding site', 'Activator binding site', 
                          'Repressor binding site'], 
                         regionGenerators)
        self.name = 'HillAR'
    
    def mapRegionToRegulation(self, index: int) -> int:
        """
        Overrides StructuredPromoterGenerator.mapRegionToRegulation().
        """
        if index == 0 or index == 2:
            return 1
        elif index == 1:
            return 0
        return None
    
    def regionPropertyNames(self, index: int) -> list[str]:
        """
        Overrides StructuredPromoterGenerator.regionPropertyNames().
        """
        if index == 0 or index == 2:
            return ['y_min', 'y_max', 'K', 'n']
        if index == 1:
            return ['K', 'n']
        return []
