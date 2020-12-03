trees = []

with open("Q3input", "r") as f:
    for line in f:
        trees.append(line.replace("\n", ""))


def ans1(tree_input):
    x = y = tree_count = 0
    while y < len(tree_input):
        if tree_input[y][x] == "#":
            tree_count += 1
        x += 3
        y += 1
        x %= len(tree_input[0])
    return tree_count


def ans2(tree_input, right, down):
    x = y = tree_count = 0
    while y < len(tree_input):
        if tree_input[y][x] == "#":
            tree_count += 1
        x += right
        y += down
        x %= len(tree_input[0])
    return tree_count


print(ans1(trees))

tree_prod = 1
for (r, d) in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    tree_prod *= ans2(trees, r, d)

print(tree_prod)
