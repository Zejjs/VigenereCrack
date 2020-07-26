import vigenere
from languageFunctions import check_for_spaces


def main():
    print("Welcome to Final Vigenere Crack Mk 2")
    print("Let's crack some Vigenere\n")

    # Attempting to open file containing the cipher text
    try:
        file = open("ciphertext.txt", "r")
        ciphertext = file.read()
        file.close()
    except FileNotFoundError:
        print("Error: ciphertext.txt not found. Make sure the file exists in the program directory and try again.")
        return

    # First crack - program asks the user for a key. If the key is known, the file is deciphered
    while True:
        key = input("Input the key followed by Enter. If key is unknown leave the key blank and press Enter\nKEY: ")
        if key.isalpha() or key == "":
            break
        else:
            print("Key can only contain letters, please try again.\n")

    print()

    # First crack - use the key provided by the user to decipher the file. Program then allows to save the plaintext
    # or to try again with a different key.
    if key != "":
        while True:
            plaintext = vigenere.decipher_vigenere(ciphertext, key)
            print("Deciphering the cipher text with key: {}.\nPlaintext:\n".format(key.upper()))
            print(plaintext)
            r = input("\nInput 'save' if you'd like to save the plaintext, 'again' if you'd like to try a different "
                      "key. Otherwise press 'Enter' to quit\nINPUT: ")

            if r.lower() == "save" or r.lower() == 's':
                file = open("plaintext.txt", "w")
                file.write(plaintext)
                file.close()
                print("\nPlaintext saved to 'plaintext.txt. Closing session.")
                return

            elif r.lower() == "again" or r.lower() == 'a':
                key = input("\nInput the key followed by Enter. "
                            "If key is unknown leave the key blank and press Enter\nKEY: ")
                print()
                continue

            elif r == "":
                print("\nClosing session.")
                return

            else:
                print("\nInput not recognized. Please try again.\n")

    # Second crack - attempting a dictionary attack. Asks the user whether they want to try a dictionary attack
    spaces = check_for_spaces(ciphertext)
    try_dict = input("Would you like to try a dictionary attack? Input 'yes' or 'y' to confirm. Input anything "
                     "else to continue\nINPUT:")
    if try_dict.lower() == "yes" or try_dict.lower() == "y":
        print("\nAttempting dictionary attack...\n")
        key, plaintext = vigenere.dictionary_attack(ciphertext, spaces)

        if plaintext:
            while True:
                r = input(
                    "\nInput 'save' if you'd like to save the plaintext, otherwise press 'Enter' to quit\nINPUT: ")
                if r.lower() == "save" or r.lower() == 's':
                    file = open("plaintext.txt", "w")
                    file.write(plaintext)
                    file.close()
                    print("\nPlaintext saved to 'plaintext.txt. Closing session.")
                    return
                elif r == "":
                    print("\nClosing session.")
                    return
                else:
                    print("\nInput not recognized. Please try again.\n")

    # Third crack - if dictionary attack failed, or the user chose not to do one, the program performs
    # a Kasinski/Babbage attack
    print("\nAttempting Kasinski/Babbage attack.\n")
    spaces = check_for_spaces(ciphertext)
    possible_key_lengths = vigenere.find_likely_key_lengths(ciphertext, 6)
    possible_keys = []

    for key_length in possible_key_lengths:
        possible_keys.extend(vigenere.find_possible_keys(ciphertext, key_length))

    key, plaintext = vigenere.brute_force_with_list(ciphertext, possible_keys, spaces)

    if plaintext:
        while True:
            r = input(
                "\nInput 'save' if you'd like to save the plaintext, otherwise press 'Enter' to quit\nINPUT: ")
            if r.lower() == "save" or r.lower() == 's':
                file = open("plaintext.txt", "w")
                file.write(plaintext)
                file.close()
                print("\nPlaintext saved to 'plaintext.txt. Closing session.")
                return
            elif r == "":
                print("\nClosing session.")
                return
            else:
                print("\nInput not recognized. Please try again.\n")


if __name__ == "__main__":
    main()
