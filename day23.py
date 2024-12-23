# Day 23 AoC 2024
# Using input23.txt data
# Source data is 3380 rows of single pairs of LAN hosts a la "sb-ii"
# Edges are not directional.  Solve for all hosts that can be paired as
# three vertice cycle.  From this, filter to find all that contain at least
# one host that starts with "t".

# networkx is starting to feel like a Konami code...
import networkx as nx


EXP_1 = [
    "kh-tc\n",
    "qp-kh\n",
    "de-cg\n",
    "ka-co\n",
    "yn-aq\n",
    "qp-ub\n",
    "cg-tb\n",
    "vc-aq\n",
    "tb-ka\n",
    "wh-tc\n",
    "yn-cg\n",
    "kh-ub\n",
    "ta-co\n",
    "de-co\n",
    "tc-td\n",
    "tb-wq\n",
    "wh-td\n",
    "ta-ka\n",
    "td-qp\n",
    "aq-cg\n",
    "wq-ub\n",
    "ub-vc\n",
    "de-ta\n",
    "wq-aq\n",
    "wq-vc\n",
    "wh-yn\n",
    "ka-de\n",
    "kh-ta\n",
    "co-tc\n",
    "wh-qp\n",
    "tb-vc\n",
    "td-yn\n",
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def get_edges(dataset):
    edges = []
    for row in dataset:
        nodes = row.strip().split("-")
        edge = (nodes[0], nodes[1])
        edges.append(edge)
    return edges


def build_graph(edges):
    graph = nx.Graph()
    for edge in edges:
        #breakpoint()
        graph.add_edge(*edge)
    return graph


def find_cycles(graph, n=None):
    # find all n host cycles
    cycles = list(nx.simple_cycles(graph, n))
    return cycles


def filter_by_t(cycles):
    t_cycles = 0
    for cycle in cycles:
        a,b,c = cycle
        if a[0] == "t" or b[0] == "t" or c[0] == "t":
            t_cycles += 1
    return t_cycles


def get_cliques(graph):
    cliques = nx.find_cliques(graph)
    return cliques


def find_max(seq):
    # find and return longest in list
    # there's probably a built-in way to do this...
    ### later found i can use arg 'key' in max() to do this.
    current_max = []
    for elem in seq:
        if len(elem) > len(current_max):
            current_max = elem
    return current_max

    
def create_password(lan):
    lan.sort()
    pw = ",".join(lan)
    return pw


if __name__ == "__main__":   
    dataset = get_data("input23.txt")
    #dataset = EXP_1
    edges = get_edges(dataset)
    graph = build_graph(edges)
    ### part 1
    #cycles = find_cycles(graph, 3)
    #t_cycles = filter_by_t(cycles)
    ### part 2
    cliques = get_cliques(graph)
    largest = find_max(cliques)
    pw = create_password(largest)
    print(pw)



# First try at Part 2, no longer used
'''
def find_connections(graph):
    connections = list(nx.connected_components(graph))
    return connections
'''

