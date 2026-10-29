"""Word loading and selection utilities for Hangman."""

from __future__ import annotations

import random
from pathlib import Path


VALID_DIFFICULTIES = ("easy", "medium", "hard")


class WordManager:
    """Load and select words from difficulty-specific text files."""

    def __init__(self, words_dir: str | Path | None = None):
        base_dir = Path(words_dir) if words_dir is not None else Path(__file__).resolve().parent / "words"
        self.words_dir = Path(base_dir)
        self.words_by_difficulty = {
            difficulty: self._load_words(difficulty)
            for difficulty in VALID_DIFFICULTIES
        }

    def _load_words(self, difficulty: str) -> list[str]:
        if difficulty not in VALID_DIFFICULTIES:
            raise ValueError(f"Invalid difficulty: {difficulty!r}.")

        path = self.words_dir / f"{difficulty}.txt"
        if not path.exists():
            raise FileNotFoundError(f"Word list not found for difficulty '{difficulty}': {path}")

        words: list[str] = []
        seen: set[str] = set()

        for line in path.read_text(encoding="utf-8").splitlines():
            word = line.strip().lower()
            if not word:
                continue
            if not word.isalpha():
                raise ValueError(f"Word list contains a non-alphabetic word: {word!r} in {path}")
            if word not in seen:
                seen.add(word)
                words.append(word)

        if not words:
            raise ValueError(f"No valid words found in {path}")

        return words

    def get_words(self, difficulty: str) -> list[str]:
        if difficulty not in VALID_DIFFICULTIES:
            raise ValueError(f"Invalid difficulty: {difficulty!r}.")
        return list(self.words_by_difficulty[difficulty])

    def choose_word(self, difficulty: str) -> str:
        words = self.get_words(difficulty)
        return random.choice(words)
