#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 15:59:52 2025
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""


def product(matrix1: list[list], matrix2: list[list]) -> list[list]:
    """
    Calculate the product of two matrices.

    Parameters
    ----------
    matrix1 : list[list]
        A list of list of numeric values representing a left-side matrix.
    matrix2 : list[list]
        A list of list of numeric values representing a right-side matrix.

    Returns
    -------
    list[list]
        A list of list of numeric values representing the production of 
        **matrix1** and **matrix2**.
    """
    if len(matrix1) == 0 or len(matrix2) == 0:
        return []
    
    if len(matrix1[0]) != len(matrix2):
        raise ValueError('The column length of the first matrix ({}) does not '
                         'equal to the row length of the second matrix ({})'.
                         format(len(matrix1[0]), len(matrix2)))
    
    rowCount = len(matrix1)
    columnCount = len(matrix2[0])
    result = [None] * rowCount
    for i, X in enumerate(matrix1):
        row = [None] * columnCount
        for j in range(0, columnCount):
            row[j] = sum(x * matrix2[k][j] for k, x in enumerate(X))
        result[i] = row
    return result
