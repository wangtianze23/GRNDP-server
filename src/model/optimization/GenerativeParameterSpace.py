#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:36:59 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.optimization.ParameterSpace import RegulationParameterSpace


class GenerativeSpace:
    """
    The mixin class for generative parameter spaces.
    """
    def feasible(value: list) -> bool:
        """
        Check if a vector value can be generated.

        Parameters
        ----------
        value : list
            A list of numeric values representing a vector.

        Returns
        -------
        bool
            Whether the specified vector value can be generated.
        """
        raise NotImplementedError(GenerativeSpace.feasible)

class GenerativeRegulationParameterSpace(GenerativeSpace, 
                                         RegulationParameterSpace):
    """
    The class for regulation parameters in a generative space.
    """
    def feasible(self, value: list) -> bool:
        """
        Overrides GenerativeSpace.feasible().
        """
        return all(True if Y is None else X in Y 
                   for X, Y in zip(value, self.boundaries))
