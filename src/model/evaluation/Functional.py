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
            The name of the functional.
        variableCount : int
            The number of variables of the function object.
        descrption : str, optional
            A string representing the description of the functional. 
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
            The name of the functional.
        variableCount : int
            The number of variables of the function object.
        descrption : str, optional
            A string representing the description of the functional. 
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

class ProbabilityFunctionalMixin:
    """
    Mixin class (interface) for evaluating the probability density of 
    a target on a function.
    Attributes required in derived classes:
        - sampleQueue: list[list[float]]
    """
    def appendSamples(self, values: list[float]):
        """
        Append a list of samples to the sample queue for evaluation in future.

        Parameters
        ----------
        values : list[float]
            A list of float values representing the sampled values of 
            the target.

        Returns
        -------
        None.
        """
        self.sampleQueue.append(values)
    
    def takeSamples(self) -> list[float]:
        """
        Take a list of samples out of the sample queue for evaluation.

        Returns
        -------
        list[float]
            A list of float values representing a series of sampled values of 
            the target.
        """
        if len(self.sampleQueue) > 0:
            return self.sampleQueue.pop(0)
        return []

class JointFunctional(BaseFunctional):
    """
    The base class for jointly evaluating multiple functionals.
    """
    def __init__(self, name: str, variableCount: int, 
                 components: list[BaseFunctional], descrption = ''):
        """
        Initialize a JointFunctional object.

        Parameters
        ----------
        name : str
            The name of the functional.
        variableCount : int
            The number of variables of the function object.
        components : list[BaseFunctional]
            A list of BaseFunctional objects representing the component 
            functionals to evaluate jointly.
        descrption : str, optional
            A string representing the description of the functional. 
            The default is an empty string.

        Returns
        -------
        None.
        """
        super().__init__(name, variableCount, descrption = descrption)
        self.components = components
        self.probabilityComponents = \
            [X for X in components if isinstance(X,ProbabilityFunctionalMixin)]
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseFunctional.__call__().
        """
        return self.components[0](function)
    
    def evaluate(self, function: object) -> list[float]:
        """
        Evaluate the functional on a function of defined ranges.

        Parameters
        ----------
        function : object
            A callable object representing the function to evaluate.

        Returns
        -------
        list[float]
            A list of float numbers representing the target evaluated on 
            each component functional.
        """
        self.prepare(function)
        return [X(function) for X in self.components]
    
    def prepare(self, function: object):
        """
        Prepare the component functionals before evaluation.

        Parameters
        ----------
        function : object
            A callable object representing the function to evaluate.

        Returns
        -------
        None.
        """
        if len(self.probabilityComponents) > 1:
            values = function()
            for component in self.probabilityComponents:
                component.appendSamples(values)
