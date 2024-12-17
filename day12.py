# Day 12 AoC 2024
# Using input12.txt data

# Didn't write any code for this one.  Started exploratory, and didn't
# get further than that.  Not yet anyway...


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


#def process()
#more logic
#def solve_a()
#def solve_b()


if __name__ == "__main__":   
    input = get_data("input12.txt")
    reports = process(input)
    solve_a(reports)
    solve_b(reports)