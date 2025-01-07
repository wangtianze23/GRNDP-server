#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 20:22:38 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from infrastructure.math.number import floatRange


class BaseSampler:
    """
    The base class for sample classes.
    """
    def __init__(self, variableRanges: list[tuple]):
        """
        Initialize a BaseSampler object.

        Parameters
        ----------
        variableRanges : list[tuple]
            A list of tuple of (int, int) representing the sampling range for 
            each variable (dimension).

        Returns
        -------
        None.
        """
        self.variableRanges = variableRanges
    
    def setVaribleRange(self, index: int, variableRange: tuple):
        """
        Set the range for a specific variable.

        Parameters
        ----------
        index : int
            The index of a variable.
        variableRange : tuple
            A tuple of (float, float) representing the lower and the upper 
            bound of the variable.

        Returns
        -------
        None.
        """
        if index < len(self.variableRanges):
            self.variableRanges[index] = variableRange
    
    def sample(self, sampleCount: list[int]) -> list[list]:
        """
        Get a specified number of samples.

        Parameters
        ----------
        sampleCount : list[int]
            A list of integers indicating the number of samples for each 
            variable.

        Returns
        -------
        list[list]
            A list of list of numeric values representing the sampled values 
            for each variable. The length of the outer list equals to 
            the number of variables, and the length of the inner list equals 
            to the number of samples for each variables.
        """
        raise NotImplementedError(BaseSampler.sample)

class LinearSampler(BaseSampler):
    """
    The sampler for sampling on linear spaces.
    """
    def sample(self, sampleCount: list[int]) -> list[list]:
        """
        Overrides BaseSampler.sample().
        """
        return [floatRange(X[0], X[1], Y) 
                for X, Y in zip(self.variableRanges, sampleCount)]

class LogarithmicSampler(BaseSampler):
    """
    The sampler for sampling on a logarithmic spaces.
    """
    def sample(self, sampleCount: list[int]) -> list[list]:
        """
        Overrides BaseSampler.sample().
        """
        return [floatRange(X[0], X[1], Y, True) 
                for X, Y in zip(self.variableRanges, sampleCount)]
