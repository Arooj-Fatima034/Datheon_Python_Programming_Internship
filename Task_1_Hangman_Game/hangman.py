import random
import os

MAX_MISTAKES = 6

STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========""",
]


def load_words():
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "words.txt")
    words = []
    try:
        with open(path, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word.isalpha() and len(word) >= 5:
                    words.append(word)
    except FileNotFoundError:
        print("words.txt not found, using default words.")
    if not words:
        words = ["python", "gallows", "keyboard", "program", "computer",
                 "variable", "function", "internet", "science", "database"]
    return words


def get_history_path():
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, "history.txt")


def save_result(word, result, mistakes):
    with open(get_history_path(), "a") as file:
        file.write(word + "," + result + "," + str(mistakes) + "\n")


def show_stats():
    wins = 0
    losses = 0
    try:
        with open(get_history_path(), "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    if parts[1] == "win":
                        wins += 1
                    elif parts[1] == "loss":
                        losses += 1
    except FileNotFoundError:
        pass
    print("Your record -> Wins:", wins, "| Losses:", losses)


def show_word(word, guessed):
    result = ""
    for letter in word:
        if letter in guessed:
            result += letter.upper() + " "
        else:
            result += "_ "
    return result.strip()


def get_guess(guessed, wrong):
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (A-Z).")
        elif guess in guessed or guess in wrong:
            print("You already guessed '" + guess.upper() + "'. Try another letter.")
        else:
            return guess


def play(word):
    guessed = set()
    wrong = set()

    while True:
        print(STAGES[len(wrong)])
        print()
        print("Word:", show_word(word, guessed))
        print("Wrong guesses:", ", ".join(sorted(l.upper() for l in wrong)) or "none")
        print("Attempts left:", MAX_MISTAKES - len(wrong))
        print()

        guess = get_guess(guessed, wrong)

        if guess in word:
            guessed.add(guess)
            print("Good guess!")
        else:
            wrong.add(guess)
            print("Wrong guess!")

        if all(letter in guessed for letter in word):
            print(STAGES[len(wrong)])
            print()
            print("=" * 30)
            print("   YOU WIN! :)")
            print("   The word was:", word.upper())
            print("=" * 30)
            save_result(word, "win", len(wrong))
            return

        if len(wrong) == MAX_MISTAKES:
            print(STAGES[len(wrong)])
            print()
            print("=" * 30)
            print("   GAME OVER :(")
            print("   The word was:", word.upper())
            print("=" * 30)
            save_result(word, "loss", len(wrong))
            return


def main():
    words = load_words()
    print("=" * 30)
    print("      HANGMAN GAME")
    print("=" * 30)
    show_stats()

    while True:
        word = random.choice(words)
        play(word)
        show_stats()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


main()
