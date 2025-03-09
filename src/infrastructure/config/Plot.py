#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The configuration classes for graphical representation services.

Created on Sun Jan  5 16:43:35 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class BasePlotConfig:
    """
    The base class of plot configuration.
    """
    def __init__(self):
        """
        Initialize a BasePlotConfig object.

        Returns
        -------
        None.
        """
        self.marginLeft = 0.2
        self.marginRight = 0.95
        self.marginBottom = 0.15
        self.marginTop = 0.95
        self.tickDirection = 'in'
        self.fontSize = 10
        self.fontWeight = 'normal'
        self.axesLabelSize = 'medium'
