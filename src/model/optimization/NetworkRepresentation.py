#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 20:29:24 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import scipy.stats as Stats
from infrastructure.plot.StaticPlot import BaseStaticPlot, StaticFigure
from model.optimization.Network import Node, Path, Regulation
from model.optimization.Representation import BaseRepresentation
from model.simulation.NetworkFactory import BaseNetworkFactory,PairedRegulation
from model.simulation.DynamicNetwork import BaseDynamicNetwork


class PathRepresentation(BaseRepresentation):
    """
    The class for graphical representation of paths in a network.
    """
    def __init__(self, canvas: BaseStaticPlot):
        """
        Initialize a PathRepresentation object.

        Parameters
        ----------
        canvas : BaseStaticPlot
            A BaseStaticPlot object for managing plots.

        Returns
        -------
        None.
        """
        super().__init__(canvas)
        self.xLogScale = True
        self.yLogScale = True
        self.xLabel = 'Transcription factor'
        self.yLabel = 'Promoter strength'
    
    def response(self, nodeList: list[Node], regulations: list[Regulation], 
                 path: Path, xRange = (1e-2, 1e2)) -> StaticFigure:
        """
        Plot the response curve of a target node with respect to changes on 
        a source node in a network.

        Parameters
        ----------
        nodeList : list
            A list of Node objects indicating all entities in the network.
        regulations : Regulation
            A list of regulations objects containing the result of optimization.
        path : Path
            A Path object indicating the path to visualize.
        xRange : tuple, optional
            A tuple of (float, float) indicating the limit of horizontal axis, 
            or None if the default range shall be used.
            The default is (1e-2, 1e2).

        Returns
        -------
        StaticFigure
            A StaticFigure object containing the graphical representation of 
            the specified path.
        """
        # Reconstruct a network of the specified topology
        regulations = [PairedRegulation(X.sourceIndex, X.targetIndex, 
                                        1 if X.regulationType == 'activation' 
                                        else 
                                        -1 if X.regulationType == 'repression' 
                                        else 0, 
                                        [Y.value for Y in X.parameters]) 
                       for X in regulations]
        network,_=BaseNetworkFactory.createFromPairedRegulations(len(nodeList), 
                                                                 regulations)
        
        # Generate samples along the specified path
        pathFunction = network.getPath(path.sourceIndex, path.targetIndex)
        
        # Plot the response curve
        self.xRange = xRange
        self.xLabel = nodeList[path.sourceIndex].name
        self.yLabel = nodeList[path.targetIndex].name
        return super().curve(lambda X: [pathFunction(Y) for Y in X])

class DensityRepresentation(BaseRepresentation):
    """
    The class for graphical representation of probability density of 
    the value of a node in a network.
    """
    def __init__(self, canvas: BaseStaticPlot):
        """
        Initialize a DensityRepresentation object.

        Parameters
        ----------
        canvas : BaseStaticPlot
            A BaseStaticPlot object for managing plots.

        Returns
        -------
        None.
        """
        super().__init__(canvas)
        self.samplingDensity = 3
        self.samplingTime = 24
        self.xLogScale = True
        self.yLogScale = False
        self.xLabel = 'Transcription factor'
        self.yLabel = 'Density'
    
    def setSamplingTime(self, samplingTime: float):
        """
        Set the time of sampling for estimating probability density.

        Parameters
        ----------
        timeSpan : int or float
            A numeric value indicating the span of time allowed for simulation  
            in each trajectory.

        Returns
        -------
        None.
        """
        self.samplingTime = samplingTime
    
    def density(self, nodeList: list[Node], regulations: list[Regulation], 
                nodeIndex: int, xRange = (1e-3, 1e2), initialValues = None, 
                minNoise = 0.001, relativeNoise = 0.2) -> StaticFigure:
        """
        Plot the response curve of a target node with respect to changes on 
        a source node in a network.

        Parameters
        ----------
        nodeList : list
            A list of Node objects indicating all entities in the network.
        regulations : Regulation
            A list of regulations objects containing the result of optimization.
        nodeIndex : int
            An integer representing the index of the node whose value density 
            is to be visualized.
        xRange : tuple, optional
            A tuple of (float, float) indicating the limit of horizontal axis, 
            or None if the default range shall be used.
            The default is (1e-4, 1e2).
        initialValues : list or NoneType, optional
            A list of numeric value representing the initial value of each 
            node in the network, or None if the default value (0) shall be 
            used for all nodes.
            The default is None.
        minNoise : int or float, optional
            A numeric value indicating the minimum absolute noise level.
            The default is 0.001.
        relativeNoise : int or float, optional
            A numeric value indicating the relative noise level.
            The default is 0.2, i.e. a gaussian noise with mean = 0 and 
            standard deviation = 0.2 * (current value of regulated variable).

        Returns
        -------
        StaticFigure
            A StaticFigure object containing the graphical representation of 
            the probability density of the specified node.
        """
        # Reconstruct a network of the specified topology
        regulations = [PairedRegulation(X.sourceIndex, X.targetIndex, 
                                        1 if X.regulationType == 'activation' 
                                        else 
                                        -1 if X.regulationType == 'repression' 
                                        else 0, 
                                        [Y.value for Y in X.parameters]) 
                       for X in regulations]
        network,_=BaseNetworkFactory.createFromPairedRegulations(len(nodeList), 
                                                                 regulations)
        
        # Generate samples for the value of the specified node
        network = BaseDynamicNetwork.fromBaseNetwork(network, 
                                                     minNoise, relativeNoise)
        if initialValues is None:
            initialValues = [0] * len(nodeList)
        sampleCount = self.sampleCount * self.samplingDensity
        samples = [X[nodeIndex] 
                   for X in network.evolve(initialValues, 
                                           self.samplingTime, sampleCount)]
        if self.xLogScale:
            minValue = min(X for X in samples if X > 0)
            kernel = Stats.gaussian_kde([max(X, minValue) for X in samples])
        else:
            kernel = Stats.gaussian_kde(samples)
        
        # Plot the response curve
        self.xRange = xRange
        self.xLabel = nodeList[nodeIndex].name
        return super().curve(lambda X: [kernel(Y) for Y in X])
