#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 09:45:12 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.generation.HillPromoterGenerator import \
    BaseHillPromoterGenerator, HillActivationPromoterGenerator, \
    HillRepressionPromoterGenerator, HillARPromoterGenerator
from model.generation.RegionGenerator import PromoterRegionGenerator


class ParameterCollection:
    """
    The container class for a set of parameter vectors.
    """
    def __init__(self, dimensions: list[str], IDs: list[str], 
                 values: list[list[float]]):
        """
        Initialize a ParameterCollection object.

        Parameters
        ----------
        dimensions : list[str]
            A list of strings representing the name of each dimension for 
            an element. The length of the list equals to the number of 
            dimensions.
        IDs : list[str]
            A list of strings representing the identity of each element.
        values : list[list[float]]
            A list of lists of numeric values representing the value on 
            each dimension for each element. The length of the outer list 
            equals to the number of elements, and the length of the inner list 
            equals to the number of dimensions.

        Returns
        -------
        None.
        """
        self.dimensions = dimensions
        self.IDs = IDs
        self.values = values

class RegionSequence:
    """
    The container class for an identifiable sequence in a region.
    """
    def __init__(self, ID: str, subregions: list[str]):
        """
        Initialize a RegionSequence object.

        Parameters
        ----------
        ID : str
            The identity of the region sequence.
        subregions : list[str]
            A list of string representing the sequence in each component 
            (subregion) of the region.

        Returns
        -------
        None.
        """
        self.ID = ID
        self.subregions = subregions

class BaseHillPromoterGeneratorFactory:
    """
    The factory class for BaseHillPromoterGenerator classes.
    """
    @staticmethod
    def createFromParameters(regulationType: str, 
                             parameterLists: list[ParameterCollection], 
                             sequenceLists: list[list[RegionSequence]]) \
                            -> BaseHillPromoterGenerator:
        """
        Construct a BaseHillPromoterGenerator object from possible choices of 
        parameters and sequences.

        Parameters
        ----------
        regulationType : str
            A string of either 'HillA', 'HillR' or 'HillAR' indicating 
            the type of the generator to create.
        parameterLists : list[ParameterCollection]
            A list of ParameterCollection objects containing the possible 
            choices of parameters for each component of the regulation that 
            can be applied to the generated promoters. The length of the list 
            equals to the number of regulatory components.
        sequenceLists : list[list[RegionSequence]]
            A list of lists of RegionSequence objects representing 
            the possible choices of sequences for each region assoicated with 
            each component of the regulation. The length of the outer list 
            equals to the number of regulatory component, and the length of 
            the inner list equals to the number of regions in a sequence.

        Returns
        -------
        BaseHillPromoterGenerator
            A BaseHillPromoterGenerator object that can be used to generate 
            promoter sequences.
        """
        if regulationType == 'HillA':
            return HillActivationPromoterGenerator(
                    [PromoterRegionGenerator('regulatory', 
                                             parameterLists[0].dimensions, 
                                             parameterLists[0].values, 
                                             [X.subregions[0] 
                                              for X in sequenceLists[0]], 
                                             [X.ID 
                                              for X in sequenceLists[0]])])
        elif regulationType == 'HillR':
            return HillRepressionPromoterGenerator(
                    [PromoterRegionGenerator('regulatory', 
                                             parameterLists[0].dimensions, 
                                             parameterLists[0].values, 
                                             [X.subregions[0] 
                                              for X in sequenceLists[0]], 
                                             [X.ID 
                                              for X in sequenceLists[0]]), 
                     PromoterRegionGenerator('regulatory', 
                                              parameterLists[0].dimensions, 
                                              parameterLists[0].values, 
                                              [X.subregions[1] 
                                               for X in sequenceLists[0]], 
                                              [X.ID 
                                               for X in sequenceLists[0]]), 
                      PromoterRegionGenerator('regulatory', 
                                               parameterLists[0].dimensions, 
                                               parameterLists[0].values, 
                                               [X.subregions[2] 
                                                for X in sequenceLists[0]], 
                                               [X.ID 
                                                for X in sequenceLists[0]])])
        elif regulationType == 'HillAR':
            return HillARPromoterGenerator(
                    [PromoterRegionGenerator('regulatory', 
                                             parameterLists[1].dimensions, 
                                             parameterLists[1].values, 
                                             [X.subregions[0] 
                                              for X in sequenceLists[1]], 
                                             [X.ID 
                                              for X in sequenceLists[1]]), 
                     PromoterRegionGenerator('regulatory', 
                                              parameterLists[0].dimensions, 
                                              parameterLists[0].values, 
                                              [X.subregions[0] 
                                               for X in sequenceLists[0]], 
                                              [X.ID 
                                               for X in sequenceLists[0]]), 
                      PromoterRegionGenerator('regulatory', 
                                               parameterLists[1].dimensions, 
                                               parameterLists[1].values, 
                                               [X.subregions[2] 
                                                for X in sequenceLists[1]], 
                                               [X.ID 
                                                for X in sequenceLists[1]])])
