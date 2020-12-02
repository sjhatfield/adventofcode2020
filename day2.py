passwords = []

with open("Q2input", "r") as f:
    for line in f:
        passwords.append(line.replace("\n", "").split(" "))


def ans1():
    valid = 0
    for pwd in passwords:
        nums = pwd[0].split("-")
        minn = int(nums[0])
        maxx = int(nums[1])
        letter = pwd[1].replace(":", "")
        password = pwd[2]
        if minn <= password.count(letter) <= maxx:
            valid += 1
    return valid


def ans2():
    valid = 0
    for pwd in passwords:
        nums = pwd[0].split("-")
        idx1 = int(nums[0]) - 1
        idx2 = int(nums[1]) - 1
        letter = pwd[1].replace(":", "")
        password = pwd[2]
        if sum([password[idx1] == letter, password[idx2] == letter]) == 1:
            valid += 1
    return valid


print(ans1())

print(ans2())
