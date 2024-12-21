# Day 13 AoC 2024
# Using input13.txt data
# Favor B over A, solve for nearest with just B, then decrement B and increment
# A until total matches target.

# Need magic way to convert:
#   "Button A: X+94, Y+34\n",
#   "Button B: X+22, Y+67\n",
#   "Prize: X=8400, Y=5400\n",
# Into:
#   {"A":[94,34],"B":[22,67],"T":[8400,5400]}  

#### Solves example, but does not solve Part 1 successfully.
# There's some remaining logic to work out, like why the solved A factors don't
# always match, and whether I have logic of this "no more than 100" aspect correct.
# Giving up for now...  Difficult to debug when it solves the example, but I
# don't have anything else to help figure out why doesn't solve Part 1.

import re


EXP_1 = [
    "Button A: X+94, Y+34\n",
    "Button B: X+22, Y+67\n",
    "Prize: X=8400, Y=5400\n",
    "\n",
    "Button A: X+26, Y+66\n",
    "Button B: X+67, Y+21\n",
    "Prize: X=12748, Y=12176\n",
    "\n",
    "Button A: X+17, Y+86\n",
    "Button B: X+84, Y+37\n",
    "Prize: X=7870, Y=6450\n",
    "\n",
    "Button A: X+69, Y+23\n",
    "Button B: X+27, Y+71\n",
    "Prize: X=18641, Y=10279\n",
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def get_claws(dataset):
    claws = []
    counter = 0
    ab_pattern = "Button [AB]\: X\+(\d*), Y\+(\d*)"
    prize_pattern = "Prize\: X\=(\d*), Y\=(\d*)"
    for row in dataset:
        counter += 1
        if counter % 4 == 0:        # blank row, ignore
            pass
        elif counter % 4 == 1:      # Button A
            coords = re.search(ab_pattern, row)
            x,y = coords[1], coords[2]
            claws.append({"A":[x,y]})
        elif counter % 4 == 2:      # Button B
            coords = re.search(ab_pattern, row)
            x,y = coords[1], coords[2]
            claws[-1]["B"] = [x,y]
        elif counter % 4 == 3:      # Prize
            coords = re.search(prize_pattern, row)
            x,y = coords[1], coords[2]
            claws[-1]["T"] = [x,y]
    return claws


def solve_claw(claw):
    # find nearest solution for B only, then increment B down and A up
    Ax, Ay = int(claw["A"][0]), int(claw["A"][1])
    Bx, By = int(claw["B"][0]), int(claw["B"][1])
    Tx, Ty = int(claw["T"][0]), int(claw["T"][1])
    Btop = min(Tx // Bx, Ty // By)
    count = 0
    while Btop - count > 0:
        b_fact = Btop - count
        if (Tx - (Bx * b_fact)) % Ax == 0 \
            and (Ty - (By * b_fact)) % Ay == 0:
                a_fact_1 = (Tx - (Bx * b_fact)) / Ax
                a_fact_2 = (Ty - (By * b_fact)) / Ay
                if a_fact_1 != a_fact_2:
                    #print(f"A factors not equal.  They are {a_fact_1} and {a_fact_2}")
                    print(f"Ax={Ax}, Ay={Ay}, Bx={Bx}, By={By}, Tx={Tx}, Ty={Ty}, Bf={b_fact}, Af1={a_fact_1}, Af2={a_fact_2}")
                if a_fact_1 >= 100 or b_fact >= 100:
                    a_fact_1, b_fact = 0,0      # ignore big games?
                return (3 * a_fact_1) + b_fact
        count += 1
    return None     # not a possible combination


def count_tokens(claws):
    tokens = 0
    for claw in claws:
        this_game = solve_claw(claw)
        if this_game == None:
            pass    # couldn't solve, ignore
        else:
            tokens += this_game
    return tokens


if __name__ == "__main__":
    dataset = get_data("input13.txt")
    #dataset = EXP_1
    claws = get_claws(dataset)
    tokens = count_tokens(claws)
    print(tokens)

# the assert is throwing errors, showing that the two versions of A aren't
# equal.  unsure if this is truly and issue or not.
# first try solved for 77272.  -- too high
# second try after adding 100+ logic: 61495  -- too high
# third try after changing 100+ to or: 37134  -- too low
# there's the thing that each button need not be pressed more than 100 times.
# maybe this is an additional exclusion factor?