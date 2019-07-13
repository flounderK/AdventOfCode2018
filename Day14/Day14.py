
recipes = [3, 7]
elf_1_ind = 0
elf_2_ind = 1


def print_recipes(elf_1_ind, elf_2_ind, recipes):
    for i, s in enumerate(recipes):
        if elf_1_ind == i:
            print(f" ({s})", end="")
        elif elf_2_ind == i:
            print(f" [{s}]", end="")
        else:
            print(f" {s}", end="")
    print("")


puzzle_in = 430971
part_2_search_len = len(str(puzzle_in)) + 2
finished = False
while not finished:
    current_sum = recipes[elf_1_ind] + recipes[elf_2_ind]
    recipes = recipes + [int(i) for i in list(str(current_sum))]
    elf_1_ind = (elf_1_ind + ((recipes[elf_1_ind] + 1) % len(recipes))) % len(recipes)
    elf_2_ind = (elf_2_ind + ((recipes[elf_2_ind] + 1) % len(recipes))) % len(recipes)
    if len(recipes) == puzzle_in + 10:
        print("Part 1: " + "".join([str(i) for i in recipes[puzzle_in:]]))

    if len(recipes) >= part_2_search_len:
        puzzle_in_ind = "".join([str(i) for i in recipes[-part_2_search_len:]]).find(str(puzzle_in))
        if puzzle_in_ind != -1:
            result = puzzle_in_ind - 1
            print(f"Part 2: {result}")
            finished = True
