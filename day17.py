import numpy as np

TEST = """
.#.
..#
###
"""


def ans1(raw: str) -> int:
    state = []
    for line in raw.split("\n"):
        if line:
            state.append([])
            for char in line:
                state[-1].append(char)
    state = np.array(state)
    states = {0: state}

    for i in range(6):
        new_states = {}
        x, y = states[0].shape
        for z, state in states.items():
            new_state = np.full((x + 2, y + 2), ".")
            new_state[1:-1, 1:-1] = state.copy()
            new_states[z] = new_state
        new_states[min(states.keys()) - 1] = np.full((x + 2, y + 2), ".")
        new_states[min(states.keys()) + 1] = np.full((x + 2, y + 2), ".")
        for z, state in states.items():
            for x in range(state.shape[0]):
                for y in range(state.shape[1]):
                    cur_state = state[x, y]
                    neighbors = 0
                    for i in range(-1, -3):
                        for j in range(-1, -3):
                            for k in range(-1, -3):
                                try:
                                    if states[z + k][x + i, y + j] == "#":
                                        neighbors += 1
                                except IndexError:
                                    print("indexerror")
                    if cur_state == "#":
                        if not neighbors in [2, 3]:
                            new_states[z][x + 1, y + 1] = "."
                    else:
                        if neighbors == 3:
                            new_states[z][x + 1, y + 1] = "#"
        states = new_states.copy()
        print(states)


print(ans1(TEST))
