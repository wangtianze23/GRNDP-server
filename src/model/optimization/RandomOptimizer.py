#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 20:51:56 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import random


class RandomBoundedStep:
    """
    The class for making random bounded steps in global optimization.
    """
    def __init__(self, maxStep = 1, stepBoundaries = [], seed = None):
        """
        Initialize a RandomBoundedStep object.

        Parameters
        ----------
        maxStep : float, optional
            A numeric value indicating the maximum absolute step size. 
            The default is 1.
        stepBoundaries : list, optional
            A list of tuples indicating the boundary of step for each 
            parameter. 
            The default is an empty list, i.e. the step size for all 
            parameters is unbounded.
        seed : int or None, optional
            An integer fed to the RNG, or None if no fixed seed is used.
            The default is None.

        Returns
        -------
        None.

        """
        self.maxStep = maxStep
        self.stepBoundaries = [(max(-self.maxStep, min(Y)), 
                                min(self.maxStep, max(Y))) 
                               for Y in stepBoundaries]
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
        return [X + random.uniform(Y[0], Y[1]) 
                for X, Y in zip(values, boundaries)]
