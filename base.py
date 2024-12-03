# Day X AoC 2024
# Using inputXX.txt data


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


#def process()
#more logic
#def solve_a()
#def solve_b()


# change input
if __name__ == "__main__":   
    input = get_data("inputXX.txt")
    reports = process(input)
    solve_a(reports)
    solve_b(reports)