#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:44:22 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import csv
from model.optimization.SequenceSpace import RegulationSequenceSpace


class RegulationSequenceSpaceFactory:
    """
    The base factory class for RegulationSequenceSpace classes.
    """
    @staticmethod
    def parseSequenceFile(dataFilename: str, mainColumnName = 'ID') \
                         -> (tuple[str], dict[str, tuple[str]]):
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
        (tuple[str], dict[str, tuple[str]])
            A tuple of the following items:
                - A tuple of strings representing the column names; the length 
                  of the tuple equals to the number of components
                - A dictionary of strings pointing to tuples of strings 
                  representing the parsed sequences in the space. The length 
                  of the dictionary equals to the number of sequence variants, 
                  and the length of each tuple equals to the number of 
                  components (subreions) in a sequence.
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
                                 (tuple(X) for X in parametersList))))
            else:
                return (columnNames, 
                        dict(zip((X[mainColumnIndex] for X in parametersList), 
                                 (tuple(Y for i, Y in enumerate(X) 
                                        if i != mainColumnIndex) 
                                  for X in parametersList))))
        return (columnNames, {})
    
    @staticmethod
    def createFromFile(dataFilename: str, ID: int) -> RegulationSequenceSpace:
        """
        Construct a RegulationSequenceSpace object from a data file.

        Parameters
        ----------
        dataFilename : str
            A string representing the path to a data file containing 
            the parameter values in the space.

        Returns
        -------
        RegulationSequenceSpace
            A RegulationSequenceSpace containing the parameter values 
            collected from the specified data file.
        """
        space = RegulationSequenceSpace(ID)
        
        # Parse the parameter file
        dimensionNames, parameters = \
                RegulationSequenceSpaceFactory.parseSequenceFile(dataFilename)
        if len(parameters) > 0:
            space.sequenceIDs = list(parameters.keys())
            space.sequences = list(parameters.values())
            space.alphabet = set(Y for X in space.sequences for Y in X)
            space.regionCount = max(len(X) for X in space.sequences)
        
        return space
