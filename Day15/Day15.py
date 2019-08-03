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
        self.hit_points = 200
        self.attack_power = 3

    def register_associated_game(self, game):
        self.associated_game = game

    def move(self, location):
        """Move to location, Error if specified location is not adjacent"""
        assert self.target_is_adjacent(*location)
        self.x, self.y = location

    def attack(self, other):
        """attack the other character specified"""
        other.take_damage(self.attack_power)

    def take_damage(self, attack_power):
        self.hit_points -= attack_power
        if self.hit_points < 1:
            self._die()

    def _die(self):
        self.deregister()

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
        path_options = [i for i in path_options if len(i) <= len(path_options[0])]
        # TODO: prioritize paths iteratively
        return prioritize_path(path_options)

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
        prioritize_characters(potential_targets)
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
        """Keep a record of all of the subclass types"""
        if cls not in cls.registry:
            cls.registry.add(cls)
        super().__init_subclass__(**kwargs)

    @classmethod
    def get_all_subclass_instances(cls):
        return [item for sublist in [i.CHARACTERS for i in [c for c in cls.registry]]
                for item in sublist]

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


def prioritize_characters(chars):
    """organize in reading order"""
    chars.sort(key=operator.attrgetter("y", "x"))


def prioritize_path(paths: list):
    divergent_ind = None
    divergent_path_ind = None
    for ind, locs in enumerate(zip(*paths)):
        default_loc_for_ind = locs[0]
        for loc in locs:
            if loc != default_loc_for_ind:
                # find the first index where there are differing locations
                divergent_ind = ind
                break
        if divergent_ind is not None:
            # choose the first of the locations in reading order
            # vv this right here decides reading order, change if broken vv
            optimal_location_at_divergence = sorted(list(locs), key=lambda a: (a[1], a[0]))[0]
            number_of_remaining_paths = len([i for i in list(locs) if i == optimal_location_at_divergence])
            optimal_paths = [p for i, p in enumerate(paths) if paths[i][ind] == optimal_location_at_divergence]
            if number_of_remaining_paths == 1:
                return optimal_paths[0]
            else:
                # recursively call this function until only one path remains
                return prioritize_path(optimal_paths)


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
        """Get the Game's current grid state. Passing in a list of tuples (x, y)
        will print those out as well."""
        grid = self.empty_grid.copy()
        for y, row in enumerate(grid):
            grid[y] = "".join(grid[y])
        if path is not None:
            for x, y in path:
                grid[y] = "".join(grid[y])
                grid[y] = grid[y][:x] + "+" + grid[y][x + 1:]

        for char in Character.get_all_subclass_instances():
            x, y = char.get_location()
            grid[y] = "".join(grid[y])
            grid[y] = grid[y][:x] + char.__repr__() + grid[y][x + 1:]
        return grid

    def print_current_grid(self, path=None):
        print("\n".join(self.get_current_grid(path)))

    @staticmethod
    def determine_rount_order():
        """Who makes a move and when"""
        all_characters = Character.get_all_subclass_instances()
        prioritize_characters(all_characters)
        return all_characters

    def tick(self):
        round_order = self.determine_rount_order()
        for char in round_order:
            char.take_turn()

    def __repr__(self):
        return "\n".join(["".join(y) for y in self.get_current_grid()])


if __name__ == "__main__":
    with open("Day15In.txt", "r") as f:
        content = f.read().splitlines()
    game = Game(content)

    e = Elf.CHARACTERS[0]
    g = Goblin.CHARACTERS[1]




