import string


def english_frequency_score(text):
    """
    Function takes a string and analyses the frequency of the characters within,
    compares the frequency with that of English language,
    and returns a score describing similarity to English

    Args:
        text: string of text to analyse

    Returns:
        int: score ranging between 0 and 12, the higher the closer the character
            distribution in the string to English
    """

    freq_score = 0
    # Six most and least common characters in the English language
    most_common = "ETAOIN"
    least_common = "VKJXQZ"
    freq_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

    uppercase = string.ascii_uppercase

    # Prepare a dictionary to store character counts
    letter_count_dict = {}
    for letter in uppercase:
        letter_count_dict[letter] = 0

    # Count the characters in text and update the dictionary
    for letter in text:
        if letter.upper() in uppercase:
            letter_count_dict[letter.upper()] += 1

    # list_of_freqs is a list of tuples consisting of letter and its count pairs
    # list is used here to enable sorting of the data
    list_of_freqs = []
    for key in letter_count_dict:
        list_of_freqs.append((key, letter_count_dict[key]))

    # sorting the list of tuples by letter count
    list_of_freqs.sort(key=lambda t: t[1], reverse=True)

    # creates a letter_frequency_string in which all characters are ordered by how frequently they appear in text
    # in case of ties ordered by reverse ETAOIN order
    letter_frequency_string = []
    current_freq = -1
    current_string = []
    for tup in list_of_freqs:
        if tup[1] == current_freq:
            current_string.append(tup[0])
        else:
            current_freq = tup[1]
            if len(current_string) > 0:
                s = "".join(sorted(current_string, key=lambda w: [freq_order.index(c) for c in w], reverse=True))
                letter_frequency_string.append(s)
                current_string.clear()
            current_string.append(tup[0])

    s = "".join(sorted(current_string, key=lambda w: [freq_order.index(c) for c in w], reverse=True))
    letter_frequency_string.append(s)
    letter_frequency_string = "".join(letter_frequency_string)

    # check the overlap between six most common characters in the text and in English
    # award points based on overlap
    for letter in letter_frequency_string[:6]:
        if letter in most_common:
            freq_score += 1

    # check the overlap between six least common characters in the text and in English
    # award points based on overlap
    for letter in letter_frequency_string[-6:]:
        if letter in least_common:
            freq_score += 1

    # return the English frequency score
    return freq_score
