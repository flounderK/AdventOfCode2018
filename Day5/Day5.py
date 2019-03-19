import re

with open("Day5In.txt", "r") as f:
    content = f.readline().replace("\n", "")

test_input = "dabAcCaCBAcCcaDA"
matches_found = True
string = content
print(string)
cached_str = ""
swapped_letters = list()
# If the start position of the first match is in this list that match should be ignored
ignored_matches = 0
while matches_found:
    matches = [i for i in re.finditer(r"([A-Za-z])\1", string, flags=re.IGNORECASE)]
    try:
        match = matches[ignored_matches]
    except IndexError:
        matches_found = False
        continue
        
    if match is None:
        # end cond
        matches_found = False
        continue

    print(f"Match found: {match[0]}")
    alternation_validation = re.search(r"([A-Za-z])(?!\1)([A-Za-z])(?:\1\2)*\1?", match[0])
    if alternation_validation is None:
        ignored_matches += 1
        """
        cached_str = string[:match.end()]
        string = string[match.end():]
        string_to_change = cached_str[match.start():match.end()]
        length = len(string_to_change)
        replacement = "#"*length
        cached_str = f"{cached_str[:match.start()]}{replacement}{cached_str[match.end():]}"
        string = cached_str + string
        """
        print(f"Match skipped: {match[0]}")
        print(f"Total Matches skipped: {ignored_matches}")
        print("")
        continue

    true_start = match.start() + alternation_validation.start()
    true_end = match.end() - alternation_validation.start()

    string = f"{string[:true_start]}{string[true_end:]}"
    print(f"Length of String: {len(string)}")
    print("")

print("Remaining String:")
print(f"{string}\n")
print(f"Final Length: {len(string)}")
