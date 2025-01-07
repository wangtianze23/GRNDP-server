#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 15:55:03 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from infrastructure.math.matrix import product


class AdjacencyMatrix:
    """
    The container class holding the adjacency of nodes in a directed graph.
    """
    def __init__(self, matrix: list[list]):
        """
        Initialize an AdjacencyMatrix object.

        Parameters
        ----------
        matrix : list[list]
            A list of list of integers representing the adjacency (regulatory 
            relationship) of each pair of nodes in a network. The length of 
            both the outer list and the inner list equals to the number of 
            nodes in the network. The total number of non-zero elements in 
            the list equals to the number of edges in the network.

        Returns
        -------
        None.
        """
        self.matrix = matrix
    
    def __getitem__(self, index: int) -> list:
        """
        Retrieve matrix elements by row index.

        Parameters
        ----------
        index : int
            The index of a row in the matrix.

        Returns
        -------
        list
            A list of numeric values representing the matrix elements at 
            the specified row.
        """
        if index < 0 or index >= len(self.matrix):
            raise IndexError('list index out of range')
        return self.matrix[index]
    
    def __len__(self) -> int:
        """
        Count matrix rows.

        Returns
        -------
        int
            The number of rows in the matrix.
        """
        return len(self.matrix)
    
    def acyclic(self) -> bool:
        """
        Check if a network is acyclic from its adjacency matrix.

        Returns
        -------
        bool
            Whether the network is acyclic.
        """
        matrix = self.matrix
        for i in range(0, len(matrix)):
            if any(X[j] > 0 for j, X in enumerate(matrix)):
                return False
            matrix = product(self.matrix, matrix)
        return True
