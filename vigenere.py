import string
import languageFunctions
from frequencyFinder import english_frequency_score
from myMath import factors


def decipher_vigenere(cipher_text, key):
    """
    Function deciphers a standard Vigenere encrypted cipher text using a key

    Args:
        cipher_text: string to be deciphered
        key: string containing the key

    Returns:
         string: deciphered cipher text
    """
    cipher_text = languageFunctions.format_for_analysis(cipher_text)
    key = key.upper()
    plaintext = []
    key_index = 0
    key_length = len(key)
    alphabet_length = len(string.ascii_uppercase)

    for index in range(len(cipher_text)):
        if cipher_text[index] == " ":
            plaintext.append(" ")
        else:
            cipher_value = string.ascii_uppercase.index(cipher_text[index])

            key_value = string.ascii_uppercase.index(key[key_index % key_length])
            key_index += 1

            index_plaintext = (cipher_value - key_value) % alphabet_length

            plaintext.append(string.ascii_uppercase[index_plaintext])

    return "".join(plaintext)


def dictionary_attack(cipher_text, spaces=True):
    """
    Function performs a dictionary attack on the cipher text.

    Args:
        cipher_text: string of text to be deciphered
        spaces: bool saying whether the text contains spaces, defaults to True

    Returns:
        tuple containing the key and the plaintext
        returns None, None if deciphering failed
    """
    # Load the text and list of keys from the dictionary created by languageFunctions.py
    cipher_text = languageFunctions.format_for_analysis(cipher_text)
    key_list = list(languageFunctions.ENGLISH_DICTIONARY.keys())

    # A dictionary attack takes a while, so the program tracks how deep into the dictionary it got so far
    displayed_percent = 0

    for key in key_list:
        # Display how many % of the dictionary have we went through
        curr_percent = int(key_list.index(key) / len(key_list) * 100)
        if curr_percent > displayed_percent:
            displayed_percent = curr_percent
            print("Tried {:02}% of the words in the dictionary".format(displayed_percent))

        # Try to decipher the text with a word from the dictionary
        plaintext = decipher_vigenere(cipher_text, key)

        # Check whether the resulting text is English and ask user for final confirmation whether deciphering is done
        if languageFunctions.is_english(plaintext, spaces):
            print("\nKey candidate: " + key)
            print("Plaintext candidate:\n" + languageFunctions.find_words_in_nospace(plaintext))
            while True:
                response = input("\nPress C to continue looking for a key, or Enter to confirm the key choice: ")
                if response == "":
                    return key, plaintext
                if response.lower() == "c":
                    print("Looking for a new key...\n")
                    break

    # Return a tuple of Nones if the attack fails
    print("Failed to find a key using dictionary attack.")
    return None, None


def find_likely_key_lengths(cipher_text, how_many=6):
    """
    Function takes a string of cipher text, performs Kasiski examination to find likely key lengths
    and returns them as a list

    Args:
        cipher_text: string of text to be analysed
        how_many: int defining how many most likely keys should be returned, defaults to 6

    Returns:
         list: a list of integers denoting likely key lengths
    """
    # Remove spaces and nonalpha chars from the text
    text = languageFunctions.format_for_analysis(cipher_text, False)

    # A dictionary that stores indexes of three to five character sequences appearing in the text
    seq_dict = {}

    # loops through character sequences of length 3, 4 and 5, and stores them in the dictionary.
    # uses the sequences as keys, and indexes of sequences as values
    for seq_length in range(3, 6):
        for i in range(len(text) - seq_length + 1):
            sequence = text[i:i + seq_length]
            if sequence in seq_dict:
                seq_dict[sequence].append(i)
            else:
                seq_dict[sequence] = [i]

    spacing_set = set()

    # goes through all the sequences in the seq_dict, removes those that only appear once,
    # then adds the spacings between the remainder to the spacing_set
    for key in seq_dict:
        if len(seq_dict[key]) == 1:
            continue
        for i in range(len(seq_dict[key]) - 1):
            for j in range(i + 1, len(seq_dict[key])):
                spacing_set.add(seq_dict[key][j] - seq_dict[key][i])

    factor_count_dict = {}

    # for each spacing in the spacing set the function takes it's factors and stores them in the factor_count_dict
    # the keys in the dictionary are the factors, the values are the counts. Most numerous factors are most likely to be
    # the key length
    # function discards factors of 1
    for spacing in spacing_set:
        for factor in factors(spacing):
            if factor == 1:
                continue
            if factor in factor_count_dict:
                factor_count_dict[factor] += 1
            else:
                factor_count_dict[factor] = 1

    likely_key_lengths = []

    # create a list of tuples, where each tuple is a factor and its count
    for key in factor_count_dict:
        likely_key_lengths.append((key, factor_count_dict[key]))

    # sort the list by count in descending order
    likely_key_lengths.sort(key=lambda t: t[1], reverse=True)

    # strip the counts from the tuples, turning the list of tuples into a list of ints, sorted by count
    for i in range(min(how_many, len(likely_key_lengths))):
        likely_key_lengths[i] = likely_key_lengths[i][0]

    # returns a list of n most likely lengths of the key, n equal to how_many, defaults to 6
    return likely_key_lengths[:min(how_many, len(likely_key_lengths))]


def get_every_nth_letter(cipher_text, n):
    """
    Function returns a list of n strings, each created by taking every nth letter.
    For example:
        get_every_nth_letter("ABCDEFGHI", 3)
    would output:
        ["ADG", "BEH", "CFI")

    Args:
        cipher_text: string of text to be divided into substrings
        n: number of strings to output

    Returns:
         list: a list with n elements, each a string made by taking every nth character
    """
    text = languageFunctions.format_for_analysis(cipher_text, False)
    list_of_strings = []

    i = 0
    while i < n:
        list_of_strings.append([])
        i += 1

    # Function uses lists and later joins them into strings for speed
    for i in range(len(text)):
        list_of_strings[i % n].append(text[i])

    for i in range(len(list_of_strings)):
        list_of_strings[i] = "".join(list_of_strings[i])

    return list_of_strings


def produce_permutations(list_of_key_lists):
    """
    A recursive function that takes a list of lists of characters, and creates all possible combinations of words
    using them, and outputs them in a string. For example:
        produce_permutations([['A', 'B', 'C'], ['D'], ['E', 'F']])
    would output:
        ["ADE", "ADF", "BDE", "BDF", "CDE", "CDF"]

    Args:
        list_of_key_lists: a list of lists, each inner list holds all the possible characters to be used at a given
        position in the

    Returns:
         A list of strings, each composed of characters from sublists in the list provided as argument
    """
    # base case: if length of list is 1, return the list
    if len(list_of_key_lists) == 1:
        return list_of_key_lists[0]
    # if the list is longer than 1, take characters from first sublist, and append the function's call to itself,
    # omitting the first sublist
    else:
        key_list = []
        for char_a in list_of_key_lists[0]:
            for char_b in produce_permutations(list_of_key_lists[1:]):
                key_list.append(char_a + char_b)
        return key_list


def find_possible_keys(cipher_text, key_length):
    """
    Function slices the cipher text into substrings equal to length of key, and then treats each substring as a standard
    Caesar cipher.
    Each Caesar cipher is brute forced with every letter of the alphabet, then the character frequency distribution
    in each brute force attempt is analysed and compared with English distribution. The keys that lead to
    "most English" distributions are returned in a list

    Args:
        cipher_text: string of text to be deciphered
        key_length: int, length of key with which the cipher text is encoded

    Returns:
        list: a list of strings, each a potential key that leads to an English-like distribution of letters.
    """

    text = languageFunctions.format_for_analysis(cipher_text, False)
    substring_list = get_every_nth_letter(text, key_length)
    alphabet = string.ascii_uppercase

    list_of_key_lists = []

    for i in range(key_length):

        key_list = list()
        highest_match_score = 0
        substring = substring_list[i]

        for letter in alphabet:
            freq_score = english_frequency_score(decipher_vigenere(substring, letter))
            if freq_score > highest_match_score:
                highest_match_score = freq_score
                key_list.clear()
                key_list.append(letter)
            elif freq_score == highest_match_score:
                key_list.append(letter)
        list_of_key_lists.append(key_list)

    list_of_keys = produce_permutations(list_of_key_lists)

    return list_of_keys


def brute_force_with_list(cipher_text, list_of_keys, spaces=True):
    """
    Function takes a cipher text and a list of keys, then tries each key until a solution in English is found.

    Args:
        cipher_text: string, the text to be deciphered
        list_of_keys: a list of strings, where each string is a key to be tried
        spaces: optional bool, denotes whether cipher_text has spaces. Defaults to True.

    Returns:
        tuple: a tuple of two strings, the first one being the key, second one the plaintext.
            returns a tuple of Nones if no solution is found.
    """
    text = languageFunctions.format_for_analysis(cipher_text)
    key_list = list_of_keys

    for key in key_list:
        plaintext = decipher_vigenere(text, key)

        if languageFunctions.is_english(plaintext, spaces):
            print("Key candidate: " + key)
            print("Plaintext candidate:\n" + languageFunctions.find_words_in_nospace(plaintext))
            while True:
                response = input("\nPress C to continue looking for a key, or Enter to confirm the key choice: ")
                if response == "":
                    return key, plaintext
                if response.lower() == "c":
                    print("Looking for a new key...\n")
                    break

    print("Failed to find a key using frequency analysis.")
    return None, None
