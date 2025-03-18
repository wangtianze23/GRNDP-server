#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 11:21:44 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class RegionAnnotation:
    """
    The container class holding the annotation of a region in a DNA sequence.
    """
    def __init__(self, name: str, start: int, stop: int, typeName = ''):
        """
        Initialize a RegionAnnotation object

        Parameters
        ----------
        name : str
            The name of the region.
        start : int
            The index of the start position of the region.
        stop : int
            The index of the stop position of the region.
        typeName : str, optional
            The type of the region.
            The default is an empty string.

        Returns
        -------
        None.
        """
        self.name = name
        self.start = start
        self.stop = stop
        self.typeName = typeName

class AnnotatedSequence:
    """
    The container class for biological sequences with annotations.
    """
    def __init__(self, sequence: str, annotations: list[RegionAnnotation]):
        """
        Initialize an AnnotatedSequence object.

        Parameters
        ----------
        sequence : str
            A string representing the sequence.
        annotations : list[RegionAnnotation]
            A list of RegionAnnotation objects representing the annotation 
            of specific regions in the sequence.

        Returns
        -------
        None.
        """
        self.sequence = sequence
        self.annotations = annotations
