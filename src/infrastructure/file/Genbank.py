#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The file classes for parsing GenBank files.

Created on Sat Mar 15 20:11:00 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from datetime import datetime


class GenbankFeature:
    """
    The container class for a feature in a GenBank record.
    """
    def __init__(self, typeName: str, start: int, stop: int, label = ''):
        """
        Initialize a GenbankFeature object.

        Parameters
        ----------
        typeName : str
            The type name of the feature.
        start : int
            The index of the start position of the feature.
        stop : int
            The index of the start position of the feature.
        label : str, optional
            A string representing the label for the feature.
            The default is an empty string.

        Returns
        -------
        None.
        """
        self.typeName = typeName
        self.start = start
        self.stop = stop
        self.label = label
    
    def __str__(self) -> str:
        """
        Get a string representation of the feature.

        Returns
        -------
        str
            A string representing the feature in a GenBank file.
        """
        return '     {}{}..{}\n{}/label="{}"'.\
               format(self.padString(self.typeName, 16), 
                      self.start + 1, max(self.stop, self.start + 1), 
                      ' ' * 21, self.label)
    
    @staticmethod
    def padString(string: str, length: int, paddingCharacter = ' ') -> str:
        """
        Pad a string to a fixed length.

        Parameters
        ----------
        string : str
            A string to pad.
        length : int
            The desired length of the padded string.
        paddingCharacter : str, optional
            A string of length 1 used to pad **string**.

        Returns
        -------
        str
            A string padded to the specified length.
        """
        return string + paddingCharacter * (length - len(string))

class GenbankRecord:
    """
    The container class for a record in a GenBank file.
    """
    def __init__(self, ID: str, sequence: str, definition: str, 
                 features: list[GenbankFeature], moleculeType = 'DNA', 
                 sequenceType = 'SYN', modificationDate = None, 
                 accession = None, version = None):
        """
        Initialize a GenbankRecord object.

        Parameters
        ----------
        ID : str
            A string representing the identity of the record.
        sequence : str
            A string representing the sequence associated with the record.
        definition : str
            A string representing the definition of the record.
        features : list[GenbankFeature]
            A list of GenbankFeature objects holding the features associated 
            with the record.
        moleculeType : str, optional
            A string indicating the type of the molecule associated with 
            the record.
            The default is 'DNA'.
        sequenceType : str, optional
            A string indicating the GenBank type of the sequence associated 
            with the record.
            The default is 'SYN', i.e. synthetic sequences.
        modificationDate : str or NoneType, optional
            A string representing the date of modification (in the format 
            'yyyy/mm/dd'), or NoneType if the current date shall be used.
            The default is None.
        accession : str or NoneType, optional
            A string representing the accession number of the record, or 
            NoneType if **ID** shall be used as its accession number.
            The default is None.
        version : str or NoneType, optional
            A string representing the version of the record, or NoneType if 
            **ID** shall be used as its version string.
            The default is None.

        Returns
        -------
        None.
        """
        self.ID = ID
        self.sequence = sequence
        self.definition = definition
        self.features = features
        self.moleculeType = moleculeType
        self.sequenceType = sequenceType
        self.modificationDate = modificationDate
        if self.modificationDate is None:
            self.modificationDate = datetime.strftime(datetime.now(), 
                                                      '%b-%d-%Y').upper()
        self.accession = accession or ID
        self.version = version or ID
    
    def __str__(self) -> str:
        """
        Get a string representation of the feature.

        Returns
        -------
        str
            A string representing the feature in a GenBank file.
        """
        return 'LOCUS       {}    {} bp {} {} {}\n'\
               'DEFINITION  {}\n'\
               'ACCESSION   {}\n'\
               'VERSION     {}\n'\
               'FEATURES             Location/Qualifiers\n'\
               '{}\n'\
               'ORIGIN\n'\
               '{}\n//\n'.\
               format(self.ID, len(self.sequence), 
                      self.moleculeType, self.sequenceType, 
                      self.modificationDate, self.definition, 
                      self.accession, self.version, 
                      '\n'.join(str(X) for X in self.features), 
                      self.sequence)

class GenbankFileWriter:
    """
    The class for writing GenBank files.
    """
    def __init__(self, file: object):
        """
        Initialize a GenbankFile object.

        Parameters
        ----------
        file : io.TextIOWrapper
            An io.TextIOWrapper object opened with writing permission.
        
        Returns
        -------
        None.
        """
        self.file = file
    
    def __del__(self):
        """
        Destruct the GenbankFileWriter object.

        Returns
        -------
        None.
        """
        if self.file is not None:
            self.close()
    
    def close(self):
        """
        Save changes to the GenBank file (if already opened) and close it.

        Returns
        -------
        None.
        """
        if self.file is not None:
            self.file.close()
            self.file = None
    
    def save(self):
        """
        Save changes to the GenBank file.

        Returns
        -------
        None.
        """
        if self.file is not None:
            self.file.flush()
    
    def appendRecord(self, record: GenbankRecord):
        """
        Append a record to the file.

        Parameters
        ----------
        record : GenbankRecord
            A GenbankRecord object to append.

        Returns
        -------
        None.
        """
        if self.file is None:
            return
        self.file.write(str(record))
