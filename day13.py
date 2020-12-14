TEST = """939
7,13,x,x,59,x,31,19"""


def read_input(raw: str) -> tuple:
    sp = raw.split("\n")
    arrive = sp[0]
    buses = sp[1]
    arrive = int(arrive)
    buses = [bus for bus in buses.split(",")]
    return (arrive, buses)


def ans1(arr_buses: tuple) -> int:
    arrive = arr_buses[0]
    buses = arr_buses[1]
    buses = [int(bus) for bus in buses if bus != "x"]
    min_wait = max(buses) + 1
    for bus in buses:
        if bus - (arrive % bus) < min_wait:
            min_bus = bus
            min_wait = bus - (arrive % bus)
    return min_wait * min_bus


def ans2(arr_buses) -> int:
    buses = arr_buses[1]
    bus_dict = {}
    for i, bus in enumerate(buses):
        if bus != "x":
            if int(bus) != int(buses[0]):
                if i > int(bus):
                    bus_dict[int(bus)] = i % int(bus)
                else:
                    bus_dict[int(bus)] = i
    checking = int(buses[0])
    inc = int(buses[0])
    for bus in bus_dict:
        while (checking + bus_dict[bus]) % bus != 0:
            checking += inc
        inc = inc * bus
    return checking


assert ans1(read_input(TEST)) == 295
assert ans2(read_input("123\n5,7,19")) == 55
assert ans2(read_input(TEST)) == 1068781

with open("day13input") as f:
    raw = f.read()
    print(ans1(read_input(raw)))
    print(ans2(read_input(raw)))
