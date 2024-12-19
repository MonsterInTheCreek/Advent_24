# Day 18 AoC 2024
# Using input18.txt data
# Source data is 3450 rows of graph coords as corrupted spots
# Graph is 0 to 70 on both x and y.  Upper left is 0,0 and bottom right is 70,70.
# Confirmed looking at dataset, 0 to 70 is inclusive of both ends.
# Goal to traverse from 0,0 to 70,70 without crossing any corrupted spots.

# Using networkx again.  This is kind of a cheat code, as I'm really relying
# on it to handle the heavy lifting of DFS.  But I still have to figure out
# how to get it to work.  Also Part 2 I didn't really implement a coded
# solution for, just manually walkled through binary search until I found the
# moment where the graph became unsolvable.


import numpy as np
import networkx as nx


EXP_1 = [
    "5,4\n",
    "4,2\n",
    "4,5\n",
    "3,0\n",
    "2,1\n",
    "6,3\n",
    "2,4\n",
    "1,5\n",
    "0,6\n",
    "3,3\n",
    "2,6\n",
    "5,1\n",
    "1,2\n",
    "5,5\n",
    "2,5\n",
    "6,5\n",
    "1,4\n",
    "0,4\n",
    "6,4\n",
    "1,1\n",
    "6,1\n",
    "1,0\n",
    "0,5\n",
    "1,6\n",
    "2,0\n",
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def build_array(dataset, dim, blocks):
    decrement = blocks
    array = np.zeros([dim+1, dim+1])
    for coord in dataset:
        row,col = coord.strip().split(",")
        array[int(col),int(row)] = 1
        decrement -= 1
        if decrement == 0:
            assert blocks == int(np.sum(array)), "blocks != coords"
            # array is now static.  use global to reduce pass IO / instantiation cost
            global STATIC_ARRAY
            STATIC_ARRAY = array
            return None # return nothing, array is global


def test_neighs(coords, dim):
    global STATIC_ARRAY
    up = np.array([-1,0])
    down = np.array([1,0])
    left = np.array([0,-1])
    right = np.array([0,1])
    all_moves = [up, down, left, right]
    possibilities = []
    for move in all_moves:
        neigh = coords + move
        if (neigh < 0).any() or (neigh > dim).any():
            pass    # outside bounds, ignore
        elif STATIC_ARRAY[tuple(neigh)] == 0:
            possibilities.append(neigh)
    return possibilities


def find_shortest(dim):
    global STATIC_ARRAY
    start = np.array([0,0])
    end = np.array([dim, dim])
    path_spots = np.where(STATIC_ARRAY == 0)
    spots = list(zip(path_spots[0],path_spots[1]))
    graph = nx.Graph()
    for spot in spots:
        neighs = test_neighs(spot, dim)
        for neigh in neighs:
            graph.add_edge(tuple(spot), tuple(neigh))
    short_path = nx.shortest_path(
        graph,
        source=tuple(start),
        target=tuple(end)
    )
    return len(short_path) - 1  # first square doesn't count as a step


if __name__ == "__main__":   
    # dataset = EXP_1
    # dim = 6
    # build_array(dataset, dim, 12)
    # #print(STATIC_ARRAY)
    # path = find_shortest(dim)
    # print(path)

    dataset = get_data("input18.txt")
    dim = 70
    build_array(dataset, dim, 2898)
    #print(STATIC_ARRAY)
    path = find_shortest(dim)
    print(path)


