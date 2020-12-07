from collections import defaultdict

with open("Q6input", "r") as f:
    answers = f.readlines()


def ans1():
    total = 0
    cur = set()
    for ans in answers:
        if ans != "\n":
            for char in ans.replace("\n", ""):
                cur.add(char)
        else:
            total += len(cur)
            cur = set()
    total += len(cur)
    return total


def ans2():
    total = 0
    people = 0
    cur = defaultdict(int)
    for ans in answers:
        if ans != "\n":
            for char in ans.replace("\n", ""):
                cur[char] += 1
            people += 1
        else:
            for char in cur:
                if cur[char] == people:
                    total += 1
            cur = defaultdict(int)
            people = 0

    for char in cur:
        if cur[char] == people:
            total += 1
    return total


print(ans1())
print(ans2())
