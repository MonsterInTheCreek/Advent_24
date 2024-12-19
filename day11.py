# Day 11 AoC 2024
# Using input11.txt data
# Rules, in order of priority, where n is an individual stone:
# Per "blink", the only the first applicable occurs of:
#   1) for n, 0 becomes 1
#   2) if n % 2 == 0, n splits into two stones on midpoint (drop leading 0's)
#   3) n = n * 2024
# Order is always preserved

### Part 1, this code runs fine
### Part 2, not so much.  Poorly performant as scale of loops increases.
### In current form, cannot complete Part 2.  Refactor.
### May be able to improve performance by:
### Change list to numpy array
### Then stop storing as strings.  Refactor so only math is used for all steps.
### May be able to use bitwise ops if mulitplication is expensive?
### Could also be useful to debug current to identify specific bottleneck
### After further review, processing at scale won't work.
### By the time we are 35 loops in, the stone count is enormous.
### Processing per loop won't work at scale.
### Goal is to know number of stones at end.  If I can find loop/pattern...
### May be able to solve without math or for loop, at least in part.

### Taking a break from Part 2, need to think a bunch on how to do this.


EXP_1 = ["0 1 10 99 999\n"]
EXP_2 = ["125 17\n"]
EXP_3 = ["0"]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    # assumes only a single row in source data
    return [row.strip().split(" ") for row in dataset][0]


def apply_rules(stones, verbose=False):
    # some logic dependent on working with elems as str and others as ints
    # inside list, save elems as strings
    new_stones = []
    count = 0
    for stone in stones:
        count += 1
        if stone == "0":
            new_stones.append("1")
        elif len(stone) % 2 == 0:    # length is even
            midpt = int(len(stone)/2)
            new_stones.append(stone[:midpt])
            new_stones.append(stone[midpt:])
        else:
            new_stones.append(str(int(stone) * 2024))
        if verbose == True:
            print(f"Current loop = {count} of {len(stones)}")
    # force drop prefix 0's by changing each elem to int then back to string
    new_stones = [str(int(stone)) for stone in new_stones]
    return new_stones


def loop_rules(stones, loops):
    for loop in range(0,loops):
        if loop >= 35:
            stones = apply_rules(stones, True)
        else:
            stones = apply_rules(stones)
        print(f"Loop #{loop} complete")
    return stones



if __name__ == "__main__":
    # input = EXP_1
    # stones = process(input)
    # looped = loop_rules(stones, 1)
    # print(looped)
    # print(len(looped))


    input = get_data("input11.txt")
    #input = EXP_3
    stones = process(input)
    looped = loop_rules(stones, 25)
    print(len(looped))
