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
###     In current form, cannot complete Part 2.  Refactor.


EXP_1 = ["0 1 10 99 999\n"]
EXP_2 = ["125 17\n"]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    # assumes only a single row in source data
    return [row.strip().split(" ") for row in dataset][0]


def apply_rules(stones):
    # some logic dependent on working with elems as str and others as ints
    # inside list, save elems as strings
    new_stones = []
    for stone in stones:
        if stone == "0":
            new_stones.append("1")
        elif len(stone) % 2 == 0:    # length is even
            midpt = int(len(stone)/2)
            new_stones.append(stone[:midpt])
            new_stones.append(stone[midpt:])
        else:
            new_stones.append(str(int(stone) * 2024))
    # force drop prefix 0's by changing each elem to int then back to string
    new_stones = [str(int(stone)) for stone in new_stones]
    return new_stones


def loop_rules(stones, loops):
    for loop in range(0,loops):
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
    stones = process(input)
    looped = loop_rules(stones, 50)
    print(len(looped))
