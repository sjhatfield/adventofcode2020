from collections import defaultdict, deque


def reduce_moves(moves: defaultdict) -> defaultdict:
    # First cancel any opposing moves
    if "w" in moves and "e" in moves:
        e_w = min(moves["e"], moves["w"])
        moves["e"] -= e_w
        moves["w"] -= e_w
    if "ne" in moves and "sw" in moves:
        ne_sw = min(moves["ne"], moves["sw"])
        moves["ne"] -= ne_sw
        moves["sw"] -= ne_sw
    if "nw" in moves and "se" in moves:
        nw_se = min(moves["nw"], moves["se"])
        moves["nw"] -= nw_se
        moves["se"] -= nw_se

    # Now rewrite moves using just E, NW and SW
    if "w" in moves:
        while moves["w"] > 0:
            moves["w"] -= 1
            moves["nw"] += 1
            moves["sw"] += 1
        del moves["w"]
    if "ne" in moves:
        while moves["ne"] > 0:
            moves["ne"] -= 1
            moves["e"] += 1
            moves["nw"] += 1
        del moves["ne"]
    if "se" in moves:
        while moves["se"] > 0:
            moves["se"] -= 1
            moves["e"] += 1
            moves["sw"] += 1
        del moves["se"]

    # Get rid of loops and loops
    if "sw" in moves and "e" in moves and "nw" in moves:
        while moves["e"] > 0 and moves["sw"] > 0 and moves["nw"] > 0:
            moves["e"] -= 1
            moves["sw"] -= 1
            moves["nw"] -= 1

    # Should now just be two non-zero elements
    return moves


def convert_moves_to_tuple(moves: dict) -> tuple:
    # Converts the dictionary of E, NW, SW moves to
    # a tuple for hashing
    return (moves["e"], moves["nw"], moves["sw"])


def get_neighbors(E_NW_SW: tuple) -> list:
    # Gets the six neighbors of a tile in reduced tile tuple format
    pos = defaultdict(int)
    pos["e"] = E_NW_SW[0]
    pos["nw"] = E_NW_SW[1]
    pos["sw"] = E_NW_SW[2]
    neighbors = []
    # Find neighbors by moving one step in each of the directions
    for d in ["e", "sw", "nw", "ne", "se", "w"]:
        n = pos.copy()
        n[d] += 1
        neighbors.append(convert_moves_to_tuple(reduce_moves(n)))
    return neighbors


def step(flips: dict) -> dict:
    flips_next = flips.copy()
    # Track which tiles have already been checked as they
    # may be looked at more than once and this will save time
    checked = set()

    # Look all tiles currently black
    for E_NW_SW in flips:

        # Any tile adjacent to a black has the potential to become black
        potential_to_change = get_neighbors(E_NW_SW)

        # Check each neighbor of a black if they will be flipped
        for pot in potential_to_change:
            # Could have already been checked
            if pot not in checked:
                checked.add(pot)
                # Get 6 neighbors of tile to be checked
                neighbors = get_neighbors(pot)
                # Find how many are black
                black = 0
                for n in neighbors:
                    if n in flips:
                        black += 1
                # If was black already
                if pot in flips:
                    # May become white
                    if black == 0 or black > 2:
                        del flips_next[pot]
                # If was white
                else:
                    if black == 2:
                        flips_next[pot] = 1

        # Also check the original black tiles
        if E_NW_SW not in checked:
            checked.add(E_NW_SW)
            neighbors = get_neighbors(E_NW_SW)
            black = 0
            for n in neighbors:
                if n in flips:
                    black += 1
            # Just need to check if it will become black
            if black == 0 or black > 2:
                del flips_next[E_NW_SW]

    # Finally do some cleaning up
    flips_copy = flips_next.copy()
    # Make sure no white tiles are in the dict and set all black to one
    for E_NW_SW in flips_copy:
        if flips_copy[E_NW_SW] % 2 == 0:
            del flips_next[E_NW_SW]
        else:
            flips_next[E_NW_SW] = 1
    return flips_next


def line_to_dict(line: str) -> dict:
    line = deque([c for c in line.strip()])
    moves = defaultdict(int)
    while len(line) > 0:
        direction = line.popleft()
        if direction in "sn":
            direction += line.popleft()
        moves[direction] += 1
    return reduce_moves(moves)


def get_flips(raw: str) -> dict:
    flips = defaultdict(int)
    for line in raw.split("\n"):
        if line:
            moves = line_to_dict(line.strip())
            flips[(moves["e"], moves["nw"], moves["sw"])] += 1
    flips_copy = flips.copy()
    for f in flips_copy:
        if (flips_copy[f] % 2) == 0:
            del flips[f]
        else:
            flips[f] = 1
    return flips


TEST = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""


flips = get_flips(TEST)

for _ in range(100):
    flips = step(flips)
print(len(flips))

with open("day24input") as f:
    raw = f.read()
    flips = get_flips(raw)
    for _ in range(100):
        flips = step(flips)
    print(len(flips))

