import re


class PlantLine:
    def __init__(self, initial_state, patterns):
        self.initial_state = initial_state
        self.patterns = patterns
        self.line = [".", ".", "."]
        self.true_zero_index = len(self.line)
        self.line.extend([i for i in initial_state])
        self.line.extend([".", ".", "."])
        self.start_index = 2
        self.generation = 0
        self.plant_number_totals = 0

    def count_plant_number_totals(self):
        for plant_ind in range(0, len(self.line)):
            if self.line[plant_ind] == "#":
                self.plant_number_totals += (plant_ind - 3)

    def next_generation(self):
        next_generation = [".", "."]
        for center_pot_ind in range(self.start_index, len(self.line) - 2):
            plant_set = "".join(self.line[center_pot_ind - 2:center_pot_ind + 3])
            match_found = False
            for pattern in self.patterns.keys():
                if plant_set.find(pattern) != -1:
                    next_generation.append(self.patterns[pattern])
                    match_found = True
                    break
            if match_found is False:
                next_generation.append(".")
        next_generation.extend([".", ".", "."])
        self.generation += 1
        self.line = next_generation

    def __repr__(self):
        return "{0:2}: {1}".format(self.generation, "".join(self.line))


with open("Day12In.txt", "r") as f:
    content = [i.replace("\n", "") for i in f.readlines()]

initial_state_match = re.search("(?:initial state: )([#.]+)", content[0])
initial_state = initial_state_match.groups()[0]
content = content[1:]
pattern_matches = [re.search("([#.]{5})(?: => )([#.])", i) for i in content if i is not ""]
patterns = {i.groups()[0]: i.groups()[1] for i in pattern_matches}
plant_line = PlantLine(initial_state, patterns)

tens = 3
print(" "*8, end="")
for i in range(1, tens + 1):
    print(" "*9 + f"{i}", end="")
print("")
print(" "*7 + "0", end="")
for i in range(1, tens + 1):
    print(" "*9 + "0", end="")
print("")

print(plant_line)

for i in range(1, 21):
    plant_line.next_generation()
    print(plant_line)
plant_line.count_plant_number_totals()
print(f"Print part 1: {plant_line.plant_number_totals}")


