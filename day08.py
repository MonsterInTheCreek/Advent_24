# Day 8 AoC 2024
# Using input08.txt data
# Input string matrix that is 50 x 50 chars (when \n char is removed)
# It is mostly "." to indicate nothing
# Meaningful chars are upper & lower case alpha, and numbers
# Chars appear to merely be unique identifiers, treat all as points only.
# Belief is that upper, lower, and numbers are to be treated equally.
# If I'm understanding correctly, a simple answer is merely:
#   Calculate all total for all possibilities on an infinite board
#   Then subtract those that would be off the board
#   The main logic then is essentially solving for which would be off board

import numpy as np
import math
from itertools import combinations

# Abbreviated tools:
fact = lambda f: math.factorial(f)


EXP_1 = [
    "............\n",
    "........0...\n",
    ".....0......\n",
    ".......0....\n",
    "....0.......\n",
    "......A.....\n",
    "............\n",
    "............\n",
    "........A...\n",
    ".........A..\n",
    "............\n",
    "............\n",
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()
    

def process(dataset):
    data_list = []
    for row in dataset:
        clean_list = list(row.strip())
        data_list.append(clean_list)
    array = np.array(data_list)
    return array


def build_coords(array):
    '''
    Return dict of elems and xy coords
    Args: array (numpy array of string chars)
    Return: 
        chars_coords (dict of letter/number keys and list of xy lists)
        dim (int) number to edge
    '''
    dim = len(array)
    chars_coords = {}
    iters = 0
    for i in range(0,dim):
        for j in range(0,dim):
            iters += 1
            if array[i,j] not in chars_coords:
                chars_coords[array[i,j]] = [np.array([i,j])]
            else:
                chars_coords[array[i,j]].append(np.array([i,j]))
    del chars_coords["."]    # not useful
    assert iters == dim ** 2, "didn't fully loop thru all elems"
    return chars_coords, dim


def build_ants(coords_dict, part):
    '''
    Calculate antenode coordinates
    Ignore unique identifiers, and don't descern good or bad ants yet
    Args:
        coords_dict (dict of keys and list of xy lists) from build_cords()
        part (int: 1 or 2) to indicate Challenge Part 1 or Part 2
    Return:
        all_ants (list of numpy arrays) all coordinates for antinodes
    '''
    all_ants = []
    for char in coords_dict.keys():
        coords = coords_dict[char]
        pair_set = list(combinations(coords, 2))
        for pair in pair_set:
            a = pair[0]
            b = pair[1]
            diff = b - a
            ant1 = a - diff
            ant2 = b + diff
            all_ants.append(ant1)  
            all_ants.append(ant2)
            if part == 2:
                # go crazy, shoot them out in all directions, way out
                # anything beyond edge should get filtered out next.
                for i in range(0,101):
                    all_ants.append(a - (i * diff))
                    all_ants.append(b + (i * diff))
        #print(pair_set)
    return all_ants


def score_ants(ants,dim):
    '''
    Essentially this is filtering out points past edges and duplicates
    Args:
        ants (list of numpy arrays) coordinates of antinodes
        dim (int) number to edge
    Return: None - print results  
    '''
    good_coords = 0
    bad_coords = 0
    unique_ants = []
    # filter duplicates
    for ant in ants:
        if list(ant) not in unique_ants:
            unique_ants.append(list(ant))
    # filter anything beyond edges
    for ant in unique_ants:
        if ant[0] >= 0 and ant[0] < dim and ant[1] >= 0 and ant[1] < dim:
            good_coords += 1
        else:
            bad_coords += 1
    print(f"good coords = {good_coords}")
    print(f"bad_coords = {bad_coords}")


if __name__ == "__main__":
    #input = EXP_1
    #array = process(input)
    #chars,dim  = build_coords(array)
    #print(chars)
    #ants = build_ants(chars)
    #score_ants(ants,dim)


    input = get_data("input08.txt")
    array = process(input)
    chars,dim  = build_coords(array)
    ants1 = build_ants(chars,1)
    ants2 = build_ants(chars,2)
    score_ants(ants1,dim)
    score_ants(ants2,dim)


"""
# Don't actually need this
def max_ants(coords):
    '''
    Calculate maximum possible antinodes
    Args: coords (dict of lists) from build_coords()
    Returns: max_ants (int)
    '''
    max_ants = 0
    for char in coords.keys():
        # for every pair, there's max 2 antinodes
        elems = len(coords[char])
        combos = (fact(elems))/(2*fact(elems-2))
        max_ants += combos * 2
    return max_ants
"""