# Day 22 AoC 2024
# Using input22.txt data
# Source data is 1685 rows of ints stored as strings, most 6 to 8 digits
# For each initial number, perform following 2000 times:
#   n = prune(mix(n * 64, n))
#   n = prune(mix(n // 32, n))
#   n = prune(mix(n * 2048, n))
# Mix op: bitwise XOR --> example: 42 XOR 15 = 37
#       Translated as 101010 XOR 001111 (notice prefix 0) = 100101 = 32+4+1 = 37
# Prune op: mod 16777216 
# Probably not by accident that all ops are in base 2
# This is purely math ops.  The issue is that at scale this may be expensive.
# Best to perform as much as possible as bitwise ops.


EXP_1 = [
    "1\n",
    "10\n",
    "100\n",
    "2024\n",
]


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    secrets = []
    for row in dataset:    
        row = row.strip()
        secrets.append(int(row))
    return secrets


def mix(x, y):
    # bitwise XOR
    return x ^ y


def prune(x):
    # bitwise modulo by 16777216 (2^24)
    # bitwise x AND constant bitshift 2^24 - 1 equiv of modulo
    mod_const = ((1 << 24) - 1)
    return x & mod_const


def next_sec(secret):
    new_sec = prune(mix(secret << 6, secret))
    new_sec = prune(mix(new_sec >> 5, new_sec))
    new_sec = prune(mix(new_sec << 11, new_sec))
    return new_sec


def shift_num(secret, n):
    for i in range(0, n + 1):
        if i == 0:
            helper = secret
        else:
            helper = next_sec(helper)
            #print(f"{i}: {helper}")
    return helper


def sum_new(secrets):
    sec_sum = 0
    for secret in secrets:
        #print(f"{secret}: {shift_num(secret, 2000)}")
        sec_sum += shift_num(secret, 2000)
    return sec_sum


if __name__ == "__main__":   
    #dataset = EXP_1
    dataset = get_data("input22.txt")
    secrets = process(dataset)
    sums = sum_new(secrets)
    print(sums)