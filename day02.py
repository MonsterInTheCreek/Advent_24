# Day 2 AoC 2024
# Using input02.txt data


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(text_data):
    reports = []
    for row in text_data:
        elems = row.split()
        elems = list(map(int, elems))
        reports.append(elems)
    return reports


def prim_test(report):
    condition = True
    # report must be increasing or decreasing, else False
    condition = \
        report == sorted(report) or \
        report == sorted(report, reverse=True)
    # each increment must be 1, 2, or 3, else False
    for current, next in zip(report, report[1:]):
        if abs(current - next) not in [1,2,3]:
            condition = False
    return condition


def solve_a(reports):
    total = 0
    for report in reports:
        if prim_test(report):
            total += 1
    print(f"Day 2, first = {total}")


def sec_test(report):
    rep_len = len(report)
    # test versions of report missing 1 elem, any True, return True
    for i in range(0, rep_len):
        temp = report.copy()
        del temp[i]
        if prim_test(temp):
            return True     # exit as soon as True is found
    return False


def solve_b(reports):
    total = 0
    for report in reports:
        # try first test, if False, then try second test
        if prim_test(report):
            total += 1
        elif sec_test(report):
            total += 1
        else:
            pass  # explicit - do not increment total
    print(f"Day 2, second = {total}")


if __name__ == "__main__":   
    input = get_data("input02.txt")
    reports = process(input)
    solve_a(reports)
    solve_b(reports)

