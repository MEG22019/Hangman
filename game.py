"""Core Hangman game engine."""

from __future__ import annotations


class HangmanGame:
    """Represent a single Hangman game."""

    def __init__(self, word: str, max_incorrect_guesses: int = 6, difficulty: str = "medium"):
        if not isinstance(word, str):
            raise ValueError("Word must be a string.")

        normalized_word = word.strip().lower()
        if not normalized_word or not normalized_word.isalpha():
            raise ValueError("Word must contain only alphabetic characters.")

        if max_incorrect_guesses <= 0:
            raise ValueError("Maximum incorrect guesses must be positive.")

        self._word = normalized_word
        self.difficulty = difficulty.strip().lower() if isinstance(difficulty, str) else "medium"
        self.max_incorrect_guesses = max_incorrect_guesses
        self.guessed_letters = set()
        self.incorrect_letters = set()
        self.status = "playing"

    def _normalize_guess(self, letter: str) -> str:
        if not isinstance(letter, str):
            raise ValueError("Guess must be a single letter.")

        normalized = letter.strip().lower()
        if len(normalized) != 1 or not normalized.isalpha():
            raise ValueError("Guess must be a single alphabetic character.")

        return normalized

    def _has_won(self) -> bool:
        return all(ch in self.guessed_letters for ch in set(self._word))

    def masked_word(self) -> str:
        return " ".join(ch if ch in self.guessed_letters else "_" for ch in self._word)

    def remaining_guesses(self) -> int:
        return self.max_incorrect_guesses - len(self.incorrect_letters)

    def guess(self, letter: str) -> dict:
        if self.status != "playing":
            raise RuntimeError("Game has already ended; cannot guess again.")

        normalized = self._normalize_guess(letter)
        if normalized in self.guessed_letters:
            raise ValueError(f"Letter '{normalized}' has already been guessed.")

        self.guessed_letters.add(normalized)

        if normalized in self._word:
            if self._has_won():
                self.status = "won"
        else:
            self.incorrect_letters.add(normalized)
            if len(self.incorrect_letters) >= self.max_incorrect_guesses:
                self.status = "lost"

        return self.get_state()

    def get_state(self) -> dict:
        state = {
            "pattern": self.masked_word(),
            "guessed_letters": sorted(self.guessed_letters),
            "incorrect_letters": sorted(self.incorrect_letters),
            "remaining_guesses": self.remaining_guesses(),
            "status": self.status,
        }

        if self.status in {"won", "lost"}:
            state["word"] = self._word

        return state

    @property
    def word(self) -> str:
        return self._word
