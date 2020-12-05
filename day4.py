import re

ATTRIBUTES = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


raw_passports = []
passports = []

with open("Q4input", "r") as f:
    newline_count = 0
    entry = ""
    for line in f:
        if line == "\n":
            if len(entry) > 0:
                raw_passports.append(entry.rstrip())
                entry = ""
        else:
            entry += line.replace("\n", "") + " "
    raw_passports.append(entry.rstrip())

for entry in raw_passports:
    p = {}
    s = entry.split(" ")
    for t in s:
        att, val = t.split(":")
        p[att] = val
    passports.append(p)


def ans1(passpts):
    num = 0
    for passport in passpts:
        valid = True
        for att in ATTRIBUTES:
            if att not in passport:
                valid = False
        if valid:
            num += 1
    return num


def ans2(passpts):
    nums = 0
    for passport in passpts:
        valid = True
        for att in ATTRIBUTES:
            if att not in passport:
                valid = False
            elif att == "byr":
                if 1920 <= int(passport[att]) <= 2002:
                    pass
                else:
                    valid = False
            elif att == "iyr":
                if 2010 <= int(passport[att]) <= 2020:
                    pass
                else:
                    valid = False
            elif att == "eyr":
                if 2020 <= int(passport[att]) <= 2030:
                    pass
                else:
                    valid = False
            elif att == "hgt":
                if passport[att][-2:] == "cm":
                    if 150 <= int(passport[att][:-2]) <= 193:
                        pass
                    else:
                        valid = False
                elif passport[att][-2:] == "in":
                    if 59 <= int(passport[att][:-2]) <= 76:
                        pass
                    else:
                        valid = False
                else:
                    valid = False
            elif att == "hcl":
                if passport[att][0] == "#":
                    if len(re.findall("(\d|[a-f]){6}", passport[att][1:])) == 1:
                        pass
                    else:
                        valid = False
                else:
                    valid = False
            elif att == "ecl":
                if passport[att] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                    pass
                else:
                    valid = False
            elif att == "pid":
                if len(passport[att]) == 9:
                    if len(re.findall("\d{9}", passport[att])) == 1:
                        pass
                    else:
                        valid = False
                else:
                    valid = False
        if valid:
            nums += 1
    return nums


print(ans1(passports))

print(ans2(passports))
