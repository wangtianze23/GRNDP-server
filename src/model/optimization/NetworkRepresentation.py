#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 20:29:24 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from matplotlib.figure import Figure
from infrastructure.math.number import floatRange
from infrastructure.plot.StaticPlot import BaseStaticPlot
from model.optimization.Network import Node, Path, Regulation
from model.simulation.NetworkFactory import BaseNetworkFactory,PairedRegulation
from model.simulation.Representation import BaseRepresentation


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
        self.samplingDensity = 300
    
    def response(self, nodeList: list[Node], regulations: list[Regulation], 
                 path: Path) -> Figure:
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

        Returns
        -------
        Figure
            A matplotlib.figure.Figure object containing the graphical 
            representation of the specified path.
        """
        regulations = [PairedRegulation(X.sourceIndex, X.targetIndex, 
                                        1 if X.regulationType == 'activation' 
                                        else -1, 
                                        [Y.value for Y in X.parameters]) 
                       for X in regulations]
        network,_=BaseNetworkFactory.createFromPairedRegulations(len(nodeList), 
                                                                 regulations)
        path = network.getPath(path.sourceIndex, path.targetIndex)
        samples = floatRange(0, 1, self.samplingDensity)
        return super().correlation(samples, [path(X) for X in samples])
