import math


class FuelCell:
    def __init__(self, x, y, serial_number):
        self.x = x
        self.y = y
        self.serial_number = serial_number
        self.rack_id = self.x + 10
        self.power_level = self.rack_id * self.y
        self.power_level = self.power_level + self.serial_number
        self.power_level = self.power_level * self.rack_id
        if self.power_level < 100:
            # only keep 100's digit
            self.power_level = 0
        else:
            self.power_level = int(self.power_level / 100) - (int(self.power_level / 1000) * 10) - 5

    def __repr__(self):
        return f"Power: {self.power_level}, Rack Id: {self.rack_id}"


class FuelCellBlock:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.power_level_total = 0
        self.fuel_cells = list()
        for c in range(x, x + 3):
            for r in range(y, y + 3):
                cell = grid[c - 1][r - 1]
                self.power_level_total += cell.power_level

    def __repr__(self):
        return f"Power: {self.power_level_total} for Block {self.x}, {self.y}"


def print_block(x, y, grid):
    for r in range((y - 2), (y - 2) + 5):
        for c in range((x - 2), (x - 2) + 5):
            print(f"{grid[c][r].power_level} ", end="")
        print("")


grid = list()
serial_number = 9221
for x in range(0, 300):
    grid.append(list())
    for y in range(0, 300):
        grid[x].append(FuelCell(x + 1, y + 1, serial_number))

highest_power_level = 0
highest_power_level_block = None
for x in range(0, 297):
    for y in range(0, 297):
        block = FuelCellBlock(x + 1, y + 1, grid)
        if block.power_level_total > highest_power_level:
            highest_power_level = block.power_level_total
            highest_power_level_block = block

print(highest_power_level_block)
