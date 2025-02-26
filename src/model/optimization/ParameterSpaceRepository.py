#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repository classes for the optimization parameter space classes.

Created on Fri Sep 13 12:54:19 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import os
from infrastructure.database.StaticResource import BaseStaticResource
from infrastructure.file.Metafile import BaseMetafile
from model.optimization.ParameterSpace import RegulationParameterSpace
from model.optimization.ParameterSpaceFactory import \
    DiscreteRegulationParameterSpaceFactory, \
    GenerativeRegulationParameterSpaceFactory


class SpaceNotFoundException(Exception):
    """
    The exception class for not finding the specified parameter space.
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

class RegulationParameterSpaceRepository:
    """
    The repository class for RegulationParameterSpace classes.
    """
    mainFilename = 'parameter.csv'
    metaFilename = 'meta.txt'
    
    def __init__(self, database: BaseStaticResource):
        """
        Initialize a RegulationParameterSpaceRepository object.

        Parameters
        ----------
        database : BaseStaticResource
            An object of sub-class of BaseStaticResource containing spaces.

        Returns
        -------
        None.
        """
        self.database = database
    
    def exists(self, ID: str) -> bool:
        """
        Determine if a space of given ID already exists in the database
        
        Parameters
        ----------
        ID : str
            The ID of the space to search.
        
        Returns
        -------
        bool
            Whether the specified space exists.
        """
        return self.database.exists(ID)
    
    def retrieveAll(self) -> list[RegulationParameterSpace]:
        """
        Retrieve all spaces from the database

        Returns
        -------
        list
            A list of BaseModel objects.
        """
        return [self.retrieveByID(X) for X in self.database.idList()]
    
    def retrieveByID(self, ID: int) -> RegulationParameterSpace:
        """
        Retrieve a regulation parameter space with given ID from database

        Parameters
        ----------
        ID : int
            The identity of a regulation parameter space.
        
        Raises
        ------
        SpaceNotFoundException
            Raised when the dataset of specified ID does not exist.

        Returns
        -------
        RegulationParameterSpace
            A RegulationParameterSpace object containing the parameter space 
            for optimization.
        """
        if not self.exists(ID):
            raise SpaceNotFoundException(ID, 'regulation parameter')
        
        dataDir = self.database.dataDirectory(ID)
        
        # Parse the meta-file
        metaFile = BaseMetafile(os.path.join(dataDir, self.metaFilename))
        metaInformation = metaFile.get(['ID', 'name',
                                        'optimizationType', 'regulationType'])
        
        if metaInformation['optimizationType'] == 'dataset':
            parameterFilename = os.path.join(dataDir, self.mainFilename)
            space = DiscreteRegulationParameterSpaceFactory.\
                            createFromFile(parameterFilename, 
                                           metaInformation['ID'], 
                                           metaInformation['regulationType'])
        elif metaInformation['optimizationType'] == 'generator':
            parameterFilename = os.path.join(dataDir, self.mainFilename)
            space = GenerativeRegulationParameterSpaceFactory.\
                            createFromFile(parameterFilename, 
                                           metaInformation['ID'], 
                                           metaInformation['regulationType'])
        else:
            space = RegulationParameterSpace(
                            ID = metaInformation['ID'], 
                            regulationType = metaInformation['regulationType'])
        space.name = metaInformation['name']
        space.source = metaInformation['optimizationType']
        return space
