import re

with open("Day10In.txt", "r") as f:
    content = [i.replace("\n", "") for i in f.readlines()]


class Beacon:

    MIN_X = 999999
    MAX_X = -999999
    MIN_Y = 999999
    MAX_Y = -999999

    def __init__(self, x, y, delta_x, delta_y):
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.dx = delta_x
        self.dy = delta_y
        self.check_for_bounds()

    def __repr__(self):
        return f"({self.x}, {self.y})  ({self.dx}, {self.dy})"

    def check_for_bounds(self):
        if self.x < Beacon.MIN_X:
            Beacon.MIN_X = self.x

        if self.y < Beacon.MIN_Y:
            Beacon.MIN_Y = self.y

        if self.x > Beacon.MAX_X:
            Beacon.MAX_X = self.x

        if self.y > Beacon.MAX_Y:
            Beacon.MAX_Y = self.y

    def tick(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.check_for_bounds()

    @classmethod
    def reset_bounds(cls):
        cls.MIN_X = 999999
        cls.MAX_X = -999999
        cls.MIN_Y = 999999
        cls.MAX_Y = -999999


def get_message_array(beacons, x_range, y_range):
    x_min, x_max = x_range
    y_min, y_max = y_range

    positions = list()
    for beacon in beacons:
        positions.append((beacon.x, beacon.y))
    columns = list()
    for y in range(y_min, y_max + 1):
        row = list()
        for x in range(x_min, x_max + 1):
            # pos_found = False
            if (x, y) in positions:
                row.append("#")
            else:
                row.append(".")
        columns.append(row)

    return columns


beacons = list()

for i in content:
    match = re.match(r"position=<(?: +)*(-*\d+),(?: +)*(-*\d+)> velocity=<(?: +)*(-*\d+),(?: +)*(-*\d+)>", i)
    if match is not None:
        x, y, dx, dy = match.groups()
        beacons.append(Beacon(int(x), int(y), int(dx), int(dy)))

smallest_x_spread = 999999
smallest_y_spread = 999999
smallest_spread_second = 0
elapsed_time = 0
while elapsed_time < 15000:
    """for r in get_message_array(beacons, (Beacon.MIN_X, Beacon.MAX_X), (Beacon.MIN_Y, Beacon.MAX_Y)):
        print("".join([c for c in r]))
    """
    spread_x = Beacon.MAX_X - Beacon.MIN_X
    spread_y = Beacon.MAX_Y - Beacon.MIN_Y
    if spread_x <= smallest_x_spread and spread_y <= smallest_y_spread:
        smallest_x_spread = spread_x
        smallest_y_spread = spread_y
        smallest_spread_second = elapsed_time

    Beacon.reset_bounds()
    for beacon in beacons:
        beacon.tick()

    elapsed_time += 1


print(f"{smallest_spread_second}, x:{smallest_x_spread}, y: {smallest_y_spread}")

for beacon in beacons:
    beacon.x = beacon.initial_x
    beacon.y = beacon.initial_y

for i in range(0, smallest_spread_second):
    for beacon in beacons:
        beacon.tick()

Beacon.reset_bounds()
for beacon in beacons:
    beacon.check_for_bounds()

positions = list()
for beacon in beacons:
    positions.append((beacon.x, beacon.y))

for y in range(Beacon.MIN_Y, Beacon.MAX_Y + 1):
    row = list()
    for x in range(Beacon.MIN_X, Beacon.MAX_X + 1):
        # pos_found = False
        if (x, y) in positions:
            print("#", end="")
        else:
            print(".", end="")
    print("\n", end="")

