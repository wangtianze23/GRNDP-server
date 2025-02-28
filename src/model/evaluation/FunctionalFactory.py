#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 21:10:29 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.evaluation.Functional import BaseFunctional
from model.evaluation.FunctionalException import FunctionalTypeNotSupported
from model.evaluation.BuiltinFunctional import \
    MinimumFunctional, MaximumFunctional, \
    InverseMinimumFunctional, InverseMaximumFunctional, FWHMFunctional
from model.evaluation.BuiltinProbabilityFunctional import \
    PopulationRatioFunctional


class BuiltinFunctionalFactory:
    """
    The factory class for built-in functional classes.
    """
    @staticmethod
    def createFromBuiltinName(name: str, valueRanges = None) -> BaseFunctional:
        """
        Construct a BaseFunctional object from its representative name.

        Parameters
        ----------
        name : str
            A string representing the internal name of a built-in functional 
            object.
        valueRanges : list[tuple] or NoneType, optional
            A list of tuples of (float, float) representing the lower and 
            upper boundary for the value of each specified node, or None if 
            the default boundaries shall be used. The length of the list must 
            equal to the length of **nodeIndexes**.
            The default is None.

        Returns
        -------
        BaseFunctional
            A BaseFunctional of the specified name.
        """
        for targetClass in \
            (MinimumFunctional, MaximumFunctional, 
             InverseMinimumFunctional, InverseMaximumFunctional, 
             FWHMFunctional, PopulationRatioFunctional):
            if targetClass.builtinName == name:
                target = targetClass()
                for i, valueRange in enumerate(valueRanges):
                    # The first range corresponds to the function value
                    # and the rest ranges correspond to the function variables
                    if i > 0 and valueRange is not None:
                        target.setVaribleRange(i - 1, valueRange)
                return target
        
        raise FunctionalTypeNotSupported(name)
