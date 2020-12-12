from functools import lru_cache

TEST1 = """16
10
15
5
1
11
7
19
6
12
4"""

TEST2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""


def read_input(raw: str) -> tuple:
    return tuple([int(num) for num in raw.split("\n") if num])


def ans1(formatted: tuple) -> int:
    formatted = tuple(sorted(formatted))
    cur = 0
    one_count = 0
    three_count = 0
    for f in formatted:
        if f - cur == 1:
            one_count += 1
        elif f - cur == 3:
            three_count += 1
        cur = f
    return one_count * (three_count + 1)


assert ans1(read_input(TEST1)) == 35
assert ans1(read_input(TEST2)) == 220

with open("day10input") as f:
    raw = f.read()
    print(ans1(read_input(raw)))


def ans2(formatted: list) -> int:
    formatted = sorted(formatted)
    formatted.append(formatted[-1] + 3)
    formatted = [0] + formatted
    formatted = tuple(formatted)

    @lru_cache(maxsize=None)
    def recursive_count(adapters: tuple) -> int:
        if len(adapters) > 1:
            ret = 0
            last = adapters[-1]
            for i in range(1, 4):
                if -(i + 1) >= -len(adapters):
                    adapt = adapters[-(i + 1)]
                    if last - adapt <= 3:
                        ret += recursive_count(adapters[:-i])
            return ret

        else:
            return 1

    return recursive_count(formatted)


print(ans2(read_input(TEST1)))
print(ans2(read_input(TEST2)))

assert ans2(read_input(TEST1)) == 8
assert ans2(read_input(TEST2)) == 19208

with open("day10input") as f:
    raw = f.read()
    print(ans2(read_input(raw)))
