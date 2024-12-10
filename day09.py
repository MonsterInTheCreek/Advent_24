# Day 9 AoC 2024
# Using input09.txt data
# Source data is a single row as one long string 20_000 chars long ending in \n
# All chars appear to be base 10 numbers
# I might not be smart enough to understand these instructions...

# CURRENTLY THIS CODE PASSES PART 1 EXAMPLE, BUT DOESN'T PASS SOURCE INPUT
# EFFECTIVELY PART 1 STILL INCOMPLETE

# Description examples:
#   "90909"  --> 999 (1 + 0 free + 9 + 0 free + 9)
#   "12345"  --> 1..3....5 (1 + 2 free + 3 + 4 free + 5)
#   Add IDs of 0 to n in sequential order to represent blocks
#   "12345" --> 1..3....5 --> 0..111....22222
#   Defrag by moving right nums to left free spots, one at a time
#   0..111....22222 --> 022111222......
#   Finally calculate checksum by each sum(num * i) for each num, i start at 0
#   ** Or something like that, may not be correct understanding yet **  

EXP_1 = "2333133121414131402\n"
EXP_2 = "12345\n"                       # example edge case, should be 60 - correct
EXP_3 = "1010101010101010101010\n"      # example edge case, should be 385, incorrect

'''
Needed functions:
Fun1: Transform initial string into fragmented string a la "n...m.....o"
Fun2: Transform that into version based on ID's
    When ID is larger than 9 does it become 10 or 0?
Fun3: Move numbers from right to left free spots, last to first
Fun4: Calculate checksum each sum(each num * incremental)
## A bunch here don't yet understand, and won't until we play with it some...

Manual walk thru of EXP_1 to confirm logic...
2 3 3 3 1 3 3 1 2 1 4 1 4 1 3 1 4 0 2
2...3...1...3.2.4.4.3.42
00...111...2...333.44.5555.6666.777.888899
0099811188827773336446555566
0  0  9  9  8  1  1  1  8  8  8  2  7  7  7  3  3  3  6  4  4  6  5  5  5  5  6  6
0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
0+0+18+27+32+5+6+7+64+72+80+22+84+91+98+45+48+51+108+76+80+126+110+115+120+125+156+162
== 1928, which is correct
'''


def get_data(file):
    with open(file,"r") as source:
        temp = source.readlines()
        return temp[0].strip()


def process(dataset):
    return dataset.strip()


def unzip(long_str):
    new_str = ""
    len_str = len(long_str)
    for i in range(0,len_str):
        if i % 2 == 0:
            new_str += long_str[i]
        else:
            new_str += "." * int(long_str[i])
    return new_str


def add_ids(unzipped):
    new_str = ""
    id = 0              # still don't know what happens when this reaches 10
    for elem in unzipped:
        #id = (id % 10)
        if elem == ".":
            new_str += elem
        else:
            new_str += int(elem) * str(id)
            id += 1
    return new_str


def move_nums(ids_str):
    # be really cautious with for loops, this will be changing state
    # assuming we don't need to keep the "." at the end.  Drop them.
    iters = 0
    while "." in ids_str:
        iters += 1
        if iters % 100 == 0:                    # slow
            print(f"processed {iters}")
        left = ids_str[:-1]
        right = ids_str[-1]
        if right == ".":
            ids_str = left
        for i in range(len(left)):
            if left[i] == ".":
                ids_str = ids_str[:i] + right + ids_str[i+1:-1]
                input(f"{ids_str}")        # debug
                break
    return ids_str


def build_checksum(defrag):
    len_str = len(defrag)
    checksum = 0
    for i in range(0,len_str):
        checksum += int(defrag[i]) * i
    return checksum


#def solve_a()
#def solve_b()


if __name__ == "__main__":    
    #processed = process(EXP_1)
    #processed = process(EXP_2)
    processed = process(EXP_3)
    unzipped = unzip(processed)
    ids = add_ids(unzipped)
    defragged = move_nums(ids)
    checksum = build_checksum(defragged)
    print(checksum)


    #dataset = get_data("input09.txt")
    #assert dataset[:10] == "7180145863"         # make sure I'm getting
    #assert dataset[-10:] == "0967439418"        # the whole thing
    #unzipped = unzip(dataset)
    #ids = add_ids(unzipped)
    #defragged = move_nums(ids)              # slow
    #checksum = build_checksum(defragged)
    #print(checksum)

    # Tried 91411296588 - too low