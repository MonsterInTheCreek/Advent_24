# Day 25 AoC 2024
# Using input25.txt data
# Source data is approx 4000 rows of 7 rows + 1 blank row of 5 chars wide
# Those with full ##### top rows representing locks, and those with #####
# bottom rows representing keys.  250 locks and 250 keys.


EXP_1 = [
    "#####\n",
    ".####\n",
    ".####\n",
    ".####\n",
    ".#.#.\n",
    ".#...\n",
    ".....\n",
    "\n",
    "#####\n",
    "##.##\n",
    ".#.##\n",
    "...##\n",
    "...#.\n",
    "...#.\n",
    ".....\n",
    "\n",
    ".....\n",
    "#....\n",
    "#....\n",
    "#...#\n",
    "#.#.#\n",
    "#.###\n",
    "#####\n",
    "\n",
    ".....\n",
    ".....\n",
    "#.#..\n",
    "###..\n",
    "###.#\n",
    "###.#\n",
    "#####\n",
    "\n",
    ".....\n",
    ".....\n",
    ".....\n",
    "#....\n",
    "#.#..\n",
    "#.#.#\n",
    "#####\n"
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    # probably better to refactor this into two functions...
    locks = []
    keys = []
    data_str = "".join(dataset)
    # use double newline chars as logical break
    data_list = data_str.split("\n\n")
    data_list_of_lists = [n.split("\n") for n in data_list]
    for elem in data_list_of_lists:
        new_elem = []
        for row in elem:
            # change # to 1, . to 0, and remove newline char
            new_row = row.replace("#","1").replace(".","0").strip()
            if new_row != "":       # exclude empty string at end of source
                new_elem.append(new_row)
        if new_elem[0] == "11111":      # indicates lock
            locks.append(new_elem)
        elif new_elem[6] == "11111":    # indicates key
            keys.append(new_elem)
        else:
            raise ValueError(f"source elem not key or lock:\n{new_elem}")
    return locks, keys


def elems_to_strs(elems):
    # convert elems (locks and keys) from visual form to number string form
    # good opportunity to refactor as class instantiation
    #     if so, add "12345" + "33333" = "45678" function
    new_elems = []
    for elem in elems:
        new_elem = ""
        for col in range(0,5):
            temp = sum([int(n[col]) for n in elem]) - 1     # remove base line
            assert temp >= 0 and temp <= 6, "bad elem:\n{elem}"
            new_elem += str(temp)
        new_elems.append(new_elem)
    return new_elems


def test_combos(locks, keys):
    # equal number of locks and keys, no benefit to looping one vs other
    good_fits = 0
    def _add_cols(elem1, elem2):
        # leaves in list of ints form, intentionally for debug
        return [int(elem1[n]) + int(elem2[n]) for n in range(0,5)]
    for lock in locks:
        for key in keys:
            #breakpoint()
            if all(x <= 5 for x in _add_cols(lock, key)):
                good_fits += 1
    return good_fits


if __name__ == "__main__":   
    dataset = get_data("input25.txt")
    #dataset = EXP_1
    locks, keys = process(dataset)
    locks = elems_to_strs(locks)
    keys = elems_to_strs(keys)
    good_fits = test_combos(locks, keys)
    print(good_fits)
