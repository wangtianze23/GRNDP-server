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
    
    def dataDirectory(self, datasetID: int) -> str:
        """
        Get the base directory of a dataset

        Parameters
        ----------
        datasetID : str
            The identify of the target dataset.

        Returns
        -------
        str
            The path to the target dataset.
        """
        if datasetID > 0:
            return os.path.join(self.path, str(datasetID))
        else:
            return ''
    
    def count(self) -> int:
        """
        Count all datasets.

        Returns
        -------
        int
            Total number of datasets in the database.
        """
        return len(os.listdir(self.path))
        
    def idList(self) -> list[str]:
        """
        Get a list of IDs of all datasets

        Returns
        -------
        list
            A list of strings representing IDs of all datasets.
        """
        return [int(X) for X in os.listdir(self.path) if X.isdigit()]
    
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
