TEST = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""


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


assert ans1(read_input(TEST)) == 165

with open("day14input") as f:
    raw = f.read()
    print(ans1(read_input(raw)))
