import pytest

from game import HangmanGame


class TestHangmanGame:
    def test_game_tracks_masked_word_and_guesses(self):
        game = HangmanGame("planet")
        state = game.get_state()

        assert state["pattern"] == "_ _ _ _ _ _"
        assert state["guessed_letters"] == []
        assert state["incorrect_letters"] == []
        assert state["remaining_guesses"] == 6
        assert state["status"] == "playing"
        assert "word" not in state

    def test_single_letter_guess_updates_pattern_and_incorrect_letters(self):
        game = HangmanGame("planet")
        result = game.guess("p")

        assert result["pattern"] == "p _ _ _ _ _"
        assert result["guessed_letters"] == ["p"]
        assert result["incorrect_letters"] == []
        assert result["remaining_guesses"] == 6

        result = game.guess("x")
        assert result["pattern"] == "p _ _ _ _ _"
        assert result["incorrect_letters"] == ["x"]
        assert result["remaining_guesses"] == 5

    def test_duplicate_guess_raises_error(self):
        game = HangmanGame("planet")
        game.guess("p")

        with pytest.raises(ValueError, match="already been guessed"):
            game.guess("P")

    def test_invalid_guess_raises_error(self):
        game = HangmanGame("planet")

        with pytest.raises(ValueError, match="single alphabetic character"):
            game.guess("ab")

        with pytest.raises(ValueError, match="single alphabetic character"):
            game.guess("1")

    def test_game_wins_when_all_letters_are_guessed(self):
        game = HangmanGame("cat")
        game.guess("c")
        game.guess("a")
        final = game.guess("t")

        assert final["status"] == "won"
        assert final["pattern"] == "c a t"
        assert final["word"] == "cat"

    def test_game_loses_after_six_wrong_guesses(self):
        game = HangmanGame("cat")
        for letter in ["x", "y", "z", "q", "m", "n"]:
            game.guess(letter)

        state = game.get_state()
        assert state["status"] == "lost"
        assert state["remaining_guesses"] == 0
        assert state["word"] == "cat"
        assert state["incorrect_letters"] == ["m", "n", "q", "x", "y", "z"]

    def test_game_rejects_guesses_after_end(self):
        game = HangmanGame("cat")
        for letter in ["x", "y", "z", "q", "m", "n"]:
            game.guess(letter)

        with pytest.raises(RuntimeError, match="already ended"):
            game.guess("a")

    def test_game_uses_lowercase_letter_normalization(self):
        game = HangmanGame("apple")
        result = game.guess("A")

        assert result["guessed_letters"] == ["a"]
        assert result["pattern"] == "a _ _ _ _"
