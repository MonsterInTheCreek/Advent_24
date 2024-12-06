# Day 6 AoC 2024
# Using input06.txt data
# Source data is 130 x 130 chars (once \n chars removed)
# Source is fully "." and "#" chars only, except one "^" char at (46,43)
# Find the steps?  # https://www.youtube.com/watch?v=S8D1YyNuunQ

# Early optimization may be the root of all evil, but I had to spend a long
# time optimizing this to have a shot at running part 2 in less than hours.

import numpy as np
import time


EXP_1 = [
    "....#.....\n",
    ".........#\n",
    "..........\n",
    "..#.......\n",
    ".......#..\n",
    "..........\n",
    ".#..^.....\n",
    "........#.\n",
    "#.........\n",
    "......#...\n",
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    prep = [list(row[:-1]) for row in dataset]
    walk_map = np.array(prep)
    # Added for part 2 optimization - rework dataset as ints
    #   . --> 0
    #   # --> 1
    #   ^ --> 2
    #   X --> 3
    cond_map = [
        walk_map == ".",
        walk_map == "#",
        walk_map == "^",
        ]
    output_map = np.array([0,1,2], dtype=np.int8)   # np.int8 tiny mem benefit
    walk_map = np.select(cond_map, output_map)

    return walk_map


def find_pt(walk_map):
    '''
    Return xy coords for current pointer anywhere on map
    '''
    start_pt = np.argwhere(walk_map == 2)
    x = start_pt[0][0]
    y = start_pt[0][1]
    return (x,y)


def move_pt(walk_map):
    first_run = True
    loops = 0
    x,y = find_pt(walk_map)
    outside = len(walk_map)
    #while not (x == 0 or y == 0 or x == outside_dim or y == outside_dim):
    while 0 < x < outside and 0 < y < outside:
        loops += 1
        x,y = find_pt(walk_map)
        walk_map[x,y] = np.int8(3)              # mark current square
        walk_map[x-1,y] = np.int8(2)            # move pt up one
        if first_run == True and walk_map[x-2,y] == 1:
            turn_map_s = time.time()
            walk_map = np.rot90(walk_map, k=1)
            turn_map_e = time.time()
            print(f"turn map took = {turn_map_e - turn_map_s:.8f}")
            first_run = False
        elif walk_map[x-2,y] == 1:
            walk_map = np.rot90(walk_map, k=1)
    print(f"took {loops} loops")
    return np.sum(walk_map == 3)


if __name__ == "__main__":   
    #walk_map = process(EXP_1)
    #print(move_pt(walk_map))

    t_start = time.time()
    input = get_data("input06.txt")
    walk_map = process(input)
    steps = move_pt(walk_map)
    t_end = time.time()
    print(f"Day 6, first = {steps}")
    print(f"Time = {t_end - t_start:.6f}")



### Full version of move_pt() including debug statements
# This is the original and improved recursive logic that I used to solve part 1

# I had the main logic of this working pretty quick
# But it took hours to figure out:
#   How to initiate exit at overflow
#       Initially used try/except, but that didn't want to work well
#   How to gracefully exit the recursion
"""

## Original Recursive logic
def move_pt(walk_map):
    x,y,_ = find_pt(walk_map)
    outside_dim = len(walk_map)
    while walk_map[x-1,y] in [".","X"]:
        if x == 0 or y == 0 or x == outside_dim or y == outside_dim:
            return np.sum(walk_map == "X")+1
            #print(np.sum(walk_map == "X")+1)   
            #exit()                             # crappy exit
        #print(x,y)                             # Used for debug
        walk_map[x,y] = "X"                     # mark current square
        walk_map[x-1,y] = "^"                   # move pt up one
        x,y,_ = find_pt(walk_map)               # update xy coords
    #print(walk_map)                             # Used for debug
    #print(np.sum(walk_map == "X")+1)            # Used for debug
    #input("Press Enter to continue...")         # Used for debug

    new_map = np.rot90(walk_map, k=1)
    return move_pt(new_map)  

## Improved Recursive logic
def move_pt_rec(walk_map):
    '''
    Original version, using recursive loop.
    Always moving forward, leave X trail behind until obstacle, then turn map.
    And recursive loop.  See below for original debug version, and notes.
    '''
    x,y,_ = find_pt(walk_map)
    outside_dim = len(walk_map)

    while walk_map[x-1,y] in [".","X"]:
        if x == 0 or y == 0 or x == outside_dim or y == outside_dim:
            return np.sum(walk_map == "X")+1    # return count of Xs
        walk_map[x,y] = "X"                     # mark current square
        walk_map[x-1,y] = "^"                   # move pt up one
        x,y,_ = find_pt(walk_map)               # update xy coords

    new_map = np.rot90(walk_map, k=1)           # turn map
    return move_pt_rec(new_map)                # recurse
"""