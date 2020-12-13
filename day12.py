from typing import List

TEST = """
F10
N3
F7
R90
F11"""

DIRECTIONS = ["N", "E", "S", "W"]


def read_input(raw: str) -> List[tuple]:
    return [(line[0], int(line[1:])) for line in raw.split("\n") if line]


def execute(instruction: str, value: int, dists: dict, cur_dir: str) -> dict:
    if instruction == "F":
        instruction = cur_dir
    if instruction in DIRECTIONS:
        if instruction == "E":
            dists["E"] += value
        elif instruction == "W":
            dists["E"] -= value
        elif instruction == "N":
            dists["N"] += value
        else:
            dists["N"] -= value
    elif instruction in ["L", "R"]:
        rotation_idx = value // 90
        if instruction == "R":
            cur_dir = DIRECTIONS[
                (DIRECTIONS.index(cur_dir) + rotation_idx) % len(DIRECTIONS)
            ]
        else:
            cur_dir = DIRECTIONS[
                (DIRECTIONS.index(cur_dir) - rotation_idx) % len(DIRECTIONS)
            ]
    return dists, cur_dir


def rotate_waypoint(waypoint: dict, direction: str, value: int) -> dict:
    assert direction in ["L", "R"]
    # All rotations will be done in 90 steps clockwise so if direction is
    # L find out the equivalent R
    if direction == "L":
        value = 360 - value
    done = 0
    while done != value:
        waypoint["N"], waypoint["E"] = -waypoint["E"], waypoint["N"]
        done += 90
    return waypoint


def ans1(instructions: List[tuple]) -> int:
    cur_dir = "E"
    dists = {"E": 0, "N": 0}
    for instruction, value in instructions:
        dists, cur_dir = execute(instruction, value, dists, cur_dir)
    return sum([abs(val) for val in dists.values()])


def ans2(instructions: List[tuple]) -> int:
    ship = {"E": 0, "N": 0}
    waypoint = {"E": 10, "N": 1}
    for instruction, value in instructions:
        if instruction in DIRECTIONS:
            waypoint, _ = execute(instruction, value, waypoint, None)
        elif instruction in ["R", "L"]:
            waypoint = rotate_waypoint(waypoint, instruction, value)
        elif instruction == "F":
            east_dist = waypoint["E"] * value
            north_dist = waypoint["N"] * value
            ship["E"] += east_dist
            ship["N"] += north_dist
    return sum([abs(val) for val in ship.values()])


assert ans1(read_input(TEST)) == 25
assert ans2(read_input(TEST)) == 286

with open("day12input") as f:
    raw = f.read()
    print(ans1(read_input(raw)))
    print(ans2(read_input(raw)))
