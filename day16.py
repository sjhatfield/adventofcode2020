TEST = """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

TEST2 = """
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""


def read_input(raw: str) -> (list, list, list):
    sp = raw.split("\n\n")
    field_names = [line.split(":")[0] for line in sp[0].split("\n") if line]
    fields_raw = [line.strip() for line in sp[0].split("\n") if line]
    fields_raw = [line.split(":")[1].strip() for line in fields_raw]
    fields_raw = [f.split("or") for f in fields_raw]
    fields_raw = [[f.split("-") for f in l] for l in fields_raw]
    fields = [[[int(v.strip()) for v in f] for f in l] for l in fields_raw]
    ticket = [num.strip() for num in sp[1].split(":")[1].split(",")]
    ticket = [int(t) for t in ticket]
    nearby = sp[2].split(":")[1]
    nearby = nearby.split("\n")
    nearby = [n.split(",") for n in nearby if n]
    nearby = [[int(n) for n in t] for t in nearby]
    return fields, ticket, nearby, field_names


def ans1(fields: list, nearby: list) -> int:
    ans = 0
    for ticket in nearby:
        for val in ticket:
            fits = False
            for field in fields:
                for rangee in field:
                    if rangee[0] <= val <= rangee[1]:
                        fits = True
            if not fits:
                ans += val
    return ans


def discard(fields: list, nearby: list) -> list:
    discard = []
    for i, ticket in enumerate(nearby):
        for val in ticket:
            fits = False
            for field in fields:
                for rangee in field:
                    if rangee[0] <= val <= rangee[1]:
                        fits = True
            if not fits:
                discard.append(i)
    valid = []
    for i in range(len(nearby)):
        if i not in discard:
            valid.append(nearby[i])
    return valid


def find_fields(fields, valid_nearby, field_names) -> dict:
    # Position (zero index), field name
    known = dict()
    # create a matrix of possible indices for each entry in each ticket
    valids = []
    for i, ticket in enumerate(valid_nearby):
        valids.append([])
        for j, t in enumerate(ticket):
            valid = []
            for k, field in enumerate(fields):
                if field[0][0] <= t <= field[0][1] or field[1][0] <= t <= field[1][1]:
                    valid.append(k)
            valids[-1].append(valid)
    # look at the validity matrix column wise and perform set intersection
    # if there is only one value in the set them it must be that field
    # remove that field as a possibility from all the others
    # repeat until all found
    while len(known) < len(valids[0]):
        for i in range(len(valids[0])):
            if i not in known:
                column_possiblity = set([k for k in range(len(valids[0]))])
                for j in range(len(valids)):
                    column_possiblity.intersection_update(valids[j][i])
                if len(column_possiblity) == 1:
                    known[i] = field_names[list(column_possiblity)[0]]
                    for row in valids:
                        for entry in row:
                            if list(column_possiblity)[0] in entry:
                                entry.remove(list(column_possiblity)[0])
    return known


def ans2(ticket: list, known: dict) -> int:
    ans = 1
    for idx, name in known.items():
        if name.startswith("departure"):
            ans *= ticket[idx]
    return ans


fields, ticket, nearby, field_names = read_input(TEST)
fields2, ticket2, nearby2, field_names2 = read_input(TEST2)

assert ans1(fields, nearby) == 71

with open("day16input") as f:
    raw = f.read()
    fields, ticket, nearby, field_names = read_input(raw)
    print(ans1(fields, nearby))
    print(ans2(ticket, find_fields(fields, discard(fields, nearby), field_names)))

