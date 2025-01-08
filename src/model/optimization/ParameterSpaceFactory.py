#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:44:22 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import csv
from model.optimization.ParameterSpace import DiscreteRegulationParameterSpace
from model.optimization.GenerativeParameterSpace import \
    GenerativeRegulationParameterSpace


class RegulationParameterSpaceFactory:
    """
    The base factory class for RegulationParameterSpace classes.
    """
    @staticmethod
    def parseDataFile(dataFilename: str, 
                      mainColumnName = 'ID') -> (tuple[str], dict):
        """
        Parse the data (parameters) in a data file of a parameter space.

        Parameters
        ----------
        dataFilename : str
            A string representing the path to a table (CSV) file containing 
            the parameter values in the space.
        mainColumnIndex : int or None, optional
            An integer indicating the name of the column containing 
            the identity of each possible choice of values (raws), or None if 
            the identity information is not available and auto-incremental 
            identities will be assigned to parsed values.
            The default is 'ID'.

        Returns
        -------
        (tuple[str], dict)
            A tuple of the following items:
                - A tuple of strings representing the column names; the length 
                  of the tuple equals to the number of components
                - A dictionary of strings pointing to tuples of numeric values 
                  representing the parsed values of each component (dimension) 
                  in the space. The length of the dictionary equals to 
                  the number of values, and the length of each tuple equals 
                  to the number of components
        """
        columnNames = tuple()
        parametersList = []
        with open(dataFilename, 'r') as parameterFile:
            data = csv.reader(parameterFile)
            columnNames = next(data)
            parametersList = list(data)
            if mainColumnName in columnNames:
                mainColumnIndex = columnNames.index(mainColumnName)
                columnNames = [X for i, X in enumerate(columnNames) 
                               if i != mainColumnIndex]
            else:
                mainColumnIndex = None
        
        if len(parametersList) > 0:
            if mainColumnIndex is None:
                return (columnNames, 
                        dict(zip(range(0, len(parametersList)), 
                                 (tuple(float(Y) for Y in X) 
                                  for X in parametersList))))
            else:
                return (columnNames, 
                        dict(zip((X[mainColumnIndex] for X in parametersList), 
                                 (tuple(float(Y) for i, Y in enumerate(X) 
                                        if i != mainColumnIndex) 
                                  for X in parametersList))))
        return (columnNames, {})

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
        dimensionNames, parameters = \
                    RegulationParameterSpaceFactory.parseDataFile(dataFilename)
        space.dimension = len(dimensionNames)
        space.dimensionNames = dimensionNames
        if len(parameters) > 0:
            space.valueIDs = list(parameters.keys())
            space.values = list(parameters.values())
            space.boundaries = [(min(X[i] for X in space.values), 
                                 max(X[i] for X in space.values)) 
                                for i in range(0, space.dimension)]
        
        return space

class GenerativeRegulationParameterSpaceFactory:
    """
    The factory class for GenerativeRegulationParameterSpace classes.
    """
    @staticmethod
    def createFromFile(dataFilename: str, ID: int, regulationType: str) \
                      -> GenerativeRegulationParameterSpace:
        """
        Construct a GenerativeRegulationParameterSpace object from a data file.

        Parameters
        ----------
        dataFilename : str
            A string representing the path to a data file containing 
            the parameter values in the space.

        Returns
        -------
        GenerativeRegulationParameterSpace
            A GenerativeRegulationParameterSpace object containing 
            the parameter ranges collected from the specified data file.
        """
        space = GenerativeRegulationParameterSpace(ID, regulationType)
        
        # Parse the parameter file
        dimensionNames, parameters = \
                    RegulationParameterSpaceFactory.parseDataFile(dataFilename)
        space.dimension = len(dimensionNames)
        space.dimensionNames = dimensionNames
        if len(parameters) > 0:
            space.boundaries = [(min(X[i] for X in parameters.values()), 
                                 max(X[i] for X in parameters.values())) 
                                for i in range(0, space.dimension)]
        
        return space
