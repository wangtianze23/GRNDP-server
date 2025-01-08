#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:44:22 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import csv
from model.optimization.ParameterSpace import DiscreteRegulationParameterSpace


class DiscreteRegulationParameterSpaceFactory:
    """
    The factory class for DiscreteRegulationParameterSpace classes.
    """
    @staticmethod
    def createFromFile(dataFilename: str, ID: int, regulationType: str) \
                      -> DiscreteRegulationParameterSpace:
        """
        Construct a DiscreteRegulationParameterSpace object from a data file.

        Parameters
        ----------
        dataFilename : str
            A string representing the path to a data file containing 
            the parameter values in the space.

        Returns
        -------
        DiscreteRegulationParameterSpace
            A DiscreteRegulationParameterSpace containing the parameter values 
            collected from the specified data file.
        """
        space = DiscreteRegulationParameterSpace(ID, regulationType)
        
        # Parse the parameter file
        parametersList = []
        with open(dataFilename, 'r') as parameterFile:
            data = csv.reader(parameterFile)
            columnNames = next(data)
            parametersList = list(data)
            if 'ID' in columnNames:
                space.dimension = len(columnNames) - 1
                space.dimensionNames = columnNames
                mainColumnIndex = columnNames.index('ID')
            else:
                space.dimension = len(columnNames)
                mainColumnIndex = None
        
        # Extract the parameter values and boundaries
        if len(parametersList) > 0:
            if mainColumnIndex is None:
                space.values = parametersList
            else:
                space.values = [tuple(float(Y) for i, Y in enumerate(X) 
                                      if i != mainColumnIndex) 
                                for X in parametersList]
                space.valueIDs = [X[mainColumnIndex] for X in parametersList]
            space.boundaries = [(min(X[i] for X in space.values), 
                                 max(X[i] for X in space.values)) 
                                for i in range(0, space.dimension)]
        
        return space
