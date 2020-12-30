from tqdm import tqdm


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def process(raw: str, part2=False) -> (ListNode, int):
    first = ListNode(int(raw[0]))
    # Pointer to create linked list
    ptr = first
    for char in raw[1:]:
        ptr.next = ListNode(int(char))
        ptr = ptr.next
    # If part 2 append nodes up to one million
    if part2:
        i = max([int(char) for char in raw]) + 1
        while i <= 1e6:
            ptr.next = ListNode(i)
            ptr = ptr.next
            i += 1
    # Loop back around
    ptr.next = first
    return first


def move(current: ListNode, part2=False) -> ListNode:
    ptr = current.next

    # Create the 3 node linked list of removed values
    removed = ListNode(ptr.val)
    removed_ptr = removed
    removed_values = [ptr.val]
    for _ in range(2):
        ptr = ptr.next
        removed_values.append(ptr.val)
        removed_ptr.next = ListNode(ptr.val)
        removed_ptr = removed_ptr.next

    # Set the current linked list to skip the removed part
    current.next = current.next.next.next.next

    # Find the destination value
    dest = current.val - 1
    if dest < 1:
        if part2:
            dest = 1000000
        else:
            dest = 9
    while dest in removed_values:
        dest -= 1
        if dest < 1:
            if part2:
                dest = 1000000
            else:
                dest = 9

    # Find the destination node
    dest_ptr = current
    while dest_ptr.val != dest:
        dest_ptr = dest_ptr.next

    # Insert the removed linked list inbetween the destination and
    # the node after it
    after_dest = dest_ptr.next
    dest_ptr.next = removed
    removed.next.next.next = after_dest

    # Return the node after current
    return current.next


def ans(current, part2=False):
    if part2:
        ptr = current
        while ptr.val != 1:
            ptr = ptr.next
        return ptr.next.val * ptr.next.next.val
    else:
        ptr = current
        while ptr.val != 1:
            ptr = ptr.next
        ans = ""
        ptr = ptr.next
        while ptr.val != 1:
            ans += str(ptr.val)
            ptr = ptr.next
    return ans


TEST = "389125467"
REAL = "614752839"

current = process(TEST, True)

for _ in tqdm(range(10000000)):
    current = move(current, True)
print(ans(current, True))

"""
# Part 1 ans
def move(cups: list, current: int):
    removed = []
    min_cup, max_cup = min(cups), max(cups)
    current_idx = cups.index(current)
    for i in range(1, 4):
        removed.append(cups[(current_idx + i) % len(cups)])
    dest_cup = current - 1
    if dest_cup < min_cup:
        dest_cup = max_cup
    while dest_cup in removed:
        dest_cup -= 1
        if dest_cup < min_cup:
            dest_cup = max_cup
    idx = [cups.index(dest_cup), cups.index(current)]
    for r in removed:
        idx.append(cups.index(r))
    idx.append(-1)
    idx.append(len(cups))
    new_cups = []
    for i in idx[:-1]:
        new_cups = cups[i : i + 1]
        new_cups.append(cups[i])
    return new_cups, new_cups[(new_cups.index(current) + 1) % len(new_cups)]


def get_ans(cups):
    ans = ""
    cur = (cups.index(1) + 1) % len(cups)
    for _ in range(len(cups) - 1):
        ans += str(cups[cur])
        cur = (cur + 1) % len(cups)
    return ans


def full1(raw, moves):
    cups = [int(n) for n in raw]
    current = cups[0]
    for _ in range(moves):
        cups, current = move(cups, current)
        print(f"{cups=}")
    return get_ans(cups)


assert full1(TEST, 10) == "92658374"
assert full1(TEST, 100) == "67384529"
"""

