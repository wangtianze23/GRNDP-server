#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 20:32:08 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import math
from model.evaluation.Functional import BaseFunctional
import scipy.optimize as Optimize


class MaximumFunctional(BaseFunctional):
    """
    The class for evaluating the maximum of a function.
    """
    builtinName = 'maximum'
    
    def __init__(self, name = 'Maximum', variableCount = 1, 
                 descrption = 'The maximum output with respect to the input'):
        """
        Initialize a MaximumFunctional object.
        """
        super().__init__(name, variableCount, descrption)
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseFunctional.__call__().
        """
        if self.variableCount == 1:
            result = Optimize.minimize_scalar(lambda X: -function((X,)), 
                                              bounds = self.variableRanges[0], 
                                              method = 'bounded')
        else:
            result = Optimize.minimize(lambda X: -function(X), 
                                       x0 = [(max(X) + min(X)) / 2 
                                             for X in self.variableRanges], 
                                       bounds = self.variableRanges, 
                                       method = 'L-BFGS-B')
        return result['x'].tolist()

class MinimumFunctional(BaseFunctional):
    """
    The class for evaluating the minimum of a function.
    """
    builtinName = 'minimum'
    
    def __init__(self, name = 'Minimum', variableCount = 1, 
                 descrption = 'The minimum output with respect to the input'):
        """
        Initialize a MinimumFunctional object.
        """
        super().__init__(name, variableCount, descrption)
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseFunctional.__call__().
        """
        if self.variableCount == 1:
            result = Optimize.minimize_scalar(lambda X: function((X,)), 
                                              bounds = self.variableRanges[0], 
                                              method = 'bounded')
        else:
            result = Optimize.minimize(lambda X: function(X), 
                                       x0 = [(max(X) + min(X)) / 2 
                                             for X in self.variableRanges], 
                                       bounds = self.variableRanges, 
                                       method = 'L-BFGS-B')
        return result['x'].tolist()

class InverseMaximumFunctional(MaximumFunctional):
    """
    The class for evaluating the inverse of maximum of a function.
    """
    builtinName = '1/maximum'
    
    def __init__(self, name = '1/Maximum', variableCount = 1, 
                 descrption = 'The inverse of maximum output with respect to '
                              'the input'):
        """
        Initialize an InverseMaximumFunctional object.
        """
        super().__init__(name, variableCount, descrption)
        self.maxValue = 1e10
    
    def __call__(self, function: object) -> float:
        """
        Overrides MaximumFunctional.__call__().
        """
        value = super().__call__(function)
        return 1 / value if value != 0 else self.maxValue

class InverseMinimumFunctional(MinimumFunctional):
    """
    The class for evaluating the inverse of minimum of a function.
    """
    builtinName = '1/minimum'
    
    def __init__(self, name = '1/Minimum', variableCount = 1, 
                 descrption = 'The inverse of minimum output with respect to '
                              'the input'):
        """
        Initialize an InverseMinimumFunctional object.
        """
        super().__init__(name, variableCount, descrption)
        self.maxValue = 1e10
    
    def __call__(self, function: object) -> float:
        """
        Overrides MinimumFunctional.__call__().
        """
        value = super().__call__(function)
        return 1 / value if value != 0 else self.maxValue

class FWHMFunctional(BaseFunctional):
    """
    The class for evaluating the full width at half maximum of a function.
    """
    builtinName = 'FWHM'
    
    def __init__(self, name = 'FWHM', 
                 descrption = 'The full width at half maximum output with '
                              'respect to the input'):
        """
        Initialize a FWHMFunctional object.
        """
        super().__init__(name, 1, descrption)
    
    def __call__(self, function: object) -> float:
        """
        Overrides BaseFunctional.__call__().
        """
        result = Optimize.minimize_scalar(lambda X: -function((X,)), 
                                          bounds = self.variableRanges[0], 
                                          method = 'bounded')
        peak = result['x'].tolist()
        halfMaximum = function((peak,)) / 2
        
        result = Optimize.minimize_scalar(lambda X: 
                                          (function((X,)) - halfMaximum) ** 2, 
                                          bounds = (self.variableRanges[0][0], 
                                                    peak), 
                                          method = 'bounded')
        rangeLength = max(self.variableRanges[0]) - min(self.variableRanges[0])
        if result['x'] > min(self.variableRanges[0]) + rangeLength * 0.001:
            halfMaximumLeft = result['x'].tolist()
        else:
            halfMaximumLeft = -math.inf
        
        result = Optimize.minimize_scalar(lambda X: 
                                          (function((X,)) - halfMaximum) ** 2, 
                                          bounds = (peak, 
                                                    self.variableRanges[0][1]), 
                                          method = 'bounded')
        if result['x'] < max(self.variableRanges[0]) - rangeLength * 0.001:
            halfMaximumRight = result['x'].tolist()
        else:
            halfMaximumRight = math.inf
        
        return max(peak - halfMaximumLeft, halfMaximumRight - peak) * 2
