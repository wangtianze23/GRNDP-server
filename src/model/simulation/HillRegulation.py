#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 20:59:30 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.simulation.Regulation import BaseRegulation


class Hill(BaseRegulation):
    """
    The base class for Hill-styled regulation classes.
    """
    name = 'Hill'
    parameterIndexes = {
        0: 'y_min', 
        1: 'y_max', 
        2: 'K', 
        3: 'n'
    }
    
    def __init__(self, y_min: float, y_max: float, K: float, n: float):
        """
        Initialize a Hill object.

        Parameters
        ----------
        y_min : float
            The minimum value of the effect of the regulation.
        y_max : float
            The maximum value of the effect of the regulation.
        K : float
            The half maximum effective input of the regulation.
        n : float
            The Hill coefficient of the regulation.

        Returns
        -------
        None.
        """
        self.y_min = y_min
        self.y_max = y_max
        self.K = K
        self.n = n
    
    def parameter(self, index: int) -> float:
        """
        Overrides BaseRegulation.parameter().
        """
        if index == 0:
            return self.y_min
        elif index == 1:
            return self.y_max
        elif index == 2:
            return self.K
        elif index == 3:
            return self.n
        return None
    
    def setParameter(self, index: int, parameter: float):
        """
        Overrides BaseRegulation.setParameter().
        """
        if index == 0:
            self.y_min = parameter
        elif index == 1:
            self.y_max = parameter
        elif index == 2:
            self.K = parameter
        elif index == 3:
            self.n = parameter

class HillA(Hill):
    """
    The class for activating Hill-styled regulation.
    """
    name = 'HillA'
    def __call__(self, X: list) -> float:
        """
        Overrides BaseRegulation.__call__().
        """
        if X[0] > 0:
            return self.y_min + self.y_max / (1 + (self.K / X[0]) ** self.n)
        else:
            return self.y_min

class HillR(Hill):
    """
    The class for repressive Hill-styled regulation.
    """
    name = 'HillR'
    parameterIndexes = {
        0: 'y_min', 
        1: 'y_max', 
        2: 'K', 
        3: 'n', 
        4: 'activation', 
        5: 'correction'
    }
    
    def __init__(self, y_min: float, y_max: float, K: float, n: float, 
                 activation = 1, correction = 1):
        """
        Initialize a HillR object.

        Parameters
        ----------
        y_min : float
            The minimum value of the effect of the regulation.
        y_max : float
            The maximum value of the effect of the regulation.
        K : float
            The half maximum effective input of the regulation.
        n : float
            The Hill coefficient of the regulation.
        activation : float
            A numeric value representing the effect of activation model.
            The default is 1.
        correction : int or float, optional
            A numeric value representing the correction factor applied to 
            the effect of repression. 
            The default is 1.

        Returns
        -------
        None.
        """
        self.y_min = y_min
        self.y_max = y_max
        self.K = K
        self.n = n
        self.activation = activation
        self.correction = correction
    
    def parameter(self, index: int) -> float:
        """
        Overrides Hill.parameter().
        """
        if index == 4:
            return self.activation
        if index == 5:
            return self.correction
        return super().parameter(index)
    
    def setParameter(self, index: int, parameter: float):
        """
        Overrides Hill.setParameter().
        """
        if index == 4:
            self.activation = parameter
        elif index == 5:
            self.correction = parameter
        else:
            super().setParameter(index, parameter)

    def __call__(self, X: list) -> float:
        """
        Overrides BaseRegulation.__call__().
        """
        return self.y_min + \
               self.y_max * self.activation * (1 + 1 / self.correction) / \
               (1 + self.activation + 
                (1 + self.correction) * (X[0] / self.K) ** self.n)

class HillAR(Hill):
    """
    The class for activating and repressive Hill-styled regulation.
    """
    name = 'HillARc'
    parameterIndexes = {
        0: 'y_min', 
        1: 'y_max', 
        2: 'K_A', 
        3: 'n_A', 
        4: 'K_R', 
        5: 'n_R', 
        6: 'correction'
    }
    
    def __init__(self, y_min: float, y_max: float, K_A: float, n_A: float, 
                 K_R: float, n_R: float, correction = 1):
        """
        Initialize a HillAR object.

        Parameters
        ----------
        y_min : float
            The minimum value of the effect of the regulation.
        y_max : float
            The maximum value of the effect of the regulation.
        K_A : float
            The half maximum effective input of the activating part of 
            the regulation.
        n : float
            The Hill coefficient of the activating part of the regulation.
        K_R : float
            The half maximum effective input of the repressive part of 
            the regulation.
        n_R : float
            The Hill coefficient of the repressive part of the regulation.
        correction : int or float, optional
            A numeric value representing the correction factor applied to 
            the effect of repression. 
            The default is 1.

        Returns
        -------
        None.
        """
        self.y_min = y_min
        self.y_max = y_max
        self.K_A = K_A
        self.n_A = n_A
        self.K_R = K_R
        self.n_R = n_R
        self.correction = correction
   
    def __call__(self, X: list) -> float:
        """
        Overrides BaseRegulation.__call__().
        """
        A = (X[0] / self.K_A) ** self.n_A if X[0] > 0 else 0
        R = (X[1] / self.K_R) ** self.n_R if X[1] > 0 else 0
        return self.y_min + self.y_max * A * (1 + 1 / self.correction) / \
               (1 + A + (1 + self.correction) * R)
    
    def parameter(self, index: int) -> float:
        """
        Overrides BaseRegulation.parameter().
        """
        if index == 0:
            return self.y_min
        elif index == 1:
            return self.y_max
        elif index == 2:
            return self.K_A
        elif index == 3:
            return self.n_A
        elif index == 4:
            return self.K_R
        elif index == 5:
            return self.n_R
        elif index == 6:
            return self.correction
        return None
    
    def setParameter(self, index: int, parameter: float):
        """
        Overrides BaseRegulation.setParameter().
        """
        if index == 0:
            self.y_min = parameter
        elif index == 1:
            self.y_max = parameter
        elif index == 2:
            self.K_A = parameter
        elif index == 3:
            self.n_A = parameter
        elif index == 4:
            self.K_R = parameter
        elif index == 5:
            self.n_R = parameter
        elif index == 6:
            self.correction = parameter
