#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:50:50 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class BaseTarget:
    """
    The base class for optimization target classes.
    """
    def __init__(self, ID: int, variableCount: int, name = '', 
                 description = ''):
        """
        Initialize a BaseTarget object.

        Parameters
        ----------
        ID : int
            A integer representing the identity of the target.
        variableCount : int
            The number of variables of the function object.
        name : str
            The name of the target. 
            The default is an empty string.
        builtin : str, optional
            A string representing the internal name of the target if it is 
            a built-in target.
            The default is an empty string, i.e. the target is not built-in.
        descrption : str, optional
            A string representing the description of the target. 
            The default is an empty string.

        Returns
        -------
        None.
        """
        self.name = name
        self.ID = ID
        self.variableCount = variableCount
        self.description = description

class BuiltinTarget(BaseTarget):
    """
    The class for built-in optimization targets.
    """
    def __init__(self, ID: int, variableCount: int, functionalNames: list[str],
                 name = '', description = ''):
        """
        Initialize a BuiltinTarget object.

        Parameters
        ----------
        ID : int
            A integer representing the identity of the target.
        variableCount : int
            The number of variables of the function object.
        functionalNames : list[str]
            A list of strings representing the internal name of each component 
            functionals.
        name : str
            The name of the target. 
            The default is an empty string.
        descrption : str, optional
            A string representing the description of the target. 
            The default is an empty string.

        Returns
        -------
        None.
        """
        super().__init__(ID, variableCount, name = name, 
                         description = description)
        self.functionalNames = functionalNames
