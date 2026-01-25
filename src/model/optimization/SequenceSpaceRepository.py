#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repository classes for the optimization sequence space classes.

Created on Mon Mar 17 15:45:05 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import os
from infrastructure.database.StaticResource import BaseStaticResource
from infrastructure.file.Metafile import BaseMetafile
from model.optimization.SequenceSpace import RegulationSequenceSpace
from model.optimization.SequenceSpaceFactory import \
    RegulationSequenceSpaceFactory


class SpaceNotFoundException(Exception):
    """
    The exception class for not finding the specified sequence space.
    """
    def __init__(self, spaceID: int, databaseName = ''):
        """
        Initialize a SpaceNotFoundException object.

        Parameters
        ----------
        spaceID : int
            The identity of a space.
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
        return 'The sequence space of ID {} was not found '\
               'in the {} database.'.format(self.actual, self.reference)

class RegulationSequenceSpaceRepository:
    """
    The repository class for RegulationSequenceSpace classes.
    """
    mainFilename = 'sequence.csv'
    metaFilename = 'meta.txt'
    
    def __init__(self, database: BaseStaticResource):
        """
        Initialize a RegulationSequenceSpaceRepository object.

        Parameters
        ----------
        database : BaseStaticResource
            An object of sub-class of BaseStaticResource containing spaces.

        Returns
        -------
        None.
        """
        self.database = database
    
    def exists(self, ID: int) -> bool:
        """
        Determine if a space of given ID already exists in the database
        
        Parameters
        ----------
        ID : int
            The identity of the space to search.
        
        Returns
        -------
        bool
            Whether the specified space exists.
        """
        return self.database.exists(ID)
    
    def retrieveAll(self) -> list[RegulationSequenceSpace]:
        """
        Retrieve all spaces from the database

        Returns
        -------
        list
            A list of BaseModel objects.
        """
        return [self.retrieveByID(X) for X in self.database.idList()]
    
    def retrieveByID(self, ID: int) -> RegulationSequenceSpace:
        """
        Retrieve a regulation sequence space with given ID from database

        Parameters
        ----------
        ID : int
            The identity of a regulation sequence space.
        
        Raises
        ------
        SpaceNotFoundException
            Raised when the dataset of specified ID does not exist.

        Returns
        -------
        RegulationSequenceSpace
            A RegulationSequenceSpace object containing the sequence space 
            for optimization.
        """
        if not self.exists(ID):
            raise SpaceNotFoundException(ID, 'regulation sequence')
        
        dataDir = self.database.dataDirectory(ID)
        
        # Parse the meta-file
        metaFile = BaseMetafile(os.path.join(dataDir, self.metaFilename))
        metaInformation = metaFile.get(['ID', 'name', 'optimizationType'])
        
        if metaInformation['optimizationType'] in ('dataset', 'generator'):
            sequenceFilename = os.path.join(dataDir, self.mainFilename)
            if os.path.exists(sequenceFilename):
                space = RegulationSequenceSpaceFactory.\
                                        createFromFile(sequenceFilename, 
                                                       metaInformation['ID'])
            else:
                space = RegulationSequenceSpace(metaInformation['ID'])
        else:
            space = RegulationSequenceSpace(metaInformation['ID'])
        space.name = metaInformation['name']
        space.source = metaInformation['optimizationType']
        return space
