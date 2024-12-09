# Day 7 AoC 2024
# Using input07.txt data
# Source data is 850 rows of strings like:
# "479027832: 8 9 69 659 96 634"

# Goal: find which rows are possible, return sum of nums on left
# Algorithm to calculate if left value can be produced by any combo of
# right nums using + and * operators.

# Already trying to optimize, but too early - EARLY OPTIMIZATION IS EVIL

from itertools import product
import time


EXP_1 = [
    "190: 10 19\n",
    "3267: 81 40 27\n",
    "83: 17 5\n",
    "156: 15 6\n",
    "7290: 6 8 6 15\n",
    "161011: 16 10 13\n",
    "192: 17 8 14\n",
    "21037: 9 7 18 13\n",
    "292: 11 6 16 20\n",
]
# True for part 1: 190, 3267, 292
# True for part 2: 190, 3267, 156, 7290, 192, 292

def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    # Quit with the clever code...  Trying to write this in two lines is dumb
    all_rows = []
    for row in dataset:
        op1, op2 = row.strip().split(":")
        op2 = op2.strip().split(" ")
        op1 = int(op1)
        op2 = [int(x) for x in op2]
        all_rows.append([op1, op2])
    return all_rows

# Never store full string, only work with underlying two sets: nums & ops

def build_eval_str(nums, ops):
    '''
    Join numbers and operators with parens to enforce eval order
    This logic only works for part 1
    Args:
        nums: list of ints, n in length
        ops: string of operators, will always be n-1 in length
    Return: string of numbers, operators, and parens
    '''
    nums_len = len(nums)
    eval_str = ""

    for i in range(0,nums_len):
        if i == 0:                          # first iter
            eval_str = ("(" * (nums_len - 1)) + str(nums[i]) + ops[i]
        elif i == nums_len - 1:             # last iter
            eval_str += str(nums[i]) + ")"
        else:                               # middle iters
            eval_str += str(nums[i]) + ")" + ops[i]
            
    return eval_str


def build_all_prods(opers, length):
    '''
    Build all Cartesian products of + and *
    Args:
        opers - (list of strings) operators
        length (int) - length of returned values
    Returns: prods (list of strings)
    '''
    #input = ["+","*"]       # Now an arg, for part 2
    prods_list = list(product(opers, repeat=length))
    # convert list of tuples into list of strings
    prods = ["".join(x) for x in prods_list]

    return prods


def test_row_1(row):
    target = row[0]
    nums = row[1]
    ops_len = len(nums) - 1
    opers = build_all_prods(["*","+"], ops_len)
    for oper in opers:
        test_str = build_eval_str(nums,oper)
        if eval(test_str) == target:
            return True
    return False      


def test_row_2(row):
    target = row[0]
    nums = row[1]
    ops_len = len(nums) - 1
    total = 0
    opers = build_all_prods(["*","+","|"], ops_len)
    for oper in opers:
        # not using build_eval_str()
        if oper[0] == "|":
            total = eval(str(nums[0]) + str(nums[1]))   # concat
        else:
            total = eval(str(nums[0]) + oper[0] + str(nums[1]))
        for i in range(1,ops_len):
            if oper[i] == "|":
                total = eval(str(total) + str(nums[i+1]))
            else:
                total = eval(str(total) + oper[i] + str(nums[i+1]))
        if total == target:
            return True
    return False


def solve_a(dataset):
    total = 0
    for row in dataset:
        if test_row_1(row):
            total += row[0]
    print(f"Day 7, first = {total}")


def solve_b(dataset):
    total = 0
    rows = 0
    start = time.time()
    for row in dataset:
        rows += 1
        if rows % 50 == 0:              # slow to run
            temp = time.time()
            print(f"50 processed.  Current time elapsed: {temp-start:.2f}")
        if test_row_2(row):
            total += row[0]
    end = time.time()
    print(f"Day 7, second = {total}")
    print(f"Total elapsed time = {end-start:.2f}")


if __name__ == "__main__":   
    #all_ops = process(EXP_1)
    #solve_a(all_ops)
    #solve_b(all_ops)

    input = get_data("input07.txt")
    all_ops = process(input)
    solve_a(all_ops)
    #solve_b(all_ops)            # very slow


## Early logic and exps
'''
def test_op(op):
    truth = False
    target = op[0]
    nums = op[1]
    op_len = len(nums)
    all_adds = ""
    for i in range(0,op_len):
        if i + 1 == op_len:
            all_adds += f"{nums[i]}"
        else:
            all_adds += f"{nums[i]}+"
    print(all_adds)
    return eval(all_adds)
    
def find_all_combos(op):
    ## Temporary function only
    ## Once logic is completed, add into test_op() so to allow for early exit
    op_len = len(op)
    opers = ["+" for _ in range(0,op_len)]
    all_adds = ""
    for i in range(0,op_len):
        all_adds += str(op[i]) + opers[i]
    print(all_adds)
    return eval(all_adds[:-1])

def mod_ops(eval_str, new_op, index):
    # "1+2+3+4+5", *, 2 --> "1+2+3*4"
    new_eval_str = eval_str[]
    #

def build_ops(nums):
    nums_len = len(nums)
    ops_len = nums_len - 1
    all_adds = ["+" * ops_len]
    current = all_adds.copy()
    all_ops = [current]
    for n in range(0,ops_len):
        current = "*" * n + "+" * (ops_len - n)
        for i in range(0,ops_len):
            temp = current
            all_adds.append(temp)


# First try of part 2 - got barfed on logic
def test_row(row, part, debug=False):
    debug_strings = []      # only used for part 2
    target = row[0]
    nums = row[1]
    ops_len = len(nums) - 1
    if part == 2:
        opers = build_all_prods(["*","+","|"], ops_len) # mod for part 2
    else:
        opers = build_all_prods(["*","+"], ops_len)     # part 1
    for oper in opers:
        test_str = build_eval_str(nums,oper)
        if part == 2:                                   # mod for part 2
            # Remove value ")|" first and then only "|" to essentially concat
            concat_num = test_str.count("|")
            # oh, this is getting kludgy...
            if oper[0] == "|":
                concat_num -= 1                     # need to remove 1 less "("
            test_str = test_str.replace(")|","")
            test_str = test_str.replace("|","")
            test_str = test_str[concat_num:]        # remove equal num of "("
            debug_strings.append(test_str)
        if eval(test_str) == target:
            return True
    if debug:
        print(debug_strings)
    return False
    
'''