# Day 19 AoC 2024
# Using input19.txt data
# Source data is 1 row of towel designs, a blank line, followed by 400 rows
# of target strings.  Towels set is 447 elems.
# Trying all combos of towels isn't feasible, it is an astronomical number.
# On a positive, don't need to solve for best solution for each target,
# Just whether it is possible or not.
# filter towels first by whether they are in target or not, that makes towel
# list much more manageable.  Testing all possible is still probably infeasible.
# maybe some way to continue to reduce possibility until testing all is possible
# over a much more limited set?

# giving up for now.  i can't think of a good way to approach this...

EXP_1 = [
    "r, wr, b, g, bwu, rb, gb, br\n",
    "\n",
    "brwrr\n",
    "bggr\n",
    "gbbr\n",
    "rrbgbr\n",
    "ubwu\n",
    "bwurrg\n",
    "brgr\n",
    "bbrgwb\n",
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    towels = [towel for towel in dataset[0].strip().split(", ")]
    targets = [target.strip() for target in dataset[2:]]
    return towels, targets


def build_towels_dict(towels, target):
    # allows for for loop of only applicable, and early quit
    towels_dict = {}
    for towel in towels:
        if towel in target:
            towels_dict[towel] = target.count(towel)
    return towels_dict


def test_target(towels, target):
    pass # magic happens


if __name__ == "__main__":
    dataset = get_data("input19.txt")
    #dataset = EXP_1
    towels, targets = process(dataset)
    for target in targets:
        print(build_towels_dict(towels, target))



# DEPRECATED
# def filter_towels(towels, target):
#     filtered_towels = []
#     for towel in towels:
#         if towel in target:
#             filtered_towels.append(towel)
#     return filtered_towels
