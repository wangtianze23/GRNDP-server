#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The database classes for persistent resources.

Created on Fri Sep 13 16:23:41 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import os
from infrastructure.config.Database import BaseDatabaseConfig


class BaseStaticResource:
    """
    The base class of database of static resource
    """
    def __init__(self, config = BaseDatabaseConfig(), name = ''):
        """
        Initialize a BaseStaticResource object
        
        Parameters
        ----------
        config : BaseDatabaseConfig, optional
            An object of BaseDatabaseConfig class or its sub-class, 
            containing database configuration.

        Returns
        -------
        None.
        """
        self.config = config
        self.path = os.path.join(self.config.staticPath, name)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
    
    def dataDirectory(self, ID: int) -> str:
        """
        Get the base directory of an entity

        Parameters
        ----------
        ID : int
            The identify of the target entity.

        Returns
        -------
        str
            The path to the target entity.
        """
        if ID > 0:
            return os.path.join(self.path, str(ID))
        else:
            return ''
    
    def count(self) -> int:
        """
        Count all entities.

        Returns
        -------
        int
            Total number of entities in the database.
        """
        return len(X for X in os.listdir(self.path) if X.isdigit())
        
    def idList(self) -> list[int]:
        """
        Get a list of IDs of all entities

        Returns
        -------
        list[int]
            A list of integers representing the IDs of all entities.
        """
        return sorted(int(X) for X in os.listdir(self.path) if X.isdigit())
    
    def exists(self, ID: int) -> bool:
        """
        Determine if an entity of given ID already exists in the database

        Parameters
        ----------
        ID : int
            The identity of the entity to search.

        Returns
        -------
        bool
            Whether the specified entity exists.
        """
        return ID in self.idList() 

class RegulatorDB(BaseStaticResource):
    """
    The class of database of parameters of regulators
    """
    def __init__(self, config = BaseDatabaseConfig()):
        super().__init__(config, 'regulator')

class TargetDB(BaseStaticResource):
    """
    The class of database of optimization targets
    """
    def __init__(self, config = BaseDatabaseConfig()):
        super().__init__(config, 'target')
