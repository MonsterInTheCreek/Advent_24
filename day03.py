# Day 3 AoC 2024
# Using input03.txt data
# Input data is list of 6 long strings of variable length
# initial pattern == mul(n,n)


import re


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def preprocess(dataset):
    '''
    This feels kludgy, but should work.
    Use arbitrary Unicode symbols to replace do() and don't().
    Then loop through strings 'recording' the proper passages as preprocess.
    '''
    rec = "\u23fa"
    stop = "\u23f9"
    filtered = []
    record = True  # originally had this inside for loop, reset state each line
    for long_string in dataset:
        long_string = long_string.replace("do()", rec)
        long_string = long_string.replace("don't()", stop)
        temp_string = ""
        for let in long_string:
            if let == rec:
                record = True           # and go to next letter
            elif let == stop:
                record = False          # and go to next letter
            elif record == True:
                temp_string += let
        filtered.append(temp_string)    # maintain list of strings
    return filtered


def process(dataset):
    all_muls = []
    for long_string in dataset:
        regex_pattern = r"mul\((\d+),(\d+)\)"
        mul_list = re.findall(regex_pattern, long_string)
        all_muls += mul_list
    return all_muls
    

def solve_a(all_muls):
    total = 0
    for mul in all_muls:
        total += int(mul[0]) * int(mul[1])
    print(f"Day 3, first = {total}")


def solve_b(all_muls):
    total = 0
    for mul in all_muls:
        total += int(mul[0]) * int(mul[1])
    print(f"Day 3, second = {total}")


if __name__ == "__main__":   
    input_a = get_data("input03.txt")
    input_b = input_a.copy()
    muls_a = process(input_a)
    solve_a(muls_a)
    muls_b = preprocess(input_b)
    muls_b = process(muls_b)
    solve_b(muls_b)


## Original logic of part 2 I barfed the regex.  Then figured out correct regex.
## But still got wrong answer.
## After testing each list item individually with many debugs,
## I still couldn't see where it was wrong.  I had to look at Reddit.
## I thought state was resetting on each new list item.
## A bunch of people on Reddit with same issue.
## But the directions do specifically say that mul is enabled at beginning of
## program, not beginning of each new list item.  My mistake.

