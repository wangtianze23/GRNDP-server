#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The configuration classes for database.

Created on Fri Sep 13 12:38:03 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class BaseDatabaseConfig:
    """
    The base class of database configuration.
    """
    def __init__(self, staticPath = '../db/static'):
        """
        Initialize a BaseDatabaseConfig object.

        Parameters
        ----------
        staticPath : str, optional
            Path to the root directory containing static resources. 
            The default is '../db/static'.

        Returns
        -------
        None.
        """
        self.staticPath = staticPath
