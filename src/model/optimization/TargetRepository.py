#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repository classes for the optimization target classes.

Created on Wed Jan  8 15:51:35 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import os
from infrastructure.database.StaticResource import BaseStaticResource
from infrastructure.file.Metafile import BaseMetafile
from model.optimization.Target import BaseTarget


class TargetNotFoundException(Exception):
    """
    The exception class for not finding the specified optimization target.
    """
    def __init__(self, spaceID: int, databaseName = ''):
        """
        Initialize a TargetNotFoundException object.

        Parameters
        ----------
        spaceID : int
            The ideneity of a target.
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
        return 'The optimization target of ID {} was not found '\
               'in the {} database.'.format(self.actual, self.reference)

class BaseTargetRepository:
    """
    The base repository class for Target classes.
    """
    metaFilename = 'meta.txt'
    
    def __init__(self, database: BaseStaticResource):
        """
        Initialize a BaseTargetRepository object.

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
    
    def retrieveAll(self) -> list[BaseTarget]:
        """
        Retrieve all targets from the database

        Returns
        -------
        list
            A list of BaseModel objects.
        """
        return [self.retrieveByID(X) for X in self.database.idList()]
    
    def retrieveByID(self, ID: int) -> BaseTarget:
        """
        Retrieve an optimization target with given ID from database

        Parameters
        ----------
        ID : int
            The identity of an optimization target.
        
        Raises
        ------
        TargetNotFoundException
            Raised when the dataset of specified ID does not exist.

        Returns
        -------
        BaseTarget
            A BaseTarget object containing the target for optimization.
        """
        if not self.exists(ID):
            raise TargetNotFoundException(ID, 'optimization target')
        
        dataDir = self.database.dataDirectory(ID)
        
        # Parse the meta-file
        metaFile = BaseMetafile(os.path.join(dataDir, self.metaFilename))
        metaInformation = metaFile.get(['ID', 'name', 'builtin', 
                                        'description', 'nodeCount'])
        target = BaseTarget(ID = metaInformation['ID'], 
                            variableCount = int(metaInformation['nodeCount']), 
                            name = metaInformation['name'], 
                            builtin = metaInformation['builtin'], 
                            description = metaInformation['description'])
        return target
