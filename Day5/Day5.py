import re
import string


def main():
    with open("Day5In.txt", "r") as f:
        content = f.readline().replace("\n", "")

    test_input = "dabAcCaCBAcCcaDA"
    alt_test_input = "rwVVvTt"

    polymer_sets = {i: 0 for i in string.ascii_lowercase}
    for polymer_unit in polymer_sets.keys():
        polymer_string = re.sub(polymer_unit, "", content, flags=re.IGNORECASE)
        matches_found = True
        print(f"removing all {polymer_unit}'s, length without that character: {len(polymer_string)}")
        # print(string)
        # If the start position of the first match is in this list that match should be ignored
        total_matched_pairs = 0
        while matches_found:
            matches = [i for i in re.finditer(r"([A-Za-z])\1+", polymer_string, flags=re.IGNORECASE)]
            ignored_matches = 0
            for match in matches:

                print(f"Match found: {match[0]}")
                alternation_validation = re.search(r"([A-Za-z])(?!\1)([A-Za-z])(?:\1\2)*\1?", match[0])
                if alternation_validation is not None:

                    true_start = match.start() + alternation_validation.start()
                    true_end = true_start + 2

                    polymer_string = f"{polymer_string[:true_start]}{polymer_string[true_end:]}"
                    print(f"Length of String: {len(polymer_string)}")
                    print("")
                    total_matched_pairs += 1
                    break
                else:
                    ignored_matches += 1
                    print(f"Match skipped: {match[0]}")
                    print(f"Total Matches skipped: {ignored_matches}")
                print("\n")
            if len(matches) == ignored_matches:
                # end cond
                matches_found = False
                continue

        print("Remaining String:")
        print(f"{polymer_string}\n")
        print(f"Final Length: {len(polymer_string)}")
        polymer_sets[polymer_unit] = len(polymer_string)

    smallest_polymers_key = ""
    smallest_polymer = len(content)
    for key in polymer_sets.keys():
        if polymer_sets[key] < smallest_polymer:
            smallest_polymers_key = key
            smallest_polymer = polymer_sets[key]
    print(f"Smallest Polymer: {smallest_polymers_key}: {smallest_polymer}")


if __name__ == "__main__":
    main()

