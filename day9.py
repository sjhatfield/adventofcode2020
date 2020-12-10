from itertools import combinations

TEST1 = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""


def read_input(raw: str) -> list:
    return [int(num) for num in raw.split("\n") if num]


def ans1(formatted: list, preamble: int) -> int:
    previous = formatted[:preamble]
    for num in formatted[preamble:]:
        summ = False
        for combins in combinations(previous, 2):
            if sum(combins) == num:
                summ = True
        if not summ:
            return num
        else:
            del previous[0]
            previous.append(num)


assert ans1(read_input(TEST1), 5) == 127

with open("day9input") as f:
    raw = f.read()
    print(ans1(read_input(raw), 25))


def ans2(formatted: list, preamble: int) -> int:
    invalid = ans1(formatted, preamble)
    for i in range(len(formatted)):
        # Basic check for a little speed up
        if formatted[i] < invalid:
            for j in range(i + 1, len(formatted)):
                if formatted[j] < invalid:
                    if sum(formatted[i:j]) == invalid:
                        return max(formatted[i:j]) + min(formatted[i:j])


assert ans2(read_input(TEST1), 5) == 62

with open("day9input") as f:
    raw = f.read()
    print(ans2(read_input(raw), 25))
