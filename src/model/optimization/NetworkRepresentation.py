#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 20:29:24 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from matplotlib.figure import Figure
from infrastructure.plot.StaticPlot import BaseStaticPlot
from model.optimization.Network import Node, Path, Regulation
from model.optimization.Representation import BaseRepresentation
from model.simulation.NetworkFactory import BaseNetworkFactory,PairedRegulation


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
                 path: Path, xRange = (1e-2, 1e2)) -> Figure:
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
        Figure
            A matplotlib.figure.Figure object containing the graphical 
            representation of the specified path.
        """
        # Reconstruct a network of the specified topology
        regulations = [PairedRegulation(X.sourceIndex, X.targetIndex, 
                                        1 if X.regulationType == 'activation' 
                                        else -1, 
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
