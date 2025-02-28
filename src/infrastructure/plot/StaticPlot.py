#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The representation classes for generating static plots.

Created on Sun Jan  5 16:42:34 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from base64 import b64encode
import tempfile
import matplotlib
import matplotlib.pyplot
from matplotlib.figure import Figure
from infrastructure.config.Plot import BasePlotConfig


class StaticFigure:
    """
    The container class for static figures.
    """
    def __init__(self, figure: Figure):
        """
        Initialize a StaticFigure object.

        Parameters
        ----------
        figure : Figure
            A matplotlib.figure.Figure object holding the figure to manipulate.

        Returns
        -------
        None.
        """
        self.figure = figure
        self.fileFormat = 'png'
    
    def save(self, filename: str):
        """
        Save a plot to file.

        Parameters
        ----------
        figure : Figure
            A matplotlib.figure.Figure object holding the plot to save.
        filename : str
            A string representing the path of the target file.

        Returns
        -------
        None.
        """
        self.figure.savefig(filename, format = self.fileFormat)
    
    def toBase64(self) -> str:
        """
        Convert a plot to a base64 string.

        Returns
        -------
        str
            A string containing the based64-encoded plot after rendering.
        """
        encodedImage = ''
        with tempfile.NamedTemporaryFile('rb') as tempFile:
            self.figure.savefig(tempFile.name, format = self.fileFormat)
            encodedImage = b64encode(tempFile.read()).decode('utf-8')
            tempFile.close()
        return encodedImage

class BaseStaticPlot:
    """
    The base class of plotting static figures
    """
    def __init__(self, config = BasePlotConfig()):
        """
        Initialize a BaseStaticPlot object
        
        Parameters
        ----------
        config : BaseStaticResource, optional
            An object of BaseStaticResource class or its sub-class, 
            containing plot configuration.

        Returns
        -------
        None.
        """
        self.config = config
        self.fileFormat = 'png'
        
        matplotlib.rcParams['xtick.direction'] = config.tickDirection
        matplotlib.rcParams['ytick.direction'] = config.tickDirection
        matplotlib.rcParams['font.size'] = config.fontSize
        matplotlib.rcParams['font.weight'] = config.fontWeight
        matplotlib.rcParams['axes.labelsize'] = config.axesLabelSize
    
    def setFileFormat(self, fileFormat: str):
        """
        Set the file format of the output figure.

        Parameters
        ----------
        fileFormat : str
            A string of either 'pdf', 'png' or 'svg' indicating the name of 
            the file format to use.

        Returns
        -------
        None.
        """
        self.fileFormat = fileFormat.strip().lower()
        if self.fileFormat == 'pdf':
            matplotlib.use('pdf')
        elif self.fileFormat == 'svg':
            matplotlib.use('svg')
        else:
            matplotlib.use('agg')
    
    @staticmethod
    def defaultSuffix(fileFormat: str) -> str:
        """
        Get the default suffix for image files of a given format

        Parameters
        ----------
        fileFormat : str
            A string indicating the name of the file format to use.

        Returns
        -------
        str
            A string indicating the default filename suffix for images 
            encapsulated in the specified format.
        """
        fileFormat = fileFormat.strip().lower()
        if fileFormat in ('eps', 'jpeg', 'jpg', 'pdf', 'png', 'ps', 'svg'):
            return '.' + fileFormat
        return ''
    
    def create(self, rowCount = 1, columnCount = 1, width = 6.4, height = 4.8,
               xRatio = [], yRatio = [], sharedX = False, sharedY = False) \
              -> StaticFigure:
        """
        Create a new figure of specified layout.

        Parameters
        ----------
        rowCount : int, optional
            The number of subplots in the figure on the horizontal direction.
            The default is 1.
        columnCount : int, optional
            The number of subplots in the figure on the vertical direction.
            The default is 1.
        width : int or float, optional
            The width of the figure in inches.
            The default is 6.4.
        height : int or float, optional
            The height of the figure in inches.
            The default is 4.8.
        xRatio : list, optional
            A list of float numbers between 0 and 1 indicating the relative 
            width for each subplot.
            The default is an empty list, i.e. evenly distributing all columns.
        yRatio : list, optional
            A list of float numbers between 0 and 1 indicating the relative 
            height for each subplot.
            The default is an empty list, i.e. evenly distributing all rows.
        shareX : bool, optional
            Whether the horizontal axis of all subplots should be synchronized.
            The default is False.
        shareY : bool, optional
            Whether the vertical axis of all subplots should be synchronized.
            The default is False.

        Returns
        -------
        StaticFigure
            A StaticFigure object holding the new plot.
        """
        if len(xRatio) == 0:
            xRatio = [1 / columnCount] * columnCount
        if len(yRatio) == 0:
            yRatio = [1 / rowCount] * rowCount
        figure = matplotlib.pyplot.subplots(rowCount, columnCount, 
                                          figsize = (width, height), 
                                          gridspec_kw = 
                                          {'width_ratios': xRatio, 
                                           'height_ratios': yRatio}, 
                                          sharex = sharedX, 
                                          sharey = sharedY)[0]
        
        # Wrap the matplotlib.figure.Figure object
        figure = StaticFigure(figure)
        figure.fileFormat = self.fileFormat
        return figure
