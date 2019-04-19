import re


class Marble:

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return str(self.number)


class Player:
    def __init__(self, number):
        self.number = number
        self.points = 0

    def __repr__(self):
        return str(f"Player {self.number}, Points: {self.points}")


with open("Day9In.txt", "r") as f:
    content = f.readline()

match = re.match(r"(\d+) players; last marble is worth (\d+) points", content)
if match is None:
    print("Non-matching input")
    exit(1)

number_of_players, last_marble_point_value = match.groups()

marbles = [Marble(0)]
current_marble_position = 0
marble_count = 1
players = list()

for i in range(1, number_of_players + 1):
    players.append(Player(i))

for player in players:
    new_marble = Marble(marble_count)

    if marble_count % 23 == 0:
        player.points += 23
        # 7 marbles counter clockwise, remove and add to score
    elif len(marbles) == 1 or current_marble_position == (len(marbles) - 2):
        marbles.append(new_marble)
        current_marble_position = len(marbles) - 1
    elif len(marbles) == 2 or current_marble_position == (len(marbles) - 1):
        marbles.insert(1, new_marble)
        current_marble_position = 1
    else:
        marbles.insert(current_marble_position + 2, new_marble)
        current_marble_position = current_marble_position + 2

    marble_count += 1

