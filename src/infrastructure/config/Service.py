#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The configuration classes for services.

Created on Fri Sep 13 12:37:14 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import tempfile
from infrastructure.config.Database import BaseDatabaseConfig


class BaseServiceConfig:
    """
    The base class of service configuration.
    """
    def __init__(self, staticResourcePath = '../db/static', 
                 temporaryResourcePath = ''):
        """
        Initialize a BaseServiceConfig object.

        Parameters
        ----------
        staticResourcePath : str, optional
            Path to the root directory containing static resources. 
            The default is '../db/static'.
        temporaryResourcePath : str, optional
            Path to the directory to store temporary resources.
            The default is an empty string, i.e. using the default temporary 
            directory specified of the system.

        Returns
        -------
        None.
        """
        self.staticResource = BaseDatabaseConfig(staticResourcePath)
        
        if len(temporaryResourcePath) == 0:
            temporaryResourcePath = tempfile.gettempdir()
        self.temporaryResource = BaseDatabaseConfig(temporaryResourcePath)
