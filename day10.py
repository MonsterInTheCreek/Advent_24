# Day 10 AoC 2024
# Using input10.txt data
# Rules:
#   Input is topographic map, each number represents 0 (low) to 9 (high)
#   Trails are greedy to be as long as possible
#   Trails start at 0, end at 9, and increment by 1 per step
#   Movement is up/down/left/right, not diagonal
#   Each starting point 0 (trailhead) may reach more than one end at 9
#   Each path 0 to 9 adds score of 1 to a given trailhead 0
#   Important - multiple inside paths between a given 0 and 9 may exist,
#       but this particular 0->9 is a score of 1 only.  Internal path is arbitrary.
#   Solve for all trailheads score, remember rule above, and sum for solution.
# Source data is list of strings, each 45 x 45 chars (after \n removed) 0-9

# Goal essentially is to sum all unique 0 to 9 sets, 
# ignoring different paths from same 0 to same 9.
# Convert to numpy array.  then build a dict or other structure to store:
    # (x,y) cords
    # element value
    # applicable neighbors (this builds in 0-9 logic)
# then loop through all potential pairs nx.has_path

import numpy as np
import networkx as nx


EXP_1 = [
    "89010123\n",
    "78121874\n",
    "87430965\n",
    "96549874\n",
    "45678903\n",
    "32019012\n",
    "01329801\n",
    "10456732\n",
    ]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    clean = [list(row.strip()) for row in dataset]
    array = np.array(clean).astype(int)
    return array


def build_struct_array(array):
    graph = nx.DiGraph()            # instantiate networkx graph obj
    dim = array.shape[0]            # assumes square
    up = np.array([-1,0])           # dumbass, I swapped x and y
    down = np.array([1,0])          # but too late now, the code works
    left = np.array([0,-1])
    right = np.array([0,1])
    all_0 = []                      # no math or freq access
    all_9 = []                      # standard list is fine
    # walk thru all points and find edges
    # consider rewriting as vectorized
    for i in range(0,dim):          # i is up/down
        for j in range(0,dim):      # j is r/l
            here = np.array([i,j])
            here_val = array[i,j]
            neighs = np.array([
                here + up, 
                here + down, 
                here + left, 
                here + right
                ])
            neighs = neighs[np.all(neighs >= 0, axis=1)]    # filter out of bounds
            neighs = neighs[np.all(neighs < dim, axis=1)]       
            for elem in neighs:
                elem_val = array[tuple(elem)]
                if here_val - elem_val == 1:
                    graph.add_edge(tuple(elem), (i,j))
                elif elem_val - here_val == 1:
                    graph.add_edge((i,j), tuple(elem))
            # build coords for endpoints 0 and 9
            if here_val == 0:
                all_0.append([i,j])
            elif here_val == 9:
                all_9.append([i,j])
    # returned graph not all obj are numpy ints, why?
    return graph, all_0, all_9


def count_walks(graph, all_0, all_9):
    walks = 0
    for one_0 in all_0:
        for one_9 in all_9:
            if nx.has_path(graph, tuple(one_0), tuple(one_9)):
                walks += 1
    return walks

def count_paths(graph, all_0, all_9):
    paths = 0
    for one_0 in all_0:
        for one_9 in all_9:
            p = list(nx.all_simple_paths(graph, tuple(one_0), tuple(one_9)))
            paths += len(p)
    return paths

if __name__ == "__main__":
    # dataset = EXP_1
    # array = process(dataset)
    # graph, all_0, all_9 = build_struct_array(array)
    # g_edges = graph.edges() 
    # walks = count_walks(graph, all_0, all_9)
    # print(walks)


    dataset = get_data("input10.txt")
    array = process(dataset)
    graph, all_0, all_9 = build_struct_array(array)
    g_edges = graph.edges()  
    #walks = count_walks(graph, all_0, all_9)
    #print(walks)
    paths = count_paths(graph, all_0, all_9)
    print(paths)




'''
# never finished
def find_trees(i,j):
    # assumes already found starting point at (i,j)
    # probably lots of existing tree finding algorithms
    # find all possible routes, then late filter to only unique end points as score
    up, down, right, left = (-1,0), (1,0), (0,1), (0, -1)
    dirs = [up, down, right, left]
    hike_order = [x for x in range(0,10)]
    routes = []
'''
