TEST = """
.#.
..#
###
"""

REAL = """
.#..####
.#.#...#
#..#.#.#
###..##.
..##...#
..##.###
#.....#.
..##..##
"""

def generate_intial(raw: str) -> dict:
    # states keys: (t, z, x, y)
    states = dict()
    rows = raw.splitlines()
    for r, row in enumerate(rows):
        for c, char in enumerate(row):
            if char == "#":
                states[(0,0,r,c)] = "#"
    return states

def get_neighbors_active(states_key, states):
    time = states_key[0]
    z = states_key[1]
    x = states_key[2]
    y = states_key[3]
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if (time, z + i, x + j, y + k) in states:
                    if not (i == 0 and j == 0 and k == 0):
                        if states[(time, z+i, x+j, y+k)] == "#":
                            neighbors += 1
    return neighbors

def get_neighbors(states_key):
    time = states_key[0]
    z = states_key[1]
    x = states_key[2]
    y = states_key[3]
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if not (i==0 and j==0 and k ==0):
                    neighbors.append((time, z + i, x+j, y+k))
    return neighbors

def one_cycle(states: dict) -> dict:
    current_time = max(states, key=lambda x: x[0])[0]
    states_copy = dict()
    for state in states:
        if state[0] == current_time:
            states_copy[state] = states[state]
    for state in states_copy:
        neighbors = get_neighbors(state)
        for n in neighbors:
            neighbors_active = get_neighbors_active(n, states)
            if n in states and states[n] == "#":
                if neighbors_active in [2, 3]:
                    states[(current_time + 1, n[1], n[2], n[3])] = "#"
            else:
                if neighbors_active == 3:
                    states[(current_time + 1, n[1], n[2], n[3])] = "#"
    return states

states = generate_intial(REAL)
for _ in range(7):
    states = one_cycle(states)

print(len([state for state in states if state[0] == 6]))
