import re
from collections import defaultdict


def manhattan_dist(loc1, loc2):
    x1, y1 = loc1
    x2, y2 = loc2
    return abs(x2 - x1) + abs(y2 - y1)


with open("Day6Input.txt", "r") as f:
    content = f.read().splitlines()


coords = [(int(x), int(y)) for x, y in [re.search(r'(\d+), (\d+)', line).groups() for line in content]]

coords.sort(key=lambda a: a[0])
min_x = coords[0][0]
max_x = coords[-1][0]
coords.sort(key=lambda a: a[1])
min_y = coords[0][1]
max_y = coords[-1][1]

# mapping of every marked coord and the locations that are closest to it
territory_dict = defaultdict(list)
# mapping of each location and the sum of the manhattan distances to every marked coord
global_distance_dict = dict()

for x in range(min_x, max_x):
    for y in range(min_y, max_y):
        loc = (x, y)
        # sort each marked coordinate and its manhattan distance from loc by manhattan dist
        distance_sorted_coords = sorted([(a, manhattan_dist(a, loc)) for a in coords], key=lambda n: n[1])
        # make sure there are not multiple shortest manhattan distances
        if distance_sorted_coords[0][1] != distance_sorted_coords[1][1]:
            closest_coord, distance = distance_sorted_coords[0]
            territory_dict[closest_coord].append(loc)
        global_distance_dict[loc] = sum([i[1] for i in distance_sorted_coords])

largest_area_coord = sorted([t for t in territory_dict.keys()], key=lambda t: len(territory_dict[t]))[-1]
print(f"Part 1: {len(territory_dict[largest_area_coord])}")
