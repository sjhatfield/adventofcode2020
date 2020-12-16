from tqdm import tqdm


def ans(raw: str, want: int) -> int:
    numbers = [int(n) for n in raw.split(",") if n]
    idx = dict()
    for i, n in enumerate(numbers):
        # (most recent, second most recent)
        idx[n] = (i + 1, None)
    cur = numbers[-1]
    for turn in tqdm(range(len(numbers) + 1, want + 1)):
        if idx[cur][1] == None:
            if 0 not in idx:
                idx[0] = (turn, None)
            else:
                idx[0] = (turn, idx[0][0])
            cur = 0
        else:
            cur = idx[cur][0] - idx[cur][1]
            if cur not in idx:
                idx[cur] = (turn, None)
            else:
                idx[cur] = (turn, idx[cur][0])
    return cur


assert ans("0,3,6", 2020) == 436
assert ans("0,3,6", 30000000) == 175594

print(ans("9,19,1,6,0,5,4", 2020))
print(ans("9,19,1,6,0,5,4", 30000000))
