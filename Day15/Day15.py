from abc import ABC, abstractmethod
from collections import defaultdict
import operator
import itertools


class Character(ABC):
    registry = set()

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.targets = set()
        self.target = None
        self.in_range_squares = list()
        self.register()
        self.associated_game = None

    def register_associated_game(self, game):
        self.associated_game = game

    def move(self, location):
        pass

    def attack(self):
        pass

    def find_path_to_adjacent_location(self, x, y):
        """Method to be used to locate a reachable path that will put character in an adjacent
        location to the one specified"""
        target_locations = self.get_valid_adjacent_locations(x, y)
        location = (self.x, self.y)
        path_options = list()
        path = [location]
        adjacency_tree = dict()
        fin = False
        pop_and_cont = False
        while fin is not True:
            pop_and_cont = False
            current_lookup_val = "".join(path.__repr__())
            if adjacency_tree.get(current_lookup_val) is None:
                adjacency_tree[current_lookup_val] = self.get_valid_adjacent_locations(*location)
                for path_loc in path:
                    if path_loc in adjacency_tree[current_lookup_val]:
                        adjacency_tree[current_lookup_val].remove(path_loc)
            valid_adjacent_locations = adjacency_tree[current_lookup_val]
            if len(path) == 1 and len(valid_adjacent_locations) < 1:
                # end turn, no more moves
                fin = True
                continue

            if len(valid_adjacent_locations) < 1:
                # no more moves, back out one and continue
                pop_and_cont = True

            if location in target_locations:
                # success, add path to return value
                path_options.append(path.copy())
                pop_and_cont = True

            if len(path_options) >= 1 and len(path) > len(sorted(path_options, key=lambda a: len(a))[0]):
                # prune off paths that are larger than the shortest path
                pop_and_cont = True

            if pop_and_cont is True:
                last_loc = location
                path.pop()
                last_lookup_val = "".join(path.__repr__())
                location = path[-1]
                adjacency_tree[last_lookup_val].remove(last_loc)
                continue

            location = valid_adjacent_locations[0]
            path.append(location)
            # print("\n".join(["".join(y) for y in self.associated_game.get_current_grid(path)]))
        path_options.sort(key=lambda a: len(a))
        return [i for i in path_options if len(i) <= len(path_options[0])]

    def get_valid_adjacent_locations(self, x, y):
        return [i for i in self.__class__.get_adjacent_locations(x, y) if self.is_empty_location(i) is True]

    def find_targets(self):
        return self.__class__.get_enemies()

    @staticmethod
    def get_adjacent_locations(x, y):
        """return all locations that are adjacent to the one specified"""
        return [(x + o, y + n) for o, n in
                [i for b in itertools.permutations([(0, 0), (-1, 1)]) for i in zip(*b)]]

    def is_empty_location(self, location):
        if location in [i.get_location() for i in self.__class__.get_all_subclass_instances()]:
            return False
        if location in self.associated_game.data["floor"]:
            return True
        else:
            return False

    def choose_target(self):
        potential_targets = self.find_targets()
        self.__class__.prioritize(potential_targets)
        adjacent_targets = [t for t in potential_targets if self.target_is_adjacent(t.x, t.y) is True]
        if len(adjacent_targets) > 0:
            target = adjacent_targets[0]
            return target.x, target.y
        target = potential_targets[0]
        return target.x, target.y

    def target_is_adjacent(self, x, y):
        if (x, y) in self.get_adjacent_locations(*self.get_location()):
            return True
        else:
            return False

    def take_turn(self):
        target_location = self.choose_target()
        if self.target_is_adjacent(*target_location) is True:
            self.attack()
        else:
            self.move(target_location)

    def __init_subclass__(cls, **kwargs):
        if cls not in cls.registry:
            cls.registry.add(cls)
        super().__init_subclass__(**kwargs)

    @classmethod
    def get_all_subclass_instances(cls):
        return [item for sublist in [i.CHARACTERS for i in [c for c in cls.registry]]
                for item in sublist]

    @staticmethod
    def prioritize(chars):
        """organize in reading order"""
        chars.sort(key=operator.attrgetter("y", "x"))

    def get_location(self):
        return self.x, self.y

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def deregister(self):
        pass

    @classmethod
    @abstractmethod
    def get_enemies(cls):
        all_characters = set([i for s in [c.CHARACTERS for c in cls.__base__.registry] for i in s])
        this_chars = set(cls.CHARACTERS)
        return list(all_characters - this_chars)


class Elf(Character):
    CHARACTERS = list()

    def register(self):
        self.__class__.CHARACTERS.append(self)

    def deregister(self):
        self.__class__.CHARACTERS.remove(self)

    @classmethod
    def get_enemies(cls):
        return super().get_enemies()

    def __repr__(self):
        return "E"


class Goblin(Character):
    CHARACTERS = list()

    def register(self):
        self.__class__.CHARACTERS.append(self)

    def deregister(self):
        self.__class__.CHARACTERS.remove(self)

    @classmethod
    def get_enemies(cls):
        return super().get_enemies()

    def __repr__(self):
        return "G"


def new_character(symbol, x, y):
    char_type = type
    if symbol == "G":
        char_type = Goblin
    if symbol == "E":
        char_type = Elf
    return char_type(x, y)


def manhattan_distance(l1, l2):
    return abs(abs(l1[0] - l2[0]) + abs(l1[1] - l2[1]))


class Game(object):
    def __init__(self, grid):
        self.data = defaultdict(list)
        self.empty_grid = self.initial_grid_parse(grid)

    def initial_grid_parse(self, grid):
        empty_grid = list()
        for y, row in enumerate(grid):
            empty_grid.append(list())
            for x, char in enumerate(row):
                loc = (x, y)
                if char == "#":
                    self.data["walls"].append(loc)
                    empty_grid[y].append(char)
                elif char == ".":
                    self.data["floor"].append(loc)
                    empty_grid[y].append(char)
                else:
                    new_char = new_character(char, x, y)
                    new_char.register_associated_game(self)
                    self.data["floor"].append((x, y))
                    empty_grid[y].append(".")
        return empty_grid

    def get_current_grid(self, path=None):
        grid = self.empty_grid.copy()
        # grid = ["".join(grid[y]) for y in grid]
        if path is not None:
            for x, y in path:
                grid[y] = "".join(grid[y])
                grid[y] = grid[y][:x] + "+" + grid[y][x + 1:]

        for char in Character.get_all_subclass_instances():
            x, y = char.get_location()
            grid[y] = "".join(grid[y])
            grid[y] = grid[y][:x] + char.__repr__() + grid[y][x + 1:]
        return grid

    @staticmethod
    def determine_rount_order():
        """Who makes a move and when"""
        all_characters = Character.get_all_subclass_instances()
        Character.prioritize(all_characters)
        return all_characters

    def __repr__(self):
        return "\n".join(["".join(y) for y in self.get_current_grid()])


if __name__ == "__main__":
    with open("Day15InPathfindingTest.txt", "r") as f:
        content = f.read().splitlines()
    game = Game(content)

    e = Elf.CHARACTERS[0]
    g = Goblin.CHARACTERS[0]
    

