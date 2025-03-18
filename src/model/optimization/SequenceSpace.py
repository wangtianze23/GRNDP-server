#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 15:21:15 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


class SequenceSpace:
    """
    The base class for sequence space classes.
    """
    def __init__(self, name = '', alphabet = '', regionCount = 1):
        """
        Initialize a SequenceSpace object.

        Parameters
        ----------
        name : str, optional
            The name of the space. The default is an empty string.
        alphabet : str, optional
            The characters that can appear in a sequence.
            The default is an empty string, i.e. any character is allowed.
        regionCount : int, optional
            An integer indicating the number of regions in each sequence.
            The default is 1.

        Returns
        -------
        None.
        """
        self.name = name
        self.alphabet = alphabet
        self.regionCount = regionCount

class RegulationSequenceSpace(SequenceSpace):
    """
    The class for regulation sequence spaces.
    """
    def __init__(self, ID: int, name = '', alphabet = '', regionCount = 1, 
                 source = '', sequences = None, sequenceIDs = None):
        """
        Initialize a SparseRegulationSequenceSpace object.

        Parameters
        ----------
        ID : int
            A integer representing the identity of the space.
        name : str, optional
            The name of the space. The default is an empty string.
        regionCount : int, optional
            An integer indicating the number of regions in each sequence.
            The default is 1.
        source : str, optional
            A string representing the source of the space. 
            The default is empty string.
        sequences : list[list[str]] or NoneType, optional
            A list of list of strings represneting the possible choices of 
            sequence of each region for each element in the space, or None 
            if the sequences are not defined.
        sequenceIDs : list[str] or NoneType, optional
            A list of strings representing the identity of each possible 
            choice of elements in the space when **sequences** is not 
            None, or None when **sequences** is None or the items in 
            **sequences** have no identity.
            The default is None.

        Returns
        -------
        None.
        """
        super().__init__(name, alphabet)
        self.ID = ID
        self.source = source
        self.sequences = sequences
        self.sequenceIDs = sequenceIDs
    
    def __contains__(self, sequence: str) -> bool:
        """
        Check if a sequence exists in the space.

        Parameters
        ----------
        value : list
            A list of numeric values representing a vector.

        Returns
        -------
        bool
            Whether the specified sequence exists in the space.
        """
        if self.sequences is not None:
            return sequence in self.sequences
        return False
    
    def __getitem__(self, index: int) -> str:
        """
        Get a sequence by its index.

        Parameters
        ----------
        index : int
            The index of a sequence.

        Returns
        -------
        str
            A string representing the specified sequence.
        """
        if self.sequences is None:
            raise ValueError('no values defined in the space')
        if index < -len(self.sequences) or index >= len(self.sequences):
            raise IndexError('value index out of range')
        return self.sequences[index]
    
    def __len__(self) -> int:
        """
        Get the number of sequences in the space.

        Returns
        -------
        int
            The total number of sequences in the space.
        """
        if self.sequences is None:
            raise ValueError('no values defined in the space')
        return len(self.sequences)
