#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 20:51:56 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import math
import random


class RandomBoundedStep:
    """
    The class for making random bounded steps in global optimization.
    """
    def __init__(self, stepBoundaries: list[tuple], maxStep = 1, 
                 valueBoundaries: list[tuple] = None, seed: int = None):
        """
        Initialize a RandomBoundedStep object.

        Parameters
        ----------
        stepBoundaries : list[tuple]
            A list of tuples of numeric values indicating the boundary of step 
            for each parameter.
        maxStep : float, optional
            A numeric value indicating the maximum absolute step size. 
            The default is 1.
        valueBoundaries : list[tuple] or NoneType, optional
            A list of tuples of numeric values indicating the boundary for  
            each parameter, or None if all parameters are unbounded.
            The default is None.
        seed : int or None, optional
            An integer fed to the RNG, or None if no fixed seed is used.
            The default is None.

        Returns
        -------
        None.

        """
        self.maxStep = abs(maxStep)
        self.stepBoundaries = [(max(-self.maxStep, min(Y)), 
                                min(self.maxStep, max(Y))) 
                               for Y in stepBoundaries]
        if valueBoundaries is None:
            valueBoundaries = [(-math.inf,math.inf)] * len(self.stepBoundaries)
        self.valueBoundaries = valueBoundaries
        self.seed = seed
        self.stepCount = 0

    def __call__(self, values: list):
        """
        Calculate the step with a given vector.

        Parameters
        ----------
        values : list
            A list of numeric values based on which steps are made.

        Returns
        -------
        list
            A list of numeric values representing the step size for each value.
            The length of the list equals to the length of **values**.
        """
        self.stepCount += 1
        if self.seed is None:
            random.seed(None)
        else:
            random.seed(self.seed + self.stepCount)
        
        boundaryCount = len(self.stepBoundaries)
        if boundaryCount == len(values):
            boundaries = self.stepBoundaries
        elif boundaryCount < len(values):
            boundaries = self.stepBoundaries + \
                         [(-self.maxStep, self.maxStep)] * \
                          (len(values) - boundaryCount)
        else:
            boundaries = self.stepBoundaries[:len(values)]
        return [max(min(X + random.uniform(Y[0], Y[1]), Z[1]), Z[0]) 
                for X, Y, Z in zip(values, boundaries, self.valueBoundaries)]
