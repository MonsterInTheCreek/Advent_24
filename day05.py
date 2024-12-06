# Day 5 AoC 2024
# Using input05.txt data
# Input has two parts:
#   Lines 1 - 1176 are of form X|Y
#   Lines 1178 - 1378 are of form X,Y,Z... of variable length
#     These are of as few as 5 and as many as 23
#   In both all values are two digit ints with no decernable increase/decrease pattern
# If you feel ambitious, consider refactoring as rules and updates as classes


EXP_1 = [
    "47|53\n",
    "97|13\n",
    "97|61\n",
    "97|47\n",
    "75|29\n",
    "61|13\n",
    "75|53\n",
    "29|13\n",
    "97|29\n",
    "53|29\n",
    "61|53\n",
    "97|53\n",
    "61|29\n",
    "47|13\n",
    "75|47\n",
    "97|75\n",
    "47|61\n",
    "75|61\n",
    "47|29\n",
    "75|13\n",
    "53|13\n",
    "\n",
    "75,47,61,53,29\n",
    "97,61,53,29,13\n",
    "75,29,13\n",
    "75,97,47,61,53\n",
    "61,13,29\n",
    "97,13,75,29,47\n",
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    '''
    Transform initial dataset into two subs: rules (top) and updates (bottom).
    Then parse each set to transform from list of str to list of list of ints
    Args: dataset (list of strings) from text import
    Returns: tuple containing:
        rules_list (list of lists of ints) parsed rules
        updates_list (list of lists of ints) parsed updates
    '''
    rule_break_row = dataset.index("\n")    # find break between two sets
    rules = dataset[:rule_break_row]
    updates = dataset[rule_break_row + 1:]
    # confirmed above is correct break

    # transform list of strings into list of lists of int values 
    def _rules_split(rule):
        return [int(num) for num in rule.strip().split("|")]
    def _updates_split(update):
        return [int(num) for num in update.split(",")]
    rules_list = [_rules_split(rule) for rule in rules]
    updates_list = [_updates_split(update) for update in updates]
    
    # validate
    assert len(rules) + len(updates) + 1 == len(dataset), "initial transform failed"
    assert len(rules_list) == len(rules), "rules transform failed"
    assert len(updates_list) == len(updates), "updates transform failed"

    return updates_list, rules_list


def filter_rules(update, rules):
    '''
    Rules are dependent on the specific update
    Filter rules to only those where both X and Y are in update
    Args:
        update (list of ints) - a specific instance of updates
        rules (list of lists of ints)
    Returns: subset of rules (list of lists of ints)
    '''
    filtered_rules = []
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            filtered_rules.append(rule)
    return filtered_rules


def find_xy(update,rule):
    '''
    Find index values of X and Y values of specific rule in specific update
    '''
    x = rule[0]             # left value
    y = rule[1]             # right value
    x_i = update.index(x)
    y_i = update.index(y)
    return x_i, y_i


def test_update(update, filtered_rules):
    '''
    Boolean test whether a specific update is valid against given set of rules
    '''
    for rule in filtered_rules:
        x_i, y_i = find_xy(update, rule)
        if x_i > y_i:
            return False
    return True


def fix_update(update, filtered_rules):
    '''
    Modify value of (bad_)update in place    
    '''
    # Using modified logic of bool test above, for part 2
    for rule in filtered_rules:
        x_i, y_i = find_xy(update, rule)
        if x_i > y_i:
            # Fix update list - flip X and Y values
            update[x_i] = rule[1]
            update[y_i] = rule[0]
        else:
            pass    # Leave update as is


def solve_a(updates, rules):
    total = 0
    bad_updates = []
    for update in updates:
        filtered_rules = filter_rules(update, rules)
        if test_update(update, filtered_rules):
            middle_i = len(update) // 2     # find middle elem
            total += update[middle_i]
        else:
            bad_updates.append(update)      # for part 2
    print(f"Day 5, first = {total}")
    return bad_updates


def solve_b(bad_updates, rules):
    # still dependent on filtered rules logic
    total = 0
    for bad_update in bad_updates:
        filtered_rules = filter_rules(bad_update, rules)
        # loop until no errors remain
        while not test_update(bad_update, filtered_rules):
            fix_update(bad_update, filtered_rules)  # modify bad_update in place
        middle_i = len(bad_update) // 2             # find middle elem
        total += bad_update[middle_i]
    print(f"Day 5, second = {total}")


if __name__ == "__main__":   
    input = get_data("input05.txt")
    updates, rules = process(input)
    bad_updates = solve_a(updates, rules)
    solve_b(bad_updates, rules)


## Refactored into two functions:
"""
def test_update(update, filtered_rules):
    '''
    Boolean test whether a specific update is valid against given set of rules
    Args:
        update (list of ints) - a specific instance of updates
        filtered_rules (list of lists of ints) - MUST BE FILTERED
    Returns: True/False    
    '''
    for rule in filtered_rules:
        left = rule[0]
        right = rule[1]
        # index of left must be < index of right
        if update.index(left) > update.index(right):
            return False
    return True
"""