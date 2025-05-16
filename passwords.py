# My addition to the assignment is to add unicode support. It's much, much harder to guess a
# password that may have characters from other languages in it. Many languages have a concept of
# cased letters, so we can still satisfy the basic requirements to check for upper and lower case
# letters. In practice, there are better ways to classify unicode password strength, but this will
# pass the test cases. 😀

import unicodedata


def is_lower(char):
    return unicodedata.category(char) == "Ll"


def is_upper(char):
    return unicodedata.category(char) == "Lu"


def is_digit(char):
    return unicodedata.category(char) == "Nd"


# For our purposes, special characters are punctuation and symbols.
def is_special(char):
    cat = unicodedata.category(char)
    return cat.startswith("P") or cat.startswith("S")


def word_in_file(word, filename, case_sensitive=False):
    with open(filename, "r", encoding="utf-8") as f:
        return any(
            word == stripped if case_sensitive else word.lower() == stripped.lower()
            for stripped in (line.strip() for line in f)
        )


def word_has_character(word, character_list):
    return any(character_list(char) for char in word)


def word_complexity(word):
    return sum(
        1
        for char_list in [is_lower, is_upper, is_digit, is_special]
        if word_has_character(word, char_list)
    )


# Note I didn't put the print statement in the function because that violates functional purity. If
# the calling code were to call this in a loop, it would spam the console. Instead, we return a
# tuple with the strength and the message and let the calling code print the message when
# appropriate.
def password_strength(password, min_length=10, strong_length=16):
    if word_in_file(password, "wordlist.txt", case_sensitive=False):
        return 0, "Password is a dictionary word and is not secure."
    if word_in_file(password, "toppasswords.txt", case_sensitive=True):
        return 0, "Password is a commonly used password and is not secure."
    if len(password) < min_length:
        return 1, "Password is too short and is not secure."
    if len(password) >= strong_length:
        return 5, "Password is long, length trumps complexity this is a good password."
    return word_complexity(password), None


def main():
    while True:
        password = input("Enter a password to check (or Q to quit): ")
        if password.lower() == "q":
            break
        strength, message = password_strength(password)
        print(f"Password strength: {strength}")
        if message:
            print(message)


if __name__ == "__main__":
    main()
