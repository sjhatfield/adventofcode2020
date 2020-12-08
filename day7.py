# Test cases given
TEST = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

TEST2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

# Processes the input into a dictionary where the key is the bag
# that contains other bags. The value is a list of tuples
# of bags and the number that must be within the parent bag
def process_input(text: str) -> dict:
    bag_rules = dict()
    lines = text.split("\n")
    for line in lines:
        contain = line.split("contain")
        # Avoid blank line issue
        if len(contain) > 1:
            outer = contain[0][:-6]
            inner = contain[1].split(",")
            bag_rules[outer] = []
            for inn in inner:
                sp = inn.split(" ")
                if sp[1] == "no":
                    break
                num = int(sp[1])
                color = sp[2] + " " + sp[3]
                bag_rules[outer].append((color, num))
    return bag_rules


def ans1(bag_rules: dict, color: str = "shiny gold") -> int:
    ans_after = set([color])
    # Loop over the bag rules adding bags to the set of bags needed
    # if the set of bags is unchanged then we are done
    while True:
        ans_prev = ans_after.copy()
        for outer in bag_rules:
            for inner in bag_rules[outer]:
                if inner[0] in ans_prev:
                    ans_after.add(outer)
        if len(ans_after) == len(ans_prev):
            break
    return len(ans_prev) - 1


# Get the inputs for testing
test_input = process_input(TEST)
test_input2 = process_input(TEST2)

# Get the real input to answer the questions
with open("day7input") as f:
    raw = f.read()
    real_input = process_input(raw)

# Test answer 1
assert ans1(test_input) == 4

# Get true answer 1
print(ans1(real_input))


def ans2(bag_rules, color="shiny gold"):
    # Use a stack to iteratively go deeper into the bags
    parents = bag_rules[color]
    ans = sum([p[1] for p in parents])
    while parents:
        parent = parents.pop()
        children = bag_rules[parent[0]]
        for child in children:
            if child[1]:
                ans += parent[1] * child[1]
            parents.append((child[0], parent[1] * child[1]))
    return ans


assert ans2(test_input2) == 126

print(ans2(real_input))
