#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 20:34:36 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import math
import sys


def floatRange(start: float, stop: float, length: int, 
               logarithm = False) -> list:
    """
    Generate a list of float numbers in the given range.

    Parameters
    ----------
    start : float
        A float number representing the lower bound (included).
    stop : float
        A float number representing the upper bound (not included).
    length : int
        An integer indicating the total number of values to generate.
    logarithm : bool, optional
        A boolean indicating whether numbers should be equally spaced 
        in the logarithmic scale instead of linear scale. 
        The default is False.

    Returns
    -------
    list
        A list of generated float numbers.
    """
    if start <= stop and length >= 1:
        if length > 1:
            if logarithm:
                start = math.log(max(start, sys.float_info.epsilon))
                stop = math.log(max(stop, sys.float_info.epsilon))
                step = (stop - start) / (length - 1)
                return [math.exp(start + step * i) for i in range(0, length)]
            else:
                step = (stop - start) / (length - 1)
                return [start + step * i for i in range(0, length)]
        else:
            return [start]
    else:
        return []

def intersectRange(range1: tuple, range2: tuple) -> tuple:
    """
    Get the intersection of two ranges.

    Parameters
    ----------
    range1 : tuple
        A tuple of (float, float) representing a range.
    range2 : tuple
        A tuple of (float, float) representing another range.

    Returns
    -------
    tuple or NoneType
        A tuple of (float, float) representing the intersection of the 
        two ranges, or None if the two ranges have no intersection.
    """
    result=(range1[0] if range2[0] is None else range2[0] if range1[0] is None 
            else (max(range1[0], range2[0])), 
            range1[1] if range2[1] is None else range2[1] if range1[1] is None 
            else (min(range1[1], range2[1])))
    if result[0] <= result[1]:
        return result
    return None

def intersectRanges(ranges: list[tuple]) -> tuple:
    """
    Get the intersection of multiple ranges.

    Parameters
    ----------
    ranges : list[tuple]
        A list of of (float, float) representing a list of ranges.

    Returns
    -------
    tuple
        A tuple of (float, float) representing the intersection of all the 
        ranges, or None if the ranges have no intersection.
    """
    if len(ranges) == 0:
        return tuple()
    result = ranges[0]
    for i in range(1, len(ranges)):
        result = intersectRange(result, ranges[i])
        if result is None:
            return None
    return result

def centroid(values: list[tuple]) -> tuple:
    """
    Calculate the dimension-wise geometric median of a list of vectors.

    Parameters
    ----------
    values : list[tuple]
        A list of tuple of numeric values representing the multidimensional 
        vectors. The length of the outer list equals to the number of vectors, 
        and the length of the inner list equals to the number of dimensions.

    Returns
    -------
    tuple
        A tuple of numeric values representing the geometric median. 
        The length of the tuple equals to the number of dimensions.
    """
    if len(values) == 0:
        return tuple()
    return tuple(math.prod(X[i] for X in values) ** (1 / len(values)) 
                 for i in range(0, len(values[0])))

def geometricMean(values: list, minValue = 1e-10) -> float:
    """
    Calculate the geometric mean of a list of numeric values.

    Parameters
    ----------
    values : list
        A list of numeric values whose geometric mean is to be calculated.
    minValue : float, optional
        The minimum value to be considered in the calculation. 
        The default is 1e-10.

    Returns
    -------
    float
        A float number representing the geometric mean of the given values.
    """
    validValues = [X for X in values if X > minValue]
    if len(validValues) > 1:
        return math.prod(validValues) ** (1 / len(validValues))
    if len(validValues) == 1:
        if len(values) > 1:
            return math.sqrt(validValues[0] * minValue)
        return validValues[0]
    return minValue

def kNN(value: tuple, neighbours: list[tuple], k = 1) -> list[tuple]:
    """
    Find the k-nearest neighbours (KNN) of a vector among a list of vectors.

    Parameters
    ----------
    value : tuple
        A tuple of numeric values representing a vector. The length of 
        the tuple equals to the number of dimensions.
    neighbours : list[tuple]
        A list of tuple of numeric values representing the multidimensional 
        vectors. The length of the outer list equals to the number of vectors, 
        and the length of the inner list equals to the number of dimensions.
    k : int, optional
        An integer indicating the number of neighbours to return. 
        The default is 1.

    Returns
    -------
    list[tuple]
        A list of tuple of numeric values representing the **k** nearest 
        neighbours of **value** among **neighbours**. The length of the list 
        equals to **k**, and the length of the tuple equals to the number of 
        dimensions.
    """
    distances = [sum((x - y) ** 2 for x,y in zip(X,value)) for X in neighbours]
    return [distances.index(X) for X in sorted(distances)[:k]]
