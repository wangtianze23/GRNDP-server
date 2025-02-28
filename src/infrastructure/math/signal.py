#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 20:53:26 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import math
import scipy.optimize as Optimize


def FWHM(values: list[float]) -> float:
    """
    Estimate the full width at half maximum (FWHM) of a potential peak 
    in a series of scalars.

    Parameters
    ----------
    values : list[float]
        A list of numeric values representing a discretized series of signals.

    Returns
    -------
    float
        A float value representing the estimated FWHM.
    """
    maximum = max(values)
    maxIndex = values.index(maximum)
    leftIndex = next(iter(i for i in range(maxIndex, -1, -1) 
                          if values[i] <= maximum / 2), None)
    rightIndex = next(iter(i for i in range(maxIndex, len(values)) 
                           if values[i] <= maximum / 2), None)
    if leftIndex is None and rightIndex is None:
        return len(values)
    if leftIndex is None:
        return (rightIndex - maxIndex) * 2
    if rightIndex is None:
        return (maxIndex - leftIndex) * 2
    return rightIndex - leftIndex

def fitGaussianPeaks(values: list, positions: list[int]) -> tuple[list]:
    """
    Deconvolute a series of scalars into Gaussian peaks with known means.

    Parameters
    ----------
    values : list[float]
        A list of numeric values representing a discretized series of signals.
    positions : list[int]
        A list of integers indicating the mean for each Gaussian peak.

    Returns
    -------
    tuple[list]
        A tuple of (list[float], list[float]). The first list contains 
        the estimated standard deviation for each peak, and the second list 
        contains the estimated scaling factor for each peak. The length of 
        both list equals to the length of **positions**.
    """
    if len(positions) == 0:
        return []
    
    peakCount = len(positions)
    if len(positions) > 1:
        width = max(positions) - min(positions)
    else:
        width = FWHM(values)
    initialHeights = [values[i] for i in positions]
    initialWidth = [width / peakCount] * peakCount
    heightRanges = [(0, X) for X in initialHeights]
    widthRanges = [(1, width * 2)] * peakCount
    result = Optimize.minimize(lambda X: 
                               sum(sum((Y - 
                                        math.exp(-((k - j) / X[i]) ** 2 / 2) * 
                                        X[peakCount + i]) ** 2 
                                       for k, Y in enumerate(values))
                                   for i, j in enumerate(positions)), 
                               x0 = initialWidth + initialHeights, 
                               bounds = widthRanges + heightRanges, 
                               method = 'L-BFGS-B')
    return (result['x'].tolist()[:peakCount], result['x'].tolist()[peakCount:])
