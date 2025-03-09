#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 09:48:52 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import math
import scipy.signal as Signal
import scipy.stats as Stats
from infrastructure.math.number import floatRange
from infrastructure.math.signal import FWHM
from model.evaluation.Functional import BaseFunctional


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

class InverseLogSpanFunctional(ProbabilityFunctionalMixin, BaseFunctional):
    """
    The class for evaluating the inverse of span of logarithm of the value 
    of a temporal function.
    """
    builtinName = '1/logSpan'
    
    def __init__(self, name = 'InverseLogSpan', variableCount = 0, 
                 descrption = 'The inverse of span of logarithim of '
                              'an output'):
        """
        Initialize an InverseLogSpanFunctional object.
        """
        super().__init__(name, variableCount, descrption)
        self.maxValue = math.log(1e10)
        self.sampleQueue = []
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseFunctional.__call__().
        """
        # Get samples of function values
        values = self.takeSamples()
        if len(values) == 0:
            values = function()
        
        # Kernel density estimation for the distribution of logarithm of values
        logMinValue = math.log(min(X for X in values if X > 0))
        kernel = Stats.gaussian_kde([math.log(X) if X > 0 else logMinValue - 1 
                                     for X in values])
        
        # Resample from the estimated distribution
        logMinValue = math.log(min(values)) - 2
        logMaxValue = math.log(max(values)) + 2
        count = int(len(values) / 2)
        distribution = kernel(floatRange(logMinValue, logMaxValue, count))
        
        # Find all maxima
        peaks = Signal.find_peaks(distribution)[0]
        if len(peaks) < 2:
            # Unimodal distribution
            peakCoverage = FWHM(distribution.tolist())
        else:
            peakCoverage = max(peaks) - min(peaks)
        
        # Calculate the span
        span = peakCoverage * (logMaxValue - logMinValue) / count
        
        # Calculate the inverse of span
        return min(1 / span, self.maxValue) if span > 0 else self.maxValue

class InverseVarianceFunctional(ProbabilityFunctionalMixin, BaseFunctional):
    """
    The class for evaluating the inverse of variance of the value of 
    a temporal function.
    """
    builtinName = '1/variance'
    
    def __init__(self, name = 'InverseVariance', variableCount = 0, 
                 descrption = 'The inverse of variance of an output'):
        """
        Initialize an InverseLogVarianceFunctional object.
        """
        super().__init__(name, variableCount, descrption)
        self.maxValue = 1e10
        self.sampleQueue = []
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseFunctional.__call__().
        """
        # Get samples of function values
        values = self.takeSamples()
        if len(values) == 0:
            values = function()
        
        # Calculate the variance
        mean = sum(values) / len(values)
        variance = sum((X - mean) ** 2 for X in values) / len(values)
        
        # Calculate the inverse of variance
        return 1 / variance if variance > 0 else self.maxValue

class PopulationRatioFunctional(ProbabilityFunctionalMixin, BaseFunctional):
    """
    The class for evaluating the ratio of probability density between two 
    clusters (populations) of the value of a temporal function.
    """
    builtinName = 'populationRatio'
    
    def __init__(self, name = 'PopulationRatio', variableCount = 0, 
                 descrption = 'The ratio of probability density between two '
                              'clusters of an output'):
        """
        Initialize a PopulationRatioFunctional object.
        """
        super().__init__(name, variableCount, descrption)
        self.sampleQueue = []
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseFunctional.__call__().
        """
        # Get samples of function values
        values = self.takeSamples()
        if len(values) == 0:
            values = function()
        
        # Kernel density estimation for the distribution of logarithm of values
        logMinValue = math.log(min(X for X in values if X > 0))
        kernel = Stats.gaussian_kde([math.log(X) if X > 0 else logMinValue - 1 
                                     for X in values])
        
        # Resample from the estimated distribution
        logMinValue = math.log(min(values)) - 2
        logMaxValue = math.log(max(values)) + 2
        count = int(len(values) / 2)
        distribution = kernel(floatRange(logMinValue, 
                                         logMaxValue, count)).tolist()
        
        # Find all maxima
        peaks = Signal.find_peaks(distribution)[0]
        if len(peaks) < 2:
            # Unimodal distribution
            return math.inf
        
        # Split the distribution at the minima between two maxima
        peak1 = min(peaks)
        peak2 = max(peaks)
        cutoffIndex = peak1
        minima = math.inf
        for i in range(peak1 + 1, peak2):
            if distribution[i] < minima:
                cutoffIndex = i
                minima = distribution[i]
        cutoff = math.exp(logMinValue + \
                          cutoffIndex * (logMaxValue - logMinValue) / count)
        
        # Calculate the ratio of sample number between two groups
        subpopulationCount = sum(1 if X <= cutoff else 0 for X in values)
        return subpopulationCount / (len(values) - subpopulationCount)
