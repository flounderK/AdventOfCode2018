import re


def main():
    with open("Day5In.txt", "r") as f:
        content = f.readline().replace("\n", "")

    test_input = "dabAcCaCBAcCcaDA"
    alt_test_input = "rwVVvTt"
    matches_found = True
    string = content
    print(string)
    # If the start position of the first match is in this list that match should be ignored
    total_matched_pairs = 0
    while matches_found:
        if total_matched_pairs == 36:
            j = 1
        matches = [i for i in re.finditer(r"([A-Za-z])\1+", string, flags=re.IGNORECASE)]
        ignored_matches = 0
        for match in matches:

            print(f"Match found: {match[0]}")
            alternation_validation = re.search(r"([A-Za-z])(?!\1)([A-Za-z])(?:\1\2)*\1?", match[0])
            if alternation_validation is not None:

                true_start = match.start() + alternation_validation.start()
                true_end = true_start + 2

                string = f"{string[:true_start]}{string[true_end:]}"
                print(f"Length of String: {len(string)}")
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
    print(f"{string}\n")
    print(f"Final Length: {len(string)}")


if __name__ == "__main__":
    main()

