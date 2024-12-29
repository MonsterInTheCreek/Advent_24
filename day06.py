# Day 6 AoC 2024
# Using input06.txt data
# Source data is 130 x 130 chars (once \n chars removed)
# Source is fully "." and "#" chars only, except one "^" char at (46,43)
# Find the steps?  # https://www.youtube.com/watch?v=S8D1YyNuunQ

### Completely refactored original code to optimize for Part 2

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


####### Part 1:


def process(dataset):
    # remove whitespace, and change symbols to numbers
    # find guard pos, change to 0, return guard pos and lab map
    cleaned = []
    row_num = 0
    for row in dataset:
        new_row = list(row.strip())
        char_map = {".":np.int8(0),"#":np.int8(1),"^":np.int8(2)}
        row_list = [char_map[let] for let in new_row]
        if 2 in row_list:       # capture initial guard position, and remove
            guard_i = row_list.index(2)
            guard = np.array((row_num, guard_i))
            row_list[guard_i] = 0
        cleaned.append(row_list)
        row_num += 1
    lab_map = np.array(cleaned)
    return guard, lab_map


def next_dir(dir):
    # always turn right
    dir_map = {"up":"right","right":"down","down":"left","left":"up"}
    return dir_map[dir]


def move_guard(guard, dir, log, lab_map):
    up = np.array([-1,0])
    down = np.array([1,0])
    left = np.array([0,-1])
    right = np.array([0,1])
    dir_map = {"up":up, "down":down, "left":left, "right":right}
    next_pos = guard + dir_map[dir]
    try:
        next_val = lab_map[tuple(next_pos)]
    except IndexError:
        # return arbitrary out of bounds value to break while loop
        log.add(tuple(guard))
        return np.array([-42,-42]), dir, log, lab_map
    if next_val == 1:       # do nothing but turn 90 degrees
        return guard, next_dir(dir), log, lab_map
    else:
        log.add(tuple(guard))
        return next_pos, dir, log, lab_map


def loop_guard(guard, lab_map):
    outside = len(lab_map)
    x,y = guard
    first_run = True
    start = time.time()
    while 0 < x < outside and 0 < y < outside:
        current = time.time()
        if first_run:
            guard, dir, log, lab_map = move_guard(guard, "up", set(), lab_map)
            first_run = False      
        else:
            guard, dir, log, lab_map = move_guard(guard, dir, log, lab_map)
        x,y = guard
    return log


####### Part 2 - optimized: remove log overhead
    # Tried optimizing using boolean True and False values instead of
    # np.int8 data type, but oddly bools were 20% slower
    # Clearly there are faster ways to do this
    # But my first try at Part 1 was going to take about four hours.  Now runs
    # in ~15 minutes.


def process_pt2(dataset):
    # remove whitespace, and change symbols to numbers
    # find guard pos, change to False, return guard pos and lab map
    cleaned = []
    row_num = 0
    for row in dataset:
        new_row = list(row.strip())
        char_map = {".":np.int8(0),"#":np.int8(1),"^":np.int8(2)}
        row_list = [char_map[let] for let in new_row]
        if 2 in row_list:       # capture initial guard position, and remove
            guard_i = row_list.index(2)
            guard = np.array((row_num, guard_i))
            row_list[guard_i] = 0
        cleaned.append(row_list)
        row_num += 1
    lab_map = np.array(cleaned)
    return guard, lab_map


def move_guard_pt2(guard, dir, lab_map):
    up = np.array([-1,0])
    down = np.array([1,0])
    left = np.array([0,-1])
    right = np.array([0,1])
    dir_map = {"up":up, "down":down, "left":left, "right":right}
    next_pos = guard + dir_map[dir]
    try:
        next_val = lab_map[tuple(next_pos)]
    except IndexError:
        # return arbitrary out of bounds value to break while loop
        return np.array([-42,-42]), dir, lab_map
    if next_val == 1:       # do nothing but turn 90 degrees
        return guard, next_dir(dir), lab_map
    else:
        return next_pos, dir, lab_map


def loop_guard_pt2(guard, lab_map):
    outside = len(lab_map)
    x,y = guard
    first_run = True
    start = time.time()
    while 0 < x < outside and 0 < y < outside:
        current = time.time()
        if first_run:
            guard, dir, lab_map = move_guard_pt2(guard, "up", lab_map)
            first_run = False
        elif current - start >= 0.25:      # if run time > 0.25 sec, inf loop
            return 1       
        else:
            guard, dir, lab_map = move_guard_pt2(guard, dir, lab_map)
        x,y = guard
    # Only return if infinite loop


def find_loopers(guard, lab_map):
    circles = 0
    outside = len(lab_map)
    # start = time.time()
    for i in range(0,outside):
        for j in range(0,outside):
            # this is not fast, can perform ~25 loop_guard() per second
            # if [i,j] == [0,25]:
            #     end = time.time()
            #     print(f"25 runs took {end - start:.2f}")
            #     input()
            new_map = lab_map.copy()
            new_map[i,j] = 1
            if loop_guard_pt2(guard, new_map) == 1:
                circles += 1
                print(f"circles = {circles} at {i},{j}")
            else:
                print(f"add block to {i},{j}")
                pass  # ignore
    return circles


if __name__ == "__main__":
    #dataset = EXP_1
    dataset = get_data("input06.txt")

    # part 1:
    #guard, lab_map = process(dataset)
    #log = loop_guard(guard, lab_map)
    #print(len(log))

    # part 2:
    guard, lab_map = process_pt2(dataset)
    circles = find_loopers(guard, lab_map)
    print(circles)

