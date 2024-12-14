# Day 14 AoC 2024
# Using input14.txt data
# If I'm understanding this correctly, part one is merely math.
# Ignore the array aspect, in this case that is just a visualization.
# Simply perform multiplacation and reduce using modulo for the edges.


import re

EXP_1 = [
    "p=0,4 v=3,-3\n",
    "p=6,3 v=-1,-3\n",
    "p=10,3 v=-1,2\n",
    "p=2,0 v=2,-1\n",
    "p=0,0 v=1,3\n",
    "p=3,0 v=-2,-2\n",
    "p=7,6 v=-1,-3\n",
    "p=3,0 v=-1,-2\n",
    "p=9,3 v=2,3\n",
    "p=7,3 v=-1,2\n",
    "p=2,4 v=2,-3\n",
    "p=9,5 v=-3,-3\n",
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    clean = [row.strip() for row in dataset]
    return clean


def find_robots(cleaned):
    re_pattern = "p=(\d+),(\d+) v=(-*\d+),(-*\d+)"
    robots = []
    for row in cleaned:
        capture = re.match(re_pattern, row)
        robots.append([
            int(capture[1]),
            int(capture[2]),
            int(capture[3]),
            int(capture[4])
            ])
    return robots


def move_robot(inst, dims):
    x,y,v1,v2 = inst
    x_side, y_side = dims
    repeat = 100
    dist_x = (v1 * repeat) + x
    dist_y = (v2 * repeat) + y
    final_x = dist_x % x_side
    final_y = dist_y % y_side
    return [final_x, final_y]


def build_final(robots, dims):
    final = []
    for inst in robots:
        moved = move_robot(inst, dims)
        final.append(moved)
    return final


def count_quads(final, dims):
    mid_x = (dims[0] // 2) + 1
    mid_y = (dims[1] // 2) + 1
    #print(mid_x, mid_y)
    q1, q2, q3, q4 = 0,0,0,0
    for robot in final:
        x, y = robot[0] + 1, robot[1] + 1
        #print(x,y)
        if x < mid_x and y < mid_y:
            q1 += 1
        elif x > mid_x and y < mid_y:
            q2 += 1
        elif x < mid_x and y > mid_y:
            q3 += 1
        elif x > mid_x and y > mid_y:
            q4 += 1
        else:
            pass    # ignore those on mid lines
    #print([q1, q2, q3, q4])
    return q1 * q2 * q3 * q4


if __name__ == "__main__":   
    # dataset = EXP_1
    # cleaned = process(dataset)
    # robots = find_robots(cleaned)
    # dims = [11,7]
    # final = build_final(robots, dims)
    # safety = count_quads(final, dims)
    # print(safety)
    
    
    dataset = get_data("input14.txt")
    cleaned = process(dataset)
    robots = find_robots(cleaned)
    dims = [101,103]
    final = build_final(robots, dims)
    safety = count_quads(final, dims)
    print(safety)

