
import random
from words import WORDS, HINTS
from stats import SessionStats


DIFFICULTIES = {
    "easy": {"lives": 8, "bonus": 3},
    "medium": {"lives": 6, "bonus": 5},
    "hard": {"lives": 4, "bonus": 8},
}


class HangmanGame:
    def __init__(self):
        self.score = 0
        self.streak = 0
        self.category = "technology"
        self.difficulty = "medium"
        self.secret = ""
        self.guessed = set()
        self.wrong = set()
        self.lives = 6
        self.hint_used = False
        self.stats = SessionStats()

    def start_round(self):
        self.secret = random.choice(WORDS[self.category]).lower()
        self.guessed.clear()
        self.wrong.clear()
        self.difficulty = self.difficulty.lower()
        self.lives = DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False

    def masked(self):
        return " ".join(
            ch if ch in self.guessed else "_"
            for ch in self.secret
        )

    def won(self):
        return all(ch in self.guessed for ch in set(self.secret))

    def guess(self, letter):
        letter = letter.strip().lower()

        if len(letter) != 1 or not letter.isalpha():
            return "Enter one letter."

        if letter in self.guessed or letter in self.wrong:
            return "Already guessed."

        if letter in self.secret:
            self.guessed.add(letter)
            return "Correct."

        self.wrong.add(letter)
        self.lives -= 1
        return "Wrong."

    def use_hint(self):
        if self.hint_used:
            return "Hint already used."

        hint = HINTS.get(self.secret)
        if not hint:
            return "No hint available for this word."

        self.hint_used = True
        self.score = max(0, self.score - 1)
        return hint

    def play_round(self):
        self.start_round()

        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print("Wrong:", " ".join(sorted(self.wrong)) or "-")
            print(
                "Lives:", self.lives,
                "Score:", self.score,
                "Streak:", self.streak,
                "Difficulty:", self.difficulty.title()
            )

            raw = input("Letter, /hint, or /quit: ").strip().lower()

            if raw == "/quit":
                return False

            if raw == "/hint":
                print(self.use_hint())
                continue

            print(self.guess(raw))

        if self.won():
            self.streak += 1
            self.score += DIFFICULTIES[self.difficulty]["bonus"] + self.streak
            self.stats.record_round(True, self.streak)
            print("Solved:", self.secret)
            return True

        self.streak = 0
        self.stats.record_round(False, self.streak)
        print("Out of lives. The word was:", self.secret)
        return True

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")

        while True:
            print("\nCategories:", ", ".join(WORDS))
            category = input("Choose category or q: ").strip().lower()

            if category == "q":
                break

            if category not in WORDS:
                print("Unknown category. Choose a listed category.")
                continue

            print("\nDifficulty: easy, medium, hard")
            difficulty = input("Choose difficulty: ").strip().lower()

            if difficulty not in DIFFICULTIES:
                print("Unknown difficulty. Choose easy, medium, or hard.")
                continue

            self.category = category
            self.difficulty = difficulty

            if not self.play_round():
                break

            print("\nSession statistics:")
            print("Rounds played:", self.stats.rounds_played)
            print("Rounds won:", self.stats.rounds_won)
            print("Best streak:", self.stats.best_streak)

            again = input("Another round? [y/n]: ").strip().lower()

            if again == "n":
                break

            if again != "y":
                print("Invalid choice. Ending session.")
                break

        print("\nFinal score:", self.score)
        print("Rounds played:", self.stats.rounds_played)
        print("Rounds won:", self.stats.rounds_won)
        print("Best streak:", self.stats.best_streak)
