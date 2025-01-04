#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 20:29:24 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from base64 import b64encode
import matplotlib.figure
import tempfile


class PathRepresentation:
    """
    The class for graphical representation of paths in a network.
    """
    def __init__(self, sourceIndex: int, targetIndex: int, 
                 figure: matplotlib.figure.Figure):
        """
        Initialize a PathRepresentation object.

        Parameters
        ----------
        sourceIndex : int
            The index of the source node connected by the path.
        targetIndex : int
            The index of the target node connected by the path.
        figure : matplotlib.figure.Figure
            A matplotlib.figure.Figure object containing the graphical 
            representation of the specified path.

        Returns
        -------
        None.
        """
        self.sourceIndex = sourceIndex
        self.targetIndex = targetIndex
        self.figure = figure
    
    def toBase64(self) -> str:
        """
        Get the Based64-encoded string of a rendered figure.
        
        Returns
        -------
        None.
        """
        encodedImage = 'data:image/png;base64'
        if self.figure is not None:
            with tempfile.NamedTemporaryFile('rb') as tempFile:
                self.figure.savefig(tempFile.name, format = 'png')
                encodedImage = b64encode(tempFile.read()).decode('utf-8')
                tempFile.close()
        return encodedImage
