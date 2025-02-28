#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 19:20:13 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.evaluation.Sampler import BaseSampler, LinearSampler


class BaseFunctional:
    """
    The base class for evaluating a target on a function.
    """
    def __init__(self, name: str, variableCount: int, descrption = ''):
        """
        Initialize a BaseFunctional object.

        Parameters
        ----------
        name : str
            The name of the target.
        variableCount : int
            The number of variables of the function object.
        descrption : str, optional
            A string representing the description of the target. 
            The default is an empty string.

        Returns
        -------
        None.
        """
        self.name = name
        self.descrption = descrption
        self.variableCount = variableCount
        self.variableRanges = [(0, 100)] * variableCount
    
    def __call__(self, function: object) -> float:
        """
        Evaluate the target on a function of defined ranges.

        Parameters
        ----------
        function : object
            A callable object representing the function to evaluate.

        Returns
        -------
        float
            The evaluated target.
        """
        raise NotImplementedError(BaseFunctional.__call__)
    
    def setVaribleRange(self, index: int, variableRange: tuple):
        """
        Set the range for a specific variable.

        Parameters
        ----------
        index : int
            The index of a variable.
        variableRange : tuple
            A tuple of (float, float) representing the lower and the upper 
            bound of the variable, between which the target shall be evaluated.

        Returns
        -------
        None.
        """
        if index < len(self.variableRanges):
            self.variableRanges[index] = variableRange

class DiscreteFunctional(BaseFunctional):
    """
    The class for evaluating a target on a function of discrete variables.
    """
    def __init__(self, name: str, variableCount: int, descrption = '', 
                 sampleCount = 20):
        """
        Initialize a DiscreteFunctional object.

        Parameters
        ----------
        name : str
            The name of the target.
        variableCount : int
            The number of variables of the function object.
        descrption : str, optional
            A string representing the description of the target. 
            The default is an empty string.
        sampleCount : int, optional
            The number of samples for each variable when evaluating the target.
            The default is 20.

        Returns
        -------
        None.
        """
        super().__init__(name, variableCount, descrption)
        self.sampleCounts = [sampleCount] * self.variableCount
        self.sampler = LinearSampler(self.variableRanges)

    def setSampler(self, index: int, sampler: BaseSampler):
        """
        Set the sampler for each variable.

        Parameters
        ----------
        index : int
            The index of a variable.
        sampler : BaseSampler
            A BaseSampler object used to get samples of the specified variable.

        Returns
        -------
        None.
        """
        if index < len(self.sampler):
            self.sampler[index] = sampler
    
    def setVaribleRange(self, index: int, variableRange: tuple):
        """
        Overrides BaseFunctional.setVaribleRange().
        """
        super().setVaribleRange(index, variableRange)
        self.sampler.setVaribleRange(index, variableRange)
