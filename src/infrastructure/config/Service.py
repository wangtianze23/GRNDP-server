#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The configuration classes for services.

Created on Fri Sep 13 12:37:14 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import tempfile
from infrastructure.config.Database import BaseDatabaseConfig
from infrastructure.config.Plot import BasePlotConfig


class BaseServiceConfig:
    """
    The base class of service configuration.
    """
    def __init__(self, staticResourcePath = '../db/static', 
                 temporaryResourcePath = '', plotOptions = None):
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
        plotOptions : dict or NoneType, optional
            A dictionary containing strings pointing to arbitrary values that 
            represent the general configuration parameters of plot services, 
            or NoneType if the default settings shall be used.
            The default is None.

        Returns
        -------
        None.
        """
        self.staticResource = BaseDatabaseConfig(staticResourcePath)
        
        if len(temporaryResourcePath) == 0:
            temporaryResourcePath = tempfile.gettempdir()
        self.temporaryResource = BaseDatabaseConfig(temporaryResourcePath)
        
        self.plotConfiguration = BasePlotConfig()
        if type(plotOptions) is dict:
            for name, value in plotOptions.items():
                if name in dir(self.plotConfiguration):
                    setattr(self.plotConfiguration, name, value)
