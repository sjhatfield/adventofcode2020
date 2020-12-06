bps = []

with open("Q5input", "r") as f:
    for line in f:
        bps.append((line[:7], line.replace("\n", "")[-3:]))


def get_row(row_raw):
    minn = 0
    maxx = 127
    while row_raw != "":
        if row_raw[0] == "F":
            maxx = (minn + maxx) // 2
        else:
            minn = (minn + maxx) // 2 + 1
        row_raw = row_raw[1:]
    return minn


def get_col(col_raw):
    minn = 0
    maxx = 7
    while col_raw != "":
        if col_raw[0] == "L":
            maxx = (minn + maxx) // 2
        else:
            minn = (minn + maxx) // 2 + 1
        col_raw = col_raw[1:]
    return minn


def get_id(row_raw, col_raw):
    return 8 * get_row(row_raw) + get_col(col_raw)


def ans1():
    max_id = -1
    for row, col in bps:
        idx = get_id(row, col)
        if idx > max_id:
            max_id = idx
    return max_id


def ans2():
    ids_present = []
    for row, col in bps:
        ids_present.append(get_id(row, col))
    return [
        x for x in range(min(ids_present), max(ids_present) + 1) if x not in ids_present
    ][0]


print(ans1())
print(ans2())
