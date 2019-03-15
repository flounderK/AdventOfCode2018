with open("AdventOfCodeDay2Input.txt", "r") as f: 
    content = [i.replace("\n","") for i in f.readlines()]

storage = dict() 
for index in range(0, len(content[0])):
    storage[index] = dict()
    for line in content:
        key = f"{line[:index]}{line[index+1:]}"
        if storage[index].get(key) is None:
            storage[index][key] = [line]
        else:
            storage[index][key].append(line)

for position_key in storage.keys(): 
    for key in storage[position_key].keys(): 
        if len(storage[position_key][key]) == 2:
            print(key) 


