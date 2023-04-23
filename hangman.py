###############################################################################################################
# Author: Gabriel Oliveira                                                                                    #
# Hangman                                                                                                     #
# Python v3.10                                                                                                #
###############################################################################################################
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    """
    print("Loading word list from file...")

    inFile = open(WORDLIST_FILENAME, 'r')

    line = inFile.readline()

    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    guessed_letters_counter = 0

    for letter in secret_word:
        if letter in letters_guessed:
            guessed_letters_counter = guessed_letters_counter + 1

    return len(secret_word) == guessed_letters_counter



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word_guessed = ""

    for letter in secret_word:
        char_to_fill = "_ "

        for letter_guessed in letters_guessed:
            if letter == letter_guessed:
                char_to_fill = letter

        word_guessed += char_to_fill

    return word_guessed



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    ascii_letters = string.ascii_lowercase
    available_letters = ""

    for index in range(len(ascii_letters)):
        letter = ascii_letters[index]

        if letter not in letters_guessed:
            available_letters += letter

    return available_letters


def get_unique_letters_from_word(word):
    '''
    word: string, regular English word
    returns: a list of characters that represents the unique letters from word
    '''
    unique_letters = []
    for letter in word:
        if letter not in unique_letters:
            unique_letters.append(letter)

    return unique_letters




def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    my_word_without_spaces = ""

    for char in my_word:
        my_word_without_spaces += char.strip()

    if len(my_word_without_spaces) != len(other_word):
        return False

    word_match = True

    for index in range(len(my_word_without_spaces)):
        if my_word_without_spaces[index] == "_":
            continue

        if my_word_without_spaces[index] != other_word[index]:
            word_match = False

    return word_match



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = ""

    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches += word + " "

    if len(matches) == 0:
        print("No matches found")
    else:
        print(matches)



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    - Game Rules:

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, should be displayed to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. **Make sure to check that the user guesses a letter**

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, should be displayed to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.
    '''
    print(secret_word)
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")

    max_guesses = 6
    guesses = 0
    letters_guessed = []

    max_warnings = 3
    warnings = 0

    print("You have", max_warnings, "warnings left.")
    print("-------------")
    while guesses <= max_guesses:
        print("You have", max_guesses - guesses, "guesses left.")
        print("Available letters: ", get_available_letters(letters_guessed))

        guess = input("Please guess a letter: ")

        if guess == "*":
            print("Possible word matches are:")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            print("------------")
            continue

        if str.isalpha(guess) is not True:
            if warnings >= max_warnings:
                guesses = guesses + 1
                if guesses >= max_guesses:
                    print("Sorry, you ran out of guesses. The word was", secret_word + ".")
                    break
            else:
                warnings = warnings + 1
                warnings_remaining = max_warnings - warnings
                print("Oops! That is not a valid letter. You have", warnings_remaining, "warnings left: ", get_guessed_word(secret_word, letters_guessed))

            continue

        guess = str.lower(guess)

        if guess in letters_guessed:
            if warnings >= max_warnings:
                guesses = guesses + 1
                if guesses >= max_guesses:
                    print("Sorry, you ran out of guesses. The word was", secret_word + ".")
                    break
            else:
                warnings = warnings + 1
                warnings_remaining = max_warnings - warnings
                print("Oops! You've already guessed that letter. You now have", warnings_remaining, "warnings: ", get_guessed_word(secret_word, letters_guessed))

            continue

        letters_guessed.append(guess)

        if is_word_guessed(secret_word, letters_guessed):
            guesses_remaining = max_guesses - guesses
            unique_letters_count = len(get_unique_letters_from_word(secret_word))

            total_score = guesses_remaining * unique_letters_count
            print("Congratulations, you won!")
            print("Your total score for this game is: ", total_score)
            break

        guessed_word = get_guessed_word(secret_word, letters_guessed)

        if guess not in secret_word:
            vowels = ['a', 'e', 'i', 'o', 'u']
            if guess in vowels:
                guesses = guesses + 2
            else:
                guesses = guesses + 1
            print("Oops! That letter is not in my word", guessed_word)
        else:
            print("Good guess:", guessed_word)

        if guesses >= max_guesses:
            print("Sorry, you ran out of guesses. The word was", secret_word + ".")
            break
        print("------------")

# -----------------------------------

if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
