import re


class claim: 
    def __init__(self, claim_string):
        self.claim = claim_string
        match = re.match(r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$", claim_string)
        self.claim_no = int(match.groups()[0])
        self.from_left = int(match.groups()[1])
        self.from_top = int(match.groups()[2])
        self.width = int(match.groups()[3])
        self.height = int(match.groups()[4])
        self.used_coords = set()
        self.__set_used_coords()

    def __set_used_coords(self):
        for row in range(self.from_left, self.from_left + self.width): 
            for col in range(self.from_top, self.from_top + self.height):
                self.used_coords.add((row,col)) 

    def __repr__(self):
        return f"{self.claim}"


def main():
    with open("Day3Input.txt", "r") as f:
        content = [i.replace("\n", "") for i in f.readlines()]

    claims = list()
    for line in content:
        claims.append(claim(line))


    used_inches = dict()
    for i in claims: 
        for coord in i.used_coords: 
            if used_inches.get(coord) is None: 
                used_inches[coord] = [i] 
            else: 
                used_inches[coord].append(i) 

    total_overlapped_inches = 0 
    for key in used_inches.keys(): 
        if len(used_inches[key]) > 1: 
            total_overlapped_inches += 1

    print(total_overlapped_inches)


if __name__ == "__main__":
    main()
