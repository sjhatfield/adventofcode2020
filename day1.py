nums = set()
with open("Q1ainput", "r") as f:
    for line in f:
        nums.add(int(line))


def ans1():
    for num in nums:
        if 2020 - num in nums:
            return num * (2020 - num)


def ans2():
    for num1 in nums:
        for num2 in nums:
            if 2020 - num1 - num2 in nums:
                return num1 * num2 * (2020 - num1 - num2)


print(ans1())

print(ans2())
