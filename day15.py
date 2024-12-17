# Day 15 AoC 2024
# Using input15.txt data


import numpy as np


EXP_1 = [
    "########\n",
    "#..O.O.#\n",
    "##.@O..#\n",
    "#...O..#\n",
    "#.#.O..#\n",
    "#...O..#\n",
    "#......#\n",
    "########\n",
    "\n",
    "<^^>>>vv<v>>v<<\n",
]

EXP_2 = [
    "##########\n",
    "#..O..O.O#\n",
    "#......O.#\n",
    "#.OO..O.O#\n",
    "#..O@..O.#\n",
    "#O#..O...#\n",
    "#O..O..O.#\n",
    "#.OO.O.OO#\n",
    "#....O...#\n",
    "##########\n",
    "\n",
    "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^\n",
    "vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v\n",
    "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<\n",
    "<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^\n",
    "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><\n",
    "^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^\n",
    ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^\n",
    "<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>\n",
    "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>\n",
    "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^\n",
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()
    

def process(dataset):
    # split into two datasets, the top map and bottom instructions
    # EXP_1, EXP_2, and import - all work
    warehouse = []
    wh_map = {
        ".":0,  # nothing
        "#":1,  # wall
        "O":2,  # box
        "@":3,  # robot
    }
    insts = ""
    insts_lines = 0
    for row in dataset:
        if row[0] == "#":
            row = row.strip()
            _temp = [wh_map[val] for val in row]
            warehouse.append(_temp)
        elif row[0] == "\n":
            pass    # do nothing
        else:
            row = row.strip()
            insts += row
            insts_lines += 1
    assert len(dataset) == len(warehouse) + 1 + insts_lines, "process() barfed"
    return np.array(warehouse), insts


def find_robot(wh_map):
    _x, _y = np.where(wh_map == 3)
    return (_x[0], _y[0])


def move_robot(wh_map, inst):
    # this is bit long, should probably refactor to abstract better
    here = find_robot(wh_map)
    up = np.array([-1,0])
    down = np.array([1,0])
    left = np.array([0,-1])
    right = np.array([0,1])
    if inst == ">":
        move = right
    elif inst == "<":
        move = left
    elif inst == "^":
        move = up
    elif inst == "v":
        move = down
    next_space = tuple(here + move)
    next_val = wh_map[next_space]
    if next_val == 1:       # if next is wall
        return wh_map       # pass, can't move wall
    elif next_val == 0:     # if next is space
        wh_map[here] = 0
        wh_map[next_space] = 3
        return wh_map
    elif next_val == 2:     # if next is box - branch logic
        boxes = 0
        spot = next_space
        while wh_map[tuple(spot)] == 2:     # solve for len of boxes
            boxes += 1
            spot = tuple(next_space + (boxes * move))
        if wh_map[spot] == 1:
            return wh_map   # pass, can't move wall
        elif wh_map[spot] == 0:
            boxes += 1      # dummy this up by 1
            wh_map[tuple(here)] = 0                     # first now blank
            wh_map[tuple(here + move)] = 3              # second now robot
            # boxes in middle can be ignored, they don't change
            wh_map[tuple(here + (boxes * move))] = 2    # last now box
            return wh_map


def loop_inst(wh_map, insts):
    for inst in insts:
        move_robot(wh_map, inst)
    return wh_map


def find_gps(wh_map):
    box_coords = np.argwhere(wh_map == 2)       # find coords for all boxes
    gps = 0
    for box in box_coords:
        gps += (box[0] * 100) + box[1]
    return gps


if __name__ == "__main__":   
    # dataset = EXP_2            
    # wh, insts = process(dataset)
    # final = loop_inst(wh, insts)
    # print(final)
    # gps = find_gps(final)
    # print(gps)


    dataset = get_data("input15.txt")
    wh, insts = process(dataset)
    final = loop_inst(wh, insts)
    #print(final)
    gps = find_gps(final)
    print(gps)

