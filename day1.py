nums = set()
with open("Q1ainput", "r") as f:
    for line in f:
        nums.add(int(line))


def ans1(numbers):
    for num in numbers:
        if 2020 - num in numbers:
            return num * (2020 - num)


def ans2(numbers):
    for num1 in numbers:
        for num2 in numbers:
            if 2020 - num1 - num2 in numbers:
                return num1 * num2 * (2020 - num1 - num2)


print(ans1(nums))

print(ans2(nums))
