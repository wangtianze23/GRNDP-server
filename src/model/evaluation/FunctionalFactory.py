#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 21:10:29 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.evaluation.Functional import BaseFunctional, JointFunctional
from model.evaluation.FunctionalException import \
    FunctionalNotCombinable, FunctionalTypeNotSupported
from model.evaluation.BuiltinFunctional import \
    MinimumFunctional, MaximumFunctional, \
    InverseMinimumFunctional, InverseMaximumFunctional, FWHMFunctional
from model.evaluation.BuiltinProbabilityFunctional import \
    InverseVarianceFunctional, InverseLogSpanFunctional, \
    PopulationRatioFunctional


class BuiltinFunctionalFactory:
    """
    The factory class for built-in functional classes.
    """
    @staticmethod
    def createFromBuiltinName(name: str, valueRanges = None) -> BaseFunctional:
        """
        Construct a BaseFunctional object from its representative name.

        Parameters
        ----------
        name : str
            A string representing the internal name of a built-in functional 
            object.
        valueRanges : list[tuple] or NoneType, optional
            A list of tuples of (float, float) representing the lower and 
            upper boundary for the value of each input variable of the input 
            function, or None if the default boundaries shall be used. 
            The length of the list must equal to the number of input variables 
            of any function to evaluate.
            The default is None.

        Returns
        -------
        BaseFunctional
            A BaseFunctional of the specified name.
        """
        for targetClass in \
            (MinimumFunctional, MaximumFunctional, 
             InverseMinimumFunctional, InverseMaximumFunctional, 
             FWHMFunctional, InverseVarianceFunctional, 
             InverseLogSpanFunctional, PopulationRatioFunctional):
            if targetClass.builtinName == name:
                target = targetClass()
                for i, valueRange in enumerate(valueRanges):
                    # The first range corresponds to the function value
                    # and the rest ranges correspond to the function variables
                    if i > 0 and valueRange is not None:
                        target.setVaribleRange(i - 1, valueRange)
                return target
        
        raise FunctionalTypeNotSupported(name)
    
    @staticmethod
    def createFromCombination(components: list[BaseFunctional], 
                              reduction: object = None) -> JointFunctional:
        """
        Construct a JointFunctional from multiple functionals.

        Parameters
        ----------
        components : list[BaseFunctional]
            A list of BaseFunctional objects to combine.

        Returns
        -------
        JointFunctional
            A JointFunctional combined from the specified component 
            functionals.
        """
        variableCounts = [X.variableCount for X in components]
        if any(X != variableCounts[-1] for X in variableCounts) > 1:
            raise FunctionalNotCombinable([X.name for X in components])
        name = '+'.join(X.name for X in components)
        description = 'Joint of {}'.format(','.join(X.name 
                                                    for X in components))
        return JointFunctional(name, variableCounts[0], components, 
                               descrption = description)
