#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 16:48:30 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import math
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from infrastructure.plot.StaticPlot import BaseStaticPlot


class BaseRepresentation:
    """
    The base image representation class of simulation classes.
    """
    def __init__(self, canvas: BaseStaticPlot):
        """
        Initialize a BaseRepresentation object.
        
        Parameters
        ----------
        canvas : BaseStaticPlot
            A BaseStaticPlot object for managing plots.
        
        Returns
        -------
        None.
        """
        self.canvas = canvas
        self.aspectRatio = 1
        self.autoAspectRatio = False
        self.xLogScale = False
        self.yLogScale = False
        self.xRange = (None, None)
        self.yRange = (None, None)
        self.xLabel = 'x'
        self.yLabel = 'y'
        self.legend = False
        self.legendPosition = 'best'
        self.legendTitle = ''
    
    def setAspectRatio(self, aspectRatio = 1, autoAdjust = False):
        """
        Set the aspect ratio when drawing scatter plots.

        Parameters
        ----------
        aspectRatio : int or float, optional
            A numeric value representing the ratio of the width versus 
            the height for any unit area drawn on the canvas. 
            The default is 1.
        autoAdjust : bool, optional
            Whether to adjust the aspect ratio for elements drawn on 
            the canvas automatically. The value of **aspectRatio** is unused 
            when **autoAspectRatio** is True.
            The default is False.

        Returns
        -------
        None.
        """
        self.aspectRatio = aspectRatio
        self.autoAspectRatio = autoAdjust
    
    def setAxisRange(self, minX = None, maxX = None, minY = None, maxY = None):
        """
        Set the numeric range of axes when drawing scatter plots.
        
        Parameters
        ----------
        minX : float or NoneType, optional
            A float number indicating the lower limit of the horizontal axis, 
            or NoneType if it is automatically determined from data.
            The default is NoneType.
        maxX : float or NoneType, optional
            A float number indicating the maximum value of the horizontal axis, 
            or NoneType if it is automatically determined from data.
            The default is NoneType.
        minY : float or NoneType, optional
            A float number indicating the lower limit of the vertical axis, 
            or NoneType if it is automatically determined from data.
            The default is NoneType.
        maxY : float or NoneType, optional
            A float number indicating the maximum value of the vertical axis, 
            or NoneType if it is automatically determined from data.
            The default is NoneType.

        Returns
        -------
        None.
        """
        self.xRange = (minX, maxX)
        self.yRange = (minY, maxY)
    
    def correlation(self, predicted: list, measured: list, 
                    color = '#1F77B4', append = None) -> Figure:
        """
        Draw a scatter plot showing the correlation between the predicted 
        and the measured targets.

        Parameters
        ----------
        predicted : list
            A list of numeric values representing the predicted target values 
            from a model.
        measured : list
            A list of numeric values representing the actual target values. 
            The length of the list equals to the length of **predicted**.
        linearFit : bool, optional
            A boolean indicating whether a linearly fitted line should be drawn 
            among the data points. The default is False.
        showFormula : bool, optional
            A boolean indicating whether a linearly fitted formula should be 
            drawn alongside the plot. The default is False.
        color : str, optional
            A string indicating the color of all data points. 
            The default is None, i.e. the default color ('#1F77B4') will 
            be used.
        append : Figure or NoneType
            A Figure object to which the plot is appended, or None if a new 
            plot should be created.
            The default is None.

        Returns
        -------
        Figure
            A matplotlib.figure.Figure object that holds the scatter plot.
        """
        # Exclude infinite values
        masks = [math.isfinite(X) and math.isfinite(Y) 
                 for X, Y in zip(predicted, measured)]
        predicted = [X for X, mask in zip(predicted, masks) if mask]
        measured = [X for X, mask in zip(measured, masks) if mask]
        
        # Create a new plot
        if append is None:
            figure = self.canvas.create(width = 4.8, height = 4.8)
        else:
            figure = append
        axes = figure.gca()
        axes.set_aspect('auto' if self.autoAspectRatio else self.aspectRatio)
        
        # Set the axis scale
        axes.set_xscale('log' if self.xLogScale else 'linear')
        axes.set_yscale('log' if self.yLogScale else 'linear')
        
        # Make a scatter plot
        axes.scatter(predicted, measured, color = color)
        
        # Adjust the plot range
        if any(X is not None for X in self.xRange):
            axes.set_xlim(self.xRange[0], self.xRange[1])
        if any(X is not None for X in self.yRange):
            axes.set_ylim(self.yRange[0], self.yRange[1])
        
        # Set the axis label
        axes.set_xlabel(self.xLabel)
        axes.set_ylabel(self.yLabel)
        
        self.updateLegend(axes)
        
        return figure
    
    def removeLegend(self, axes: Axes):
        legend = axes.get_legend()
        if legend is not None:
            legend.remove()
    
    def updateLegend(self, axes: Axes):
        if self.legend:
            axes.legend(loc = self.legendPosition, title = self.legendTitle)
