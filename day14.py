TEST = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

TEST2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

from itertools import combinations_with_replacement, permutations


def read_input(raw: str) -> list:
    out = []
    first = True
    for sp in raw.strip().split("\n"):
        instr, value = sp.split("=")
        if instr[:2] == "ma":
            if not first:
                out.append(tup)
            tup = (value, [])
            first = False
        else:
            m = instr.rstrip().split("[")[1][:-1]
            tup[1].append((int(m), int(value)))
    out.append(tup)
    return out


def ans1(mask_list: list) -> int:
    memory_dict = dict()
    for (mask, memory_maps) in mask_list:
        mask_dict = dict()
        for i, m in enumerate(mask):
            if m != "X":
                mask_dict[i] = m
        for (inputt, output) in memory_maps:
            bin_out = str(bin(output))[2:]
            bin_out = "0" * (len(mask) - len(bin_out)) + bin_out
            change = False
            for i in mask_dict:
                if bin_out[i] != mask_dict[i]:
                    change = True
                    bin_out = bin_out[:i] + mask_dict[i] + bin_out[i + 1 :]
            if change:
                memory_dict[inputt] = int(bin_out, 2)
    return sum([val for val in memory_dict.values()])


def ans2(mask_list: list) -> int:
    memory_dict = dict()
    count = 0
    for (mask, memory_maps) in mask_list:
        mask = mask.strip()
        for (inputt, output) in memory_maps:
            bin_out = str(bin(inputt))[2:]
            bin_out = "0" * (len(mask) - len(bin_out)) + bin_out
            x_count = 0
            for i, m in enumerate(mask):
                if m != "0":
                    bin_out = bin_out[:i] + m + bin_out[i + 1 :]
                if m == "X":
                    x_count += 1
            permutations_done = set()
            for combo in combinations_with_replacement("01", x_count):
                for permutation in permutations(combo, len(combo)):
                    if permutation not in permutations_done:
                        permutations_done.add(permutation)
                        bin_out_copy = bin_out
                        while "X" in bin_out_copy:
                            replace_with = permutation[0]
                            permutation = permutation[1:]
                            idx = bin_out_copy.index("X")
                            bin_out_copy = (
                                bin_out_copy[:idx]
                                + replace_with
                                + bin_out_copy[idx + 1 :]
                            )
                        memory_dict[bin_out_copy] = output
    return sum([val for val in memory_dict.values()])


assert ans1(read_input(TEST)) == 165
assert ans2(read_input(TEST2)) == 208

with open("day14input") as f:
    raw = f.read()
    print(ans1(read_input(raw)))
    print(ans2(read_input(raw)))
