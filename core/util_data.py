#-----------------------------------------------------------------------------------------------------
# Author: cgarcia@umw.edu
# Created: 2/20/2020
# About: This file contains some utility functions for generating data.
#
# Revision History:
# Date        Author            Change Description
# 2/20/2020   cgarcia           Initial version.
#-----------------------------------------------------------------------------------------------------

import random as rnd

# Generate a matrix of constant values.
def const_matrix(n_rows, n_columns, const=0):
    return [[const for j in range(n_columns)] for i in range(n_rows)]

# Expands a matrix (2D list) by duplicating rows and columns according to the specified dimensional factors.    
def expand_matrix(matrix, row_factor=1, column_factor=1):
    rows = []
    for i in matrix:
        for rf in range(row_factor):
            row = list(i)
            col = []
            for j in row:
                for cf in range(column_factor):
                    col.append(j)
            rows.append(col)
    return rows

# Generate a random float in the specified range.
def rand_float(minf, maxf):
    return minf + ((maxf - minf) * rnd.random())

# Generate a random segment in form of (start, finish), based on the length and bound constraints specified.    
def rand_segment(min_length, max_length, lower_bound, upper_bound, integer=False):
    min_length = min(min_length, upper_bound - lower_bound)
    max_length = min(max_length, upper_bound - lower_bound)
    length = rand_float(min_length, max_length)
    position = rand_float(lower_bound, upper_bound - length)
    if not(integer):
        return (position, position + length)
    else:
        a = round(position)
        b = min(round(position + length), int(upper_bound))
        return(int(a), int(b))

# Generate a list of random 0/1 values according to the specified probability of getting a 1.
def rand_binaries(n, prob_1):
    rb = lambda: 1 if rnd.random() < prob_1 else 0
    return [rb() for i in range(n)]

# Given m items and n slots, randomly distrubute the items to the slots and return the final slot item counts.   
def rand_slot_distribute(m_items, n_slots):
    slots = [0 for i in range(n_slots)]
    for i in range(m_items):
        slots[rnd.randint(0, n_slots - 1)] += 1
    return slots

# Generates a random binary matrix such that no row or column sums to zero, provided sum(column_sums) >= n_rows.
# @param n_rows: the number of rows in the matrix
# @param column_sums: a column vector specifying the sums that each column should have in the final matrix.
def rand_bin_matrix(n_rows, column_sums):
    column_sums = [min(s, n_rows) for s in column_sums] # safety feature to prevent an infinite loop
    mat = const_matrix(n_rows, len(column_sums), 0)
    zeros = [0 for i in range(len(column_sums))]
    ones = [1 for i in range(len(column_sums))]
    i = 0
    while column_sums != zeros:
        if i >= n_rows:
            i = 0
            rnd.shuffle(mat)
        try:
            j = rnd.sample([x for x in range(len(column_sums)) if mat[i][x] == 0 and column_sums[x] != 0], 1)[0]
            mat[i][j] += 1
            column_sums[j] -= 1
        except:
            pass
        i += 1
    return mat

# Given a list of numeric weights that correspond to the probability that an index will be chosen, randomly select
# one of the indices and return it.    
def random_weighted_index(weights):
    if len(weights) < 1:
        raise 'random_weight_index: weights must not be empty'
    sm = sum(weights)
    tw = 0
    rd = rand_float(0, sm)
    for i in range(len(weights)):
        tw += weights[i]
        if rd <= tw:
            return i
    
    
    