import re


class Player:
    def __init__(self, number):
        self.number = number
        self.points = 0
        self.won_marbles = list()

    def __repr__(self):
        return str(f"Player {self.number}, Points: {self.points}")


with open("Day9In.txt", "r") as f:
    content = f.readline()

match = re.match(r"(\d+) players; last marble is worth (\d+) points", content)
if match is None:
    print("Non-matching input")
    exit(1)

# number_of_players, last_marble_point_value = int(match.groups()[0]), int(match.groups()[1])
number_of_players, last_marble_point_value = 10, 1618

marbles = [0]
current_marble_position = 0
marble_count = 1
players = list()

for i in range(1, number_of_players + 1):
    players.append(Player(i))

last_marble_placed = False

while not last_marble_placed:
    for player in players:
        new_marble = marble_count

        if marble_count % 23 == 0:
            player.points += marble_count
            offset_index = -7
            if current_marble_position < 7:
                offset_index = offset_index - 1

            marble_to_remove = marbles[current_marble_position + offset_index]

            player.points += marble_to_remove
            marbles.remove(marble_to_remove)
            current_marble_position = marbles.index(marbles[current_marble_position + offset_index])
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

        if marble_count == last_marble_point_value:
            last_marble_placed = True
            break

        # print(f"[{marble_count}] " + "  ".join([str(i) if i != marble_count else str(f"({i})") for i in marbles]))
        marble_count += 1


players.sort(key=lambda x: x.points, reverse=True)

print(f"Winner: {players[0]}")

