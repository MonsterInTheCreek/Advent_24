# Day 1 AoC 2024
# Using input01.txt data


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(text_data):
    left, right = [], []
    for row in text_data:
        temp_l, temp_r = row.split()
        left.append(temp_l)
        right.append(temp_r)
        assert len(left) == len(right), "len of lists don't match"
    return left, right


def solve_a(left, right):
    left.sort()
    right.sort()
    total = 0
    row_num = len(left)
    for i in range(0, row_num):
        total += abs(int(left[i]) - int(right[i]))
    print(f"Day 1, first = {total}")


def solve_b(left, right):
    total = 0
    for num in left:
        total += int(num) * right.count(num)
    print(f"Day 1, second = {total}")


if __name__ == "__main__":
    input = get_data("input01.txt")
    left, right = process(input)
    solve_a(left, right)
    solve_b(left, right)