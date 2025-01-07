#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 17:17:45 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.simulation.HillRegulation import Hill, HillA, HillR, HillAR
from model.simulation.RegulationException import RegulationInvalidTypeException


class HillRegulationFactory:
    """
    The factory class for Hill classes.
    """
    @staticmethod
    def createFromParameters(regulationTypes: list, parameters: list) -> Hill:
        """
        Construct a Hill object with specified parameters.

        Parameters
        ----------
        regulationTypes : list
            A list of integers of either 1 (activation) or -1 (repression) 
            indicating the type of each component of the regulation.
        parameters : list
            A list of numeric values representing the parameters associated 
            with the regulation.

        Raises
        ------
        RegulationInvalidTypeException
            Raised when the specified types are not valid.

        Returns
        -------
        Hill
            A Hill object of specified types and parameters.
        """
        connectivity = len(regulationTypes)
        if connectivity == 1:
            if regulationTypes[0] > 0:
                return HillA(*parameters)
            else:
                return HillR(*parameters)
        if connectivity == 2:
            if regulationTypes[0] > 0 and regulationTypes[1] < 0:
                return HillAR(*parameters)
        raise RegulationInvalidTypeException(str(regulationTypes))
    
    @staticmethod
    def createFromCombination(regulations: list[Hill]) \
                             -> (Hill, list[list]):
        """
        Construct a Hill object from multiple Hill objects.

        Parameters
        ----------
        regulations : list[Hill]
            A list of Hill objects representing the component regulations.

        Raises
        ------
        RegulationInvalidTypeException
            Raised when the type of any component regulations is not valid.

        Returns
        -------
        (Hill, list[list])
            A tuple of the following items:
                - A Hill object composed of given component regulations
                - A list of lists of integers or None indicating the index of \
                  corresponding parameter in the combined Hill object for \
                  each parameter in each component regulation; the item is \
                  replaced by None if the original parameter is not mapped. 
                  The length of the outer list equals to the length of \
                  **regulations**, and the length of the inner length equals \
                  to the number of  parameters in each component regulations.
        """
        activation = [X for X in regulations if isinstance(X, HillA)]
        repression = [X for X in regulations if isinstance(X, HillR)]
        if len(activation) == 1 and len(repression) == 1:
            return (HillAR(repression[0].y_min, repression[0].y_max, 
                           activation[0].K, activation[0].n, 
                           repression[0].K, repression[0].n, 
                           repression[0].correction), 
                    [[None, None, 2, 3], [0, 1, 4, 5, None, 6]])
        raise RegulationInvalidTypeException(str(regulations))
