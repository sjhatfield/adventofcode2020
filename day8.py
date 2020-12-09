TEST1 = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


def read_input(raw: str) -> list:
    instructions = []
    for line in raw.splitlines():
        instruction = line.split(" ")
        instructions.append((instruction[0], int(instruction[1])))
    return instructions


def ans1(instructions: list) -> (int, bool):
    accumulated = 0
    cur_idx = 0
    visited = []
    terminates = False
    while cur_idx not in visited:
        visited.append(cur_idx)
        instruction = instructions[cur_idx][0]
        value = instructions[cur_idx][1]
        if instruction == "nop":
            cur_idx += 1
        elif instruction == "acc":
            accumulated += value
            cur_idx += 1
        else:
            cur_idx += value
        if cur_idx == len(instructions):
            terminates = True
            break
    return accumulated, terminates


assert ans1(read_input(TEST1)) == (5, False)

with open("day8input", "r") as f:
    raw = f.read()
    print(ans1(read_input(raw)))


def ans2(instructions: list) -> int:
    for i, instruction in enumerate(instructions):
        if instruction[0] != "acc":
            if instruction[0] == "nop":
                test_instructions = (
                    instructions[:i]
                    + [("jump", instruction[1])]
                    + instructions[i + 1 :]
                )
                accumulate, terminates = ans1(test_instructions)
                if terminates:
                    return accumulate
            else:
                test_instructions = (
                    instructions[:i] + [("nop", instruction[1])] + instructions[i + 1 :]
                )
                accumulate, terminates = ans1(test_instructions)
            if terminates:
                return accumulate


assert ans2(read_input(TEST1)) == 8

with open("day8input", "r") as f:
    raw = f.read()
    print(ans2(read_input(raw)))
