# Helper functions go here:
import random

# Clean search name to use on the betika site:


def clean_search_input(string) -> str:
    """
    Info: The Betika site has the following limitations regarding team names searched:
        - It only returns results for the accurately spelt names.
        - No word under 4 characters really returns accurate results.
        - Mostly shortens team names with more than one word (If both names are longer
        than 4 characters each, they shorten the longest and use the other).
        - Strings like 'U20', 'U23' are unacceptable
    Implemented solution:
        - First check the name of the first team:
            - if it has no spaces and is longer than four characters, use it.
            - if it has a space, get the longest word of those present, and these
            longest words must be longer than 3 characters and shorter than 10 
            characters, else just use the next word.
        - If none of those work, do the same check for the second name.
        - However, the name with the least number of spaces is one that is more likely to get
        the expected results.
        - Randomly pick any three letter word available at that instance and take chances on it, lol.
    """

    str_arr = string.split(" vs ")
    first_name = str_arr[0]
    second_name = str_arr[1]

    some_exceptions = ["SOUTH", "NORTH", "WEST", "EAST", "YOUTH"]

    # check first name:
    if not " " in first_name and len(first_name) > 3:
        return first_name

    # working with the name with least number of spaces:
    first_name_spaces = first_name.count(" ")
    second_name_spaces = second_name.count(" ")

    if " " in first_name and first_name_spaces < second_name_spaces:
        # for cases such as "SOUTH KOREA U23"
        for name in some_exceptions:
            if name in first_name.split(" "):
                return f"{first_name.split(' ')[0]} {first_name.split(' ')[1]}"

        longest_word = max(first_name.split(" "), key=len)
        len_longest = len(longest_word)
        if len_longest >= 4 and len_longest <= 9:
            return longest_word

    # Check second name
    if not " " in second_name and len(second_name) > 3:
        return second_name

    if " " in second_name and second_name_spaces < first_name_spaces:
        longest_word = max(second_name.split(" "), key=len)
        if len(longest_word) >= 4:
            return longest_word

    # Worst case scenario eg --> "FC OSS vs FC AIK"
    random_idx = random.randint(0, 1)
    return max(str_arr[random_idx].split(" "), key=len)


# Further event verification helper:
def verify(entry, term_searched, teams) -> bool:
    """
    INFO: This function checks if besides the search term selected,
    the other team's name is also in the current event being checked.
    """
    team_1 = teams[0].upper()
    team_2 = teams[1].upper()
    # case where both team names are just one word entries
    if not " " in team_1 and " " not in team_2:
        if term_searched == team_1:
            if team_2 in entry["teams"]:
                return True
        elif term_searched == team_2:
            if team_1 in entry["teams"]:
                return True

    # case where only one of the team names is a one word entry
    if " " in team_1 and not " " in team_2:
        if term_searched in team_1:
            if team_2 in entry["teams"]:
                return True
        elif term_searched == team_2:
            for name in list(team_1.split(" ")):
                if name in entry["teams"]:
                    return True
    elif " " in team_2 and not " " in team_1:
        if term_searched in team_2:
            if team_1 in entry["teams"]:
                return True
        elif term_searched == team_1:
            for name in list(team_2.split(" ")):
                if name in entry["teams"]:
                    return True

    # case where both team names are more than a word entry.
    if " " in team_1 and " " in team_2:
        if term_searched in team_1:
            for name in list(team_2.split(" ")):
                if name in entry["teams"]:
                    return True
        elif term_searched in team_2:
            for name in list(team_1.split(" ")):
                if name in entry["teams"]:
                    return True

    # if all the above cases dont match:
    return False
