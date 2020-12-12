from typing import List
import copy

TEST1 = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


def read_input(raw: str) -> List[List]:
    sp = raw.split("\n")
    mat = []
    for row, line in enumerate(sp):
        if line:
            mat.append([])
            for pos in line:
                mat[row].append(pos)
    return mat


def count_adjacents(mat: List[List], row, col) -> int:
    count = 0
    if row > 0:
        if col > 0:
            if mat[row - 1][col - 1] == "#":
                count += 1
        if col < len(mat[0]) - 1:
            if mat[row - 1][col + 1] == "#":
                count += 1
        if mat[row - 1][col] == "#":
            count += 1
    if row < len(mat) - 1:
        if col > 0:
            if mat[row + 1][col - 1] == "#":
                count += 1
        if col < len(mat[0]) - 1:
            if mat[row + 1][col + 1] == "#":
                count += 1
        if mat[row + 1][col] == "#":
            count += 1
    if col > 0:
        if mat[row][col - 1] == "#":
            count += 1
    if col < len(mat[0]) - 1:
        if mat[row][col + 1] == "#":
            count += 1
    return count


def count_adjacents_seen(mat: List[List], row, col) -> int:
    count = 0
    row_ = row - 1
    while row_ >= 0:
        if mat[row_][col] == "#":
            count += 1
            break
        elif mat[row_][col] == "L":
            break
        row_ -= 1

    row_ = row + 1
    while row_ <= len(mat) - 1:
        if mat[row_][col] == "#":
            count += 1
            break
        elif mat[row_][col] == "L":
            break
        row_ += 1

    col_ = col - 1
    while col_ >= 0:
        if mat[row][col_] == "#":
            count += 1
            break
        elif mat[row][col_] == "L":
            break
        col_ -= 1

    col_ = col + 1
    while col_ <= len(mat[0]) - 1:
        if mat[row][col_] == "#":
            count += 1
            break
        elif mat[row][col_] == "L":
            break
        col_ += 1

    row_ = row - 1
    col_ = col - 1
    while row_ >= 0 and col_ >= 0:
        if mat[row_][col_] == "#":
            count += 1
            break
        elif mat[row_][col_] == "L":
            break
        row_ -= 1
        col_ -= 1

    row_ = row + 1
    col_ = col - 1
    while row_ <= len(mat) - 1 and col_ >= 0:
        if mat[row_][col_] == "#":
            count += 1
            break
        elif mat[row_][col_] == "L":
            break
        row_ += 1
        col_ -= 1

    row_ = row - 1
    col_ = col + 1
    while row_ >= 0 and col_ <= len(mat[0]) - 1:
        if mat[row_][col_] == "#":
            count += 1
            break
        elif mat[row_][col_] == "L":
            break
        row_ -= 1
        col_ += 1

    row_ = row + 1
    col_ = col + 1
    while row_ <= len(mat) - 1 and col_ <= len(mat[0]) - 1:
        if mat[row_][col_] == "#":
            count += 1
            break
        elif mat[row_][col_] == "L":
            break
        row_ += 1
        col_ += 1

    return count


def one_iteration(mat: List[List]) -> List[List]:
    nextt = copy.deepcopy(mat)
    for row in range(len(mat)):
        for col in range(len(mat[0])):
            prev_state = mat[row][col]
            if prev_state != ".":
                count = count_adjacents(mat, row, col)
                if prev_state == "L" and count == 0:
                    nextt[row][col] = "#"
                elif prev_state == "#" and count >= 4:
                    nextt[row][col] = "L"
    return nextt


def one_iteration_seen(mat: List[List]) -> List[List]:
    nextt = copy.deepcopy(mat)
    for row in range(len(mat)):
        for col in range(len(mat[0])):
            prev_state = mat[row][col]
            if prev_state != ".":
                count = count_adjacents_seen(mat, row, col)
                if prev_state == "L" and count == 0:
                    nextt[row][col] = "#"
                elif prev_state == "#" and count >= 5:
                    nextt[row][col] = "L"
    return nextt


def ans1(mat: List[List]) -> int:
    prev = copy.deepcopy(mat)
    nextt = one_iteration(mat)
    while prev != nextt:
        prev = copy.deepcopy(nextt)
        nextt = one_iteration(prev)
    return sum([sum([entry == "#" for entry in row]) for row in nextt])


def ans2(mat: List[List]) -> int:
    prev = copy.deepcopy(mat)
    nextt = one_iteration(mat)
    while prev != nextt:
        prev = copy.deepcopy(nextt)
        nextt = one_iteration_seen(prev)
    return sum([sum([entry == "#" for entry in row]) for row in nextt])


assert ans1(read_input(TEST1)) == 37
assert ans2(read_input(TEST1)) == 26

with open("day11input") as f:
    raw = f.read()
    print(ans1(read_input(raw)))
    print(ans2(read_input(raw)))

