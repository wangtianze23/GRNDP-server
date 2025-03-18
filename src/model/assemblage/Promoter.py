#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 20:07:11 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

import tempfile
from infrastructure.file.Genbank import \
    GenbankFeature, GenbankRecord, GenbankFileWriter
from model.assemblage.Sequence import AnnotatedSequence


class FeaturedPromoter:
    """
    The container class for a promoter sequence with features.
    """
    def __init__(self, sequence: AnnotatedSequence, properties: dict):
        """
        Initialize a FeaturedPromoter object.

        Parameters
        ----------
        sequence : AnnotatedSequence
            An AnnotatedSequence object representing a promoter sequence.
        properties : dict
            A dictionary with strings as keys pointing to numeric values, 
            representing the name and value of the properties associate with 
            the promoter.

        Returns
        -------
        None.
        """
        self.sequence = sequence
        self.properties = properties

class RegulationPromoterCollection:
    """
    The container class for a series of promoters pertaining to 
    the regulations in a network.
    """
    def __init__(self, promoters: list[FeaturedPromoter], 
                 nodeIndexes: list[int], names: list[str]):
        """
        Initialize a RegulationPromoterCollection object.

        Parameters
        ----------
        promoters : list[FeaturedPromoter]
            A list of FeaturedPromoter object holding the sequence and 
            additional information about the promoters.
        nodeIndexes : list[int]
            A list of integers indicating the index of the nodes associated 
            with the promoters. The length of the list equals to the length 
            of **promoters**.
        names : list[str]
            A list of strings representing the name of the promoters.
            The length of the list equals to the length of **promoters**.

        Returns
        -------
        None.
        """
        self.promoters = promoters
        self.nodeIndexes = nodeIndexes
        self.names = names
    
    def toGenbank(self) -> str:
        """
        Export the promoters to a Genbank file.

        Returns
        -------
        str
            A string representing the content of the Genbank file.
        """
        tempFile = tempfile.TemporaryFile('w+')
        writer = GenbankFileWriter(tempFile)
        for promoter, nodeIndex, name in \
            zip(self.promoters, self.nodeIndexes, self.names):
            features = [GenbankFeature(X.typeName, X.start, X.stop, 
                                       label = X.name)
                        for X in promoter.sequence.annotations]
            record = GenbankRecord(name, promoter.sequence.sequence, name, 
                                   features)
            writer.appendRecord(record)
        writer.save()
        tempFile.seek(0, 0)
        return tempFile.read()
