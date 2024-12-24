# Day 24 AoC 2024
# Using input24.txt data


EXP_1 = [
    "x00: 1\n",
    "x01: 1\n",
    "x02: 1\n",
    "y00: 0\n",
    "y01: 1\n",
    "y02: 0\n",
    "\n",
    "x00 AND y00 -> z00\n",
    "x01 XOR y01 -> z01\n",
    "x02 OR y02 -> z02\n",
]

EXP_2 = [
    "x00: 1\n",
    "x01: 0\n",
    "x02: 1\n",
    "x03: 1\n",
    "x04: 0\n",
    "y00: 1\n",
    "y01: 1\n",
    "y02: 1\n",
    "y03: 1\n",
    "y04: 1\n",
    "\n",
    "ntg XOR fgs -> mjb\n",
    "y02 OR x01 -> tnw\n",
    "kwq OR kpj -> z05\n",
    "x00 OR x03 -> fst\n",
    "tgd XOR rvg -> z01\n",
    "vdt OR tnw -> bfw\n",
    "bfw AND frj -> z10\n",
    "ffh OR nrd -> bqk\n",
    "y00 AND y03 -> djm\n",
    "y03 OR y00 -> psh\n",
    "bqk OR frj -> z08\n",
    "tnw OR fst -> frj\n",
    "gnj AND tgd -> z11\n",
    "bfw XOR mjb -> z00\n",
    "x03 OR x00 -> vdt\n",
    "gnj AND wpb -> z02\n",
    "x04 AND y00 -> kjc\n",
    "djm OR pbm -> qhw\n",
    "nrd AND vdt -> hwm\n",
    "kjc AND fst -> rvg\n",
    "y04 OR y02 -> fgs\n",
    "y01 AND x02 -> pbm\n",
    "ntg OR kjc -> kwq\n",
    "psh XOR fgs -> tgd\n",
    "qhw XOR tgd -> z09\n",
    "pbm OR djm -> kpj\n",
    "x03 XOR y03 -> ffh\n",
    "x00 XOR y04 -> ntg\n",
    "bfw OR bqk -> z06\n",
    "nrd XOR fgs -> wpb\n",
    "frj XOR qhw -> z04\n",
    "bqk OR frj -> z07\n",
    "y03 OR x01 -> nrd\n",
    "hwm AND bqk -> z03\n",
    "tgd XOR rvg -> z12\n",
    "tnw OR pbm -> gnj\n",
]


import re


def get_data(file):
    with open(file,"r") as source:
        return source.readlines()


def process(dataset):
    # use regex to capture data points from both top values and bottom gates
    values = {}
    gates = []
    top = True
    values_re = "(\w\d{2}): (\d)"
    gates_re = "([\d\w]{3}) (\w*) ([\d\w]{3}) -> ([\d\w]{3})"
    for row in dataset:
        if row == "\n":         # switch from values to gates
            top = False
        elif top:
            capture = re.search(values_re, row)
            var = capture[1]
            val = int(capture[2])
            values[var] = val
        else:
            capture = re.search(gates_re, row)
            input1 = capture[1]
            operand = capture[2]
            input2 = capture[3]
            target = capture[4]
            gates.append([input1, input2, operand, target])
    return values, gates


def update(values, gates):
    ## Potential concern - treating bit values as base 10, not base 2
    #  Update values and gates, and test whether any changes occured
    new_gates = []
    debug_loops = 0
    ops = {"AND":"&", "OR":"|", "XOR":"^"}
    made_mod = False                        # pass out whether any mods occured
    for gate in gates:
        input1, input2, operand, target = gate
        new1 = values.get(input1, input1)
        new2 = values.get(input2, input2)
        if (
            isinstance(target, str) and     # target not yet int
            isinstance(new1, int) and       # new1/input1 not still str
            isinstance(new2, int)           # new2/input2 not still str
        ):
            debug_loops += 1
            new_targ = eval(str(new1) + ops[operand] + str(new2))
            values[target] = new_targ
            made_mod = True
            new_gates.append([new1, new2, operand, new_targ])
        else:
            new_gates.append([new1, new2, operand, target])
    return values, new_gates, made_mod


def find_z_vals(values, gates):
    # loop updating values and gates until no changes occur
    made_mod = True
    while made_mod:
        values, gates, made_mod = update(values, gates)
    # filter values to just those that start with "z"
    z_vals = {k:values[k] for k in values.keys() if k[0] == "z"}
    return z_vals


def get_num(z_vals):
    # sort "z" values, then join into string and convert from bin to dec
    sorted_keys = [k for k in sorted(z_vals.keys(), reverse=True)]
    bin_list = [str(z_vals[k]) for k in sorted_keys]
    bin_str = "".join(bin_list)
    num = int(bin_str, 2)
    return num


if __name__ == "__main__":   
    dataset = get_data("input24.txt")
    #dataset = EXP_2
    values, gates = process(dataset)
    z_vals = find_z_vals(values, gates)
    num = get_num(z_vals)
    print(num)