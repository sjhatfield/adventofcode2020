from tqdm import tqdm
from typing import Union


def process(raw: str, part2: bool = False) -> list:
    if part2:
        cups = [0] * 1000000
    else:
        cups = [0] * len(raw)
    for i in range(len(raw) - 1):
        cups[int(raw[i]) - 1] = int(raw[i + 1])
    if part2:
        cups[int(raw[-1]) - 1] = 10
        for i in range(10, 1000000):
            cups[i - 1] = i + 1
    if part2:
        cups[999999] = int(raw[0])
    else:
        cups[int(raw[-1]) - 1] = int(raw[0])
    return cups, int(raw[0])


def move(cups: list, current: int, part2: bool = False) -> (list, int):
    removed = [
        cups[current - 1],
        cups[cups[current - 1] - 1],
        cups[cups[cups[current - 1] - 1] - 1],
    ]
    cups[current - 1] = cups[removed[2] - 1]
    dest = current - 1
    if part2:
        if dest < 1:
            dest = 1000000
        while dest in removed:
            dest -= 1
            if dest < 1:
                dest = 1000000
    else:
        if dest < 1:
            dest = 9
        while dest in removed:
            dest -= 1
            if dest < 1:
                dest = 9
    after_dest = cups[dest - 1]
    cups[dest - 1] = removed[0]
    cups[removed[2] - 1] = after_dest

    return cups, cups[current - 1]


def ans(cups, part2: bool = False) -> Union[int, str]:
    if part2:
        print(f"{cups[0]=}")
        print(f"{cups[cups[0]-1]=}")
        return cups[0] * cups[cups[0] - 1]
    else:
        ans = ""
        curr = cups[0]
        while len(ans) < 8:
            ans += str(curr)
            curr = cups[curr - 1]
        return ans


TEST = "389125467"
REAL = "614752839"

cups, current = process(REAL, True)
for _ in tqdm(range(10000000)):
    cups, current = move(cups, current, True)
print(ans(cups, True))
