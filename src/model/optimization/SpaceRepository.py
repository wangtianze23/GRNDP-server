#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repository classes for the optimization space classes.

Created on Fri Sep 13 12:54:19 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import csv
import os
from infrastructure.database.StaticResource import BaseStaticResource
from infrastructure.file.Metafile import BaseMetafile
from model.optimization.Space import \
    BaseModel, ParameterSpace, RegulationParameterSpace, TargetSpace


class SpaceNotFoundException(Exception):
    """
    The exception class for not finding the specified optimization space.
    """
    def __init__(self, spaceID: int, databaseName = ''):
        """
        Initialize a SpaceNotFoundException object.

        Parameters
        ----------
        spaceID : int
            The ideneity of a space.
        databaseName : str, optional
            The name of the queried database. The default is ''.

        Returns
        -------
        None.
        """
        self.actual = spaceID
        self.reference = databaseName
    
    def __str__(self) -> str:
        """
        Get a text representation of the exception.

        Returns
        -------
        str
            A string containing the description of the exception.
        """
        return 'The optimization space of ID {} was not found '\
               'in the {} database.'.format(self.actual, self.reference)

class BaseSpaceRepository:
    """
    The base repository class for parameter space classes.
    """
    def __init__(self, database: BaseStaticResource):
        """
        Initialize a BaseSpaceRepository object.

        Parameters
        ----------
        database : BaseStaticResource
            An object of sub-class of BaseStaticResource containing datasets.

        Returns
        -------
        None.
        """
        self.database = database
    
    def exists(self, ID: str) -> bool:
        """
        Determine if a dataset of given ID already exists in the database
        
        Parameters
        ----------
        ID : str
            The ID of the dataset to search.
        
        Returns
        -------
        bool
            Whether the specified dataset exists.
        """
        return self.database.exists(ID)
    
    def retrieveAll(self) -> list[BaseModel]:
        """
        Retrieve all spaces from the database

        Returns
        -------
        list
            A list of BaseModel objects.
        """
        return [self.retrieveByID(X) for X in self.database.idList()]
    
    def retrieveByID(self, ID: int) -> BaseModel:
        """
        Retrieve a BaseModel object with given ID from database

        Parameters
        ----------
        ID : int
            The identity of an regulation parameter space.
        
        Raises
        ------
        SpaceNotFoundException
            Raised when the dataset of specified ID does not exist.

        Returns
        -------
        BaseModel
            A BaseModel containing the parameter space for optimization.
        """
        raise NotImplementedError(BaseSpaceRepository.retrieveByID)
    
class RegulationParameterSpaceRepository(BaseSpaceRepository):
    """
    The repository class for RegulationParameterSpace classes.
    """
    mainFilename = 'parameter.csv'
    metaFilename = 'meta.txt'
    
    def retrieveByID(self, ID: int) -> RegulationParameterSpace:
        """
        Overrides BaseSpaceRepository.retrieveByID().
        """
        if not self.exists(ID):
            raise SpaceNotFoundException(ID)
        
        dataDir = self.database.dataDirectory(ID)
        
        # Parse the meta-file
        metaFile = BaseMetafile(os.path.join(dataDir, self.metaFilename))
        metaInformation = metaFile.get(['ID', 'name',
                                        'optimizationType', 'regulationType'])
        space = RegulationParameterSpace(ID = metaInformation['ID'], 
                                         name = metaInformation['name'], 
                                         optimizationType = 
                                         metaInformation['optimizationType'], 
                                         regulationType = 
                                         metaInformation['regulationType'],
                                         parameterList = [])
        
        # Parse the parameter file
        parametersList = []
        parameterFilename = os.path.join(dataDir, self.mainFilename)
        with open(parameterFilename, 'r') as parameterFile:
            data = csv.reader(parameterFile)
            columnNames = next(data)
            if 'ID' in columnNames:
                parametersList = list(data)
        
        if len(parametersList) == 0:
            return space
        
        parameterCount = len(parametersList[0]) - 1
        for i in range(1, parameterCount + 1):
            if i >= len(columnNames):
                break
            parameterSpace = ParameterSpace(index = i - 1, 
                                            name = columnNames[i], 
                                            min = min(float(X[i]) 
                                                      for X in parametersList), 
                                            max = max(float(X[i]) 
                                                      for X in parametersList))
            space.parameterList.append(parameterSpace)
        return space
   
class TargetSpaceRepository(BaseSpaceRepository):
    """
    The repository class for TargetSpace classes.
    """
    metaFilename = 'meta.txt'
    
    def retrieveByID(self, ID: int) -> TargetSpace:
        """
        Overrides BaseSpaceRepository.retrieveByID().
        """
        if not self.exists(ID):
            raise SpaceNotFoundException(ID)
        
        dataDir = self.database.dataDirectory(ID)
        
        # Parse the meta-file
        metaFile = BaseMetafile(os.path.join(dataDir, self.metaFilename))
        metaInformation = metaFile.get(['ID', 'name',
                                        'description', 'nodeCount'])
        space = TargetSpace(index = metaInformation['ID'], 
                            name = metaInformation['name'], 
                            description = metaInformation['description'], 
                            nodeCount = int(metaInformation['nodeCount']))
        return space
