#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The file classes for parsing meta-file of databases.

Created on Fri Sep 13 18:37:53 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class BaseMetafile:
    """
    The base class for parsing meta-files.
    """
    def __init__(self, filename: str):
        """
        Initialize a BaseMetafile object.

        Parameters
        ----------
        filename : str
            The name of the meta-file.

        Returns
        -------
        None.
        """
        self.filename = filename
    
    def get(self, names: list) -> dict:
        """
        Get a list of values associated with specified field names.

        Parameters
        ----------
        fields : list
            A list of string indicating the fields to retrieve.

        Returns
        -------
        dict
            A list of values associated with the specified names.
        """
        result = {}
        try:
            metaFile = open(self.filename, 'r')
        except:
            return result
        while True:
            line = metaFile.readline()
            if len(line) == 0:
                break
            
            fields = line.strip().split('=')
            if len(fields) != 2:
                continue
            
            key = fields[0].strip()
            if key in names:
                if fields[1].startswith('[') and fields[1].endswith(']'):
                    tempValues = [X.strip() 
                                  for X in fields[1][1 : -1].split(',')]
                    result[key] = [X[1 : -1] 
                                   if X.startswith('\'') and X.endswith('\'')
                                   else X 
                                   for X in tempValues]
                else:
                    if fields[1].startswith('\'') and fields[1].endswith('\''):
                        result[key] = fields[1][1 : -1]
                    else:
                        result[key] = fields[1]
        metaFile.close()
        return result
    
    def put(self, values: dict):
        """
        Put a list of named values.

        Parameters
        ----------
        values : dict
            A list of key-value pairs representing named values.

        Returns
        -------
        None.
        """
        metaFile = open(self.filename, 'w')
        metaFile.writelines('{}={}\n'.format(key, value) 
                            for key, value in values.items())
