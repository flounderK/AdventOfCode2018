import re
from collections import deque


class Player:
    def __init__(self, number):
        self.number = number
        self.points = 0

    def __repr__(self):
        return str(f"Player {self.number}, Points: {self.points}")


def play(number_of_players, last_marble_point_value):
    marbles = deque([0])
    marble_count = 1
    players = [Player(i) for i in range(1, number_of_players + 1)]

    while marble_count < last_marble_point_value:
        for p in players:
            if marble_count % 23 == 0:
                p.points += marble_count
                marbles.rotate(7)
                p.points += marbles.pop()
                marbles.rotate(-1)
            else:
                marbles.rotate(-1)
                marbles.append(marble_count)

            marble_count += 1
            if marble_count > last_marble_point_value:
                break

    players.sort(key=lambda x: x.points)
    print(players[-1])


with open("Day9In.txt", "r") as f:
    content = f.readline()

match = re.match(r"(\d+) players; last marble is worth (\d+) points", content)
if match is None:
    print("Non-matching input")
    exit(1)

number_of_players, last_marble_point_value = int(match.groups()[0]), int(match.groups()[1])
print("Part 1:")
play(number_of_players, last_marble_point_value)
print("Part 2:")
play(number_of_players, last_marble_point_value * 100)
