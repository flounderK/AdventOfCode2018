
class Cart:
    def __init__(self, x, y, initial_representation):
        self.x = x
        self.y = y
        self.current_location = (x, y)
        self.next_location  = None
        self.on_intersection = False
        self.on_turn = False
        self.last_turn_symbol = ""
        self.current_representation = initial_representation
        self.next_direction_change = "left"
        self.directions = {"left": {"<": "v", "v": ">", ">": "^", "^": "<"},
                           "straight": {"<": "<", "v": "v", ">": ">", "^": "^"},
                           "right": {"<": "^", "v": "<", ">": "v", "^": ">"}}
        self.turn_dictionary = {"/": {"<": "v", "^": ">", ">": "^", "v": "<"},
                                "\\": {"v": ">", "<": "^", "^": "<", ">": "v"}}

    def turn(self, rail_symbol):
        if rail_symbol == "+":
            self.on_intersection = True
            self.intersection_turn()
        else:
            self.on_turn = True
            self.last_turn_symbol = rail_symbol
            self.current_representation = self.turn_dictionary[rail_symbol][self.current_representation]

    def intersection_turn(self):
        self.current_representation = self.directions[self.next_direction_change][self.current_representation]
        if self.next_direction_change == "left":
            self.next_direction_change = "straight"
        elif self.next_direction_change == "straight":
            self.next_direction_change = "right"
        elif self.next_direction_change == "right":
            self.next_direction_change = "left"

    def get_next_location(self):
        if self.current_representation == "^":
            return self.x, self.y -1
        if self.current_representation == "v":
            return self.x, self.y + 1
        if self.current_representation == "<":
            return self.x - 1, self.y
        if self.current_representation == ">":
            return self.x + 1, self.y

    def set_next_location(self, x, y):
        self.next_location = (x, y)

    def move(self):
        self.x, self.y = self.next_location
        self.current_location = (self.x, self.y)


class Railways:
    def __init__(self, map):
        self.map = map
        self.carts = list()
        self.rail_grid = list()
        self.process_map()
        self.crashes = list()

    def find_cart(self, x, y):
        for cart in self.carts:
            if cart.x == x and cart.y == y:
                return cart
        return None

    def process_map(self):
        lines = self.map.splitlines()
        for y in range(0, len(lines)):
            self.rail_grid.append(list())
            for x in range(0, len(lines[y])):
                character = lines[y][x]
                self.rail_grid[y].append(character)
                if character in ["^", "v", ">", "<"]:
                    self.carts.append(Cart(x, y, character))

    def find_collisions(self):
        location_count = dict()
        for cart in self.carts:
            if location_count.get(cart.current_location) is None:
                location_count[cart.current_location] = 1
            else:
                location_count[cart.current_location] += 1
        for location in list(location_count.keys()):
            if location_count[location] >= 2:
                x, y = location
                self.rail_grid[y][x] = "X"
                self.crashes.append(location)
                return

    def tick(self):
        for y in range(0, len(self.rail_grid)):
            for x in range(0, len(self.rail_grid[y])):
                rail_symbol = self.rail_grid[y][x]
                if rail_symbol in ["^", "v", ">", "<"]:
                    cart = self.find_cart(x, y)
                    if cart is None:
                        break
                    next_x, next_y = cart.get_next_location()
                    # check for glags to replace grid symbol
                    if cart.on_intersection is False and cart.on_turn is False:
                        if cart.current_representation in [">", "<"]:
                            self.rail_grid[y][x] = "-"
                        if cart.current_representation in ["^", "v"]:
                            self.rail_grid[y][x] = "|"
                    if cart.on_intersection is True:
                        self.rail_grid[y][x] = "+"
                        cart.on_intersection = False
                    if cart.on_turn is True:
                        self.rail_grid[y][x] = cart.last_turn_symbol
                        cart.on_turn = False
                    cart.set_next_location(next_x, next_y)
                    next_symbol = self.rail_grid[next_y][next_x]
                    if next_symbol in ["+", "/", "\\"]:
                        cart.turn(next_symbol)
        # get next movement locations and move to them
        for cart in sorted(self.carts, key=lambda n: n.y):
            cart.move()
            next_x, next_y = cart.next_location
            self.rail_grid[next_y][next_x] = cart.current_representation
        # update railway grid with nex cart locations
        for cart in self.carts:
            x, y = cart.current_location
            self.rail_grid[y][x] = cart.current_representation
        self.find_collisions()

    def print_railway(self):
        for y in self.rail_grid:
            print("".join(y))


if __name__ == "__main__":
    with open("Day13In.txt", "r") as f:
        content = f.read()
    railway = Railways(content)
    railway.print_railway()
    while len(railway.crashes) < 1:
        railway.tick()
        railway.print_railway()
    print(f"Part 1: {railway.crashes}")


