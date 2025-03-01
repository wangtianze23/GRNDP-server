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
from infrastructure.math.signal import FWHM, fitGaussianPeaks
from model.evaluation.Functional import BaseFunctional, CompoundFunctional


class SubpopulationRatioFunctional(BaseFunctional):
    """
    The class for evaluating the ratio of probability density between two 
    potential clusters (subpopulations) of the value of a temporal function.
    """
    builtinName = 'subpopulationRatio'
    
    def __init__(self, name = 'SubpopulationRatio', variableCount = 0, 
                 descrption = 'The ratio of probability density between two '
                              'potential clusters of an output'):
        """
        Initialize a SubpopulationRatioFunctional object.
        """
        super().__init__(name, variableCount, descrption)
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseFunctional.__call__().
        """
        # Get samples of function values
        values = function()
        
        # Kernel density estimation for the distribution of logarithm of values
        logMinValue = math.log(min(X for X in values if X > 0))
        kernel = Stats.gaussian_kde([math.log(X) if X > 0 else logMinValue - 1 
                                     for X in values])
        
        # Resample from the estimated distribution
        logMinValue = math.log(min(values)) - 2
        logMaxValue = math.log(max(values)) + 2
        count = int(len(values) / 3)
        distribution = kernel(floatRange(logMinValue, 
                                         logMaxValue, count)).tolist()
        
        # Find all maxima
        peaks = Signal.find_peaks(distribution)[0]
        if len(peaks) < 2:
            # Unimodal distribution
            peakWidth = int(FWHM(distribution) / 2 + 0.5)
            peak1 = peaks[0] - peakWidth
            peak2 = peaks[0] + peakWidth
        else:
            peak1 = min(peaks[:2])
            peak2 = max(peaks[:2])
        _, peakHeights = fitGaussianPeaks(distribution, [peak1, peak2])
        
        return peakHeights[0] / peakHeights[1]

class InverseVarianceFunctional(BaseFunctional):
    """
    The class for evaluating the inverse of variance of probability density 
    of the value of a temporal function.
    """
    builtinName = '1/variance'
    
    def __init__(self, name = 'InverseVariance', variableCount = 0, 
                 descrption = 'The inverse of variance of probability density '
                              'of an output'):
        """
        Initialize an InverseVarianceFunctional object.
        """
        super().__init__(name, variableCount, descrption)
        self.maxValue = 1e10
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseFunctional.__call__().
        """
        # Get samples of function values
        values = function()
        
        # Calculate the variance
        mean = sum(values) / len(values)
        variance = sum((X - mean) ** 2 for X in values) / len(values)
        return 1 / variance if variance > 0 else self.maxValue

class PopulationRatioFunctional(CompoundFunctional):
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
        super().__init__(name, variableCount, 
                         [SubpopulationRatioFunctional(), 
                          InverseVarianceFunctional()], 
                         descrption = descrption)
        self.reduction = math.prod
