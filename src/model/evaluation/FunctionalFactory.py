#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 21:10:29 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.evaluation.Functional import BaseFunctionalTarget
from model.evaluation.BuiltinFunctional import \
    MinimumFunctionalTarget, MaximumFunctionalTarget, \
    InverseMinimumFunctionalTarget, InverseMaximumFunctionalTarget, \
    FWHMTarget


class BuiltinFunctionalFactory:
    """
    The factory class for built-in functional classes.
    """
    @staticmethod
    def createFromBuiltinName(name: str) -> BaseFunctionalTarget:
        """
        Construct a BaseFunctionalTarget object from its representative name.

        Parameters
        ----------
        name : str
            A string representing the internal name of a built-in functional 
            object.

        Returns
        -------
        BaseFunctionalTarget
            A BaseFunctionalTarget of the specified name.
        """
        for target in \
            (MinimumFunctionalTarget, MaximumFunctionalTarget, 
             InverseMinimumFunctionalTarget, InverseMaximumFunctionalTarget, 
             FWHMTarget):
            if target.builtinName == name:
                return target()
