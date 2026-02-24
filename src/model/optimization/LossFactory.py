#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 10:04:46 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from model.evaluation.FunctionalFactory import BuiltinFunctionalFactory
from model.optimization.Loss import \
    BaseOptimizationLoss, MSEOptimizationLoss, CompoundOptimizationLoss
from model.optimization.Constraint import TargetConstraint
from model.optimization.Target import BuiltinTarget


class OptimizationLossFactory:
    """
    The factory class for BaseOptimizationLoss classes.
    """
    @staticmethod
    def createFromTargetConstraint(constraint: TargetConstraint) \
                                  -> BaseOptimizationLoss:
        """
        Construct a BaseOptimizationLoss object from an optimization target.

        Parameters
        ----------
        constraint : TargetConstraint
            A TargetConstraint object containing the information about 
            an optimization target and its constraints.

        Returns
        -------
        BaseOptimizationLoss
            A BaseOptimizationLoss object that can be used to calculate 
            the optimization loss.
        """
        if not isinstance(constraint.space, BuiltinTarget):
            return BaseOptimizationLoss([])
        
        functionals = [BuiltinFunctionalFactory.
                       createFromBuiltinName(X, 
                                             valueRanges = 
                                             constraint.valueRanges) 
                       for X in constraint.space.functionalNames]
        if len(functionals) > 1:
            jointFunctional = \
                BuiltinFunctionalFactory.createFromCombination(functionals)
            functionals = jointFunctional.components
        else:
            jointFunctional = None
        
        lossObjects = []
        for i, functional in enumerate(functionals):
            if constraint.expectedValue is None or i > 0:
                lossObject = BaseOptimizationLoss(functional)
            else:
                lossObject = MSEOptimizationLoss(functional)
                lossObject.setExpectedValue(constraint.expectedValue)
            lossObjects.append(lossObject)
        
        if len(lossObjects) > 1:
            return CompoundOptimizationLoss(lossObjects, jointFunctional)
        return lossObjects[0]
