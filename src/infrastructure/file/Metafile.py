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
    
    @staticmethod
    def serializeArray(values: list) -> str:
        """
        Serialize a list of values into a string.

        Parameters
        ----------
        values : list
            A list or tuple of values. Each element must be of one of 
            the following types: int, float, str.

        Returns
        -------
        str
            A string representing the serialized array.
        """
        return '[{}]'.format(','.join('\'{}\''.format(X.replace('\\', '\\\\').
                                                        replace('\'', '\\\'').
                                                        replace(',', '\\x2C')) 
                                      if type(X) == str else str(X) 
                                      for X in values))
    
    @staticmethod
    def unserializeArray(value: str) -> list:
        """
        Unserialize a string into a list of values.

        Parameters
        ----------
        value : str
            A string representing the values to unserialize into an array.
            The target values must be of one of the following types: 
            int, float, str.

        Returns
        -------
        str
            A list of unserialized values.
        """
        if len(value) >= 2 and value.startswith('[') and value.endswith(']'):
            values = [X.strip() for X in value[1 : -1].split(',')]
            return [X[1 : -1].replace('\\x2C', ',').replace('\\\'', '\'').
                              replace('\\\\', '\\') 
                    if X.startswith('\'') and X.endswith('\'') 
                    else float(X) if '.' in X or 'e+' in X or 'e-' in X 
                    else int(X)
                    for X in values]
        return []
    
    @staticmethod
    def serialize(value: object) -> str:
        """
        Serialize a value into a string.

        Parameters
        ----------
        values : object
            A value to serialize. It must be of one of the following types: 
            int, float, str, list[int], list[float], list[str].

        Returns
        -------
        str
            A string representing the serialized value.
        """
        if type(value) == list:
            return BaseMetafile.serializeArray(value)
        if type(value) == str:
            return value.replace('\\', '\\\\').replace('\'', '\\\'').\
                         replace('\r\n', '\\n').replace('\n', '\\n')
        return str(value)
    
    @staticmethod
    def unserialize(value: str) -> object:
        """
        Serialize a value into a string.

        Parameters
        ----------
        values : str
            A string containing the value to unserialize. 
            The target value must be of one of the following types: 
            str, list[int], list[float], list[str].

        Returns
        -------
        object
            An object representing the unserialized value.
        """
        if value.startswith('[') and value.endswith(']'):
            return BaseMetafile.unserializeArray(value)
        return value.replace('\\n', '\n').replace('\\\'', '\'').\
                     replace('\\\\', '\\')
    
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
                result[key] = self.unserialize(fields[1])
        metaFile.close()
        return result
    
    def put(self, values: dict):
        """
        Put a list of named values.

        Parameters
        ----------
        values : dict
            A list of key-value pairs representing named values. The values 
            must be one of the following types: int, float, str, list[int], 
            list[float], list[str].

        Returns
        -------
        None.
        """
        metaFile = open(self.filename, 'w')
        metaFile.writelines('{}={}\n'.format(key, self.serialize(value)) 
                            for key, value in values.items())
