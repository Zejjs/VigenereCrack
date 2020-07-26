import string


def check_for_spaces(text):
    """
    Utility function ussed for checking whether text contains spaces.

    Args:
        text: a string to be checked for whether it contains spaces

    Returns:
        bool: True if text has spaces, False if not
    """
    for char in text:
        if char == " ":
            return True

    return False


def load_words():
    """
    Function opens the dictionary.txt file,
    stores its contents in a dictionary
    and returns it.
    Uses a dictionary for speed of access.

    Returns:
        dict: dictionary containing all words in dictionary.txt
    """
    dict_file = open("dictionary.txt")
    dictionary = {}

    for word in dict_file.read().split():
        dictionary[word] = None
    dict_file.close()

    return dictionary


ENGLISH_DICTIONARY = load_words()


def format_for_analysis(text, keep_spaces=True):
    """
    Function takes a string, turns it uppercase,
    and removes all non-letter, non-space characters

    Args:
        text: a string to be formatted
        keep_spaces: bool defaulting to True, if set to False function also removes spaces

    Returns:
        string: uppercase string consisting of uppercase letters and by default spaces

    """
    text = text.upper()
    uppercase_and_space = string.ascii_uppercase + " "

    formatted_text = []

    for character in text:
        if keep_spaces and character in uppercase_and_space:
            formatted_text.append(character)
        elif not keep_spaces and character in string.ascii_uppercase:
            formatted_text.append(character)

    return "".join(formatted_text).strip()


def is_english(text, spaces=True):
    """
    Function takes a string and checks whether it's in English.
    Returns True if more than a certain threshold of words in the string are English.

    Args:
        text: string of text
        spaces: indicates whether the string has spaces or not, defaults to True

    Returns:
         bool: in case of spaced text True if >= 33% of words the string are in English, False otherwise
               in case of unspaced text the threshold is 70%
    """

    # Spaces the text
    if not spaces:
        text = find_words_in_nospace(text)

    english_count = 0

    # Turns the string uppercase, removes non-letters, and splits it into a list
    words_list = format_for_analysis(text).split()

    # Counts the English words
    for word in words_list:
        if word in ENGLISH_DICTIONARY:
            english_count += 1

    # Calculates the percentage of English words in the string
    if len(words_list) > 0:
        english_percent = english_count / len(words_list) * 100
    else:
        english_percent = 0

    if english_percent >= 33 and spaces:
        return True
    # Threshold is higher for nonspaced strings because of single letter false positives
    elif english_percent >= 70 and not spaces:
        return True
    else:
        return False


def find_words_in_nospace(text):
    """
    Function takes a nonspaced English string and returns a spaced string.

    Args:
        text: a string of nonspaces text

    Returns:
        string: a spaced string
    """

    text = format_for_analysis(text)
    text_length = len(text)
    words_list = []
    not_a_word_string = ""

    current_start_index = 0
    longest_word_length = 13

    # Outer loop continues until the start index reaches the end of the text
    while current_start_index < text_length:

        # Inner loop provides the end index of the string slice
        # It starts at the length of the longest word in the dictionary, and goes down from there
        for word_length in reversed(range(longest_word_length)):

            word_candidate = text[current_start_index:min(current_start_index + word_length, text_length)]

            # if the current slice is in the dictionary it's added to the list of words, and the start index is updated
            if word_candidate in ENGLISH_DICTIONARY:
                current_start_index += min(word_length, text_length)
                # before we add the word to the list we clear the not_a_word_string buffer of non-English words
                if not_a_word_string != "":
                    words_list.append(not_a_word_string)
                    not_a_word_string = ""
                words_list.append(word_candidate)
                break

            # If we ended up with a candidate of length one that's not in the dictionary,
            # we add it to the not_a_word_string buffer and increment the start index
            elif len(word_candidate) == 1:
                not_a_word_string += word_candidate
                current_start_index += 1
                break

    return " ".join(words_list)
