# Day 4 AoC 2024
# Using input04.txt data
# input is list of 140 strings of 140 chars (less \n)
# made a lot of assumptions based on working with square arrays
# trying to use vector ops as much as possible, but some scalar ops remain
# learning vectorized ops is noble and time well spent
## but EARLY OPTIMIZATION IS EVIL

# This code is a little ugly, but it works...


import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


EXAMPLE = [
    "....XXMAS.\n",
    ".SAMXMS...\n",
    "...S..A...\n",
    "..A.A.MS.X\n",
    "XMASAMX.MM\n",
    "X.....XA.A\n",
    "S.S.S.S.SS\n",
    ".A.A.A.A.A\n",
    "..M.M.M.MM\n",
    ".X.X.XMASX\n",
]

EXAMPLE_2 = np.array(["M",".","S",".","A",".","M",".","S"])
EXAMPLE_2.shape = (3,3)


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset, shape):
    prep = [list(row)[:-1] for row in dataset]  # drop last \n char
    array = np.array(prep)
    array.shape = shape                         # reshape as square
    return array


### Part 1 logic ###

def get_horiz_vert(array):
    horiz_lr = array
    horiz_rl = np.flip(horiz_lr, axis=None)
    vert_ud = array.T
    vert_du = np.flip(vert_ud, axis=None)
    horiz_vert = np.vstack((horiz_lr, horiz_rl, vert_ud, vert_du))
    # transform into list of strings
    easy_stuff = ["".join(subarray) for subarray in horiz_vert] 
    return easy_stuff


def get_diags(array):
    # diagonals are more complicated:
    # flipping is less intuitive
    # np.diagonal() returns only one list at a time

    diag_range_num = len(array) - 1
    diag_range = range(-diag_range_num, diag_range_num + 1)
    all_diag = []
    for offset in diag_range:
        # order doesn't matter
        diag = np.diagonal(array, offset=offset)
        diag_flip = np.flip(diag, axis=None)
        anti_diag = np.diagonal(np.flip(array, axis=1), offset=offset)
        anti_diag_flip = np.flip(anti_diag, axis=None)
        # transform into list of strings
        temp = []
        temp.append("".join(diag))
        temp.append("".join(diag_flip))
        temp.append("".join(anti_diag))
        temp.append("".join(anti_diag_flip))
        all_diag += temp
    return all_diag
        

def solve_a(array):
    all = []
    all += get_horiz_vert(array)
    all += get_diags(array)
    total_xmas = 0
    for elem in all:
        total_xmas += elem.count("XMAS")
    print(f"Day 4, first = {total_xmas}")


### End of part 1 ###

### Part 2 logic ###

def get_Xs(array):
    '''
    Walk thru large array and return all sub-arrays in (3,3) shape
    Full transparency - got this function from ChatGPT
    '''
    all = sliding_window_view(array, window_shape=(3,3))
    # returns 4d hypercube, need to reshape
    reshaped = all.reshape(-1,3,3)
    return reshaped


def test_X(subarray):
    '''
    Return boolean for X array conforms with X-MAS
    '''
    diag = np.diagonal(subarray)
    anti_diag = np.diagonal(np.flip(subarray, axis=1))
    diag = "".join(diag)
    anti_diag = "".join(anti_diag)
    good_Xs = [
        ("MAS","MAS"),
        ("MAS","SAM"),
        ("SAM","MAS"),
        ("SAM","SAM"),
        ]
    if (diag, anti_diag) in good_Xs:
        return True
    else:
        return False


def solve_b(array):
    all = get_Xs(array)
    count_Xs = 0
    for subarray in all:
        if test_X(subarray):
            count_Xs += 1
    print(f"Day 4, second = {count_Xs}")

### End of part 2 ###


if __name__ == "__main__":
    # Using EXAMPLE from above:
    #exp_dims = len(EXAMPLE)                      
    #exp = process(EXAMPLE, (exp_dims, exp_dims))
    #solve_a(exp)

    input = get_data("input04.txt")
    dims = len(input)                            
    xmas = process(input, (dims, dims))
    solve_a(xmas)
    solve_b(xmas)


