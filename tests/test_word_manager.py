import pytest

from word_manager import WordManager


class TestWordManager:
    def test_loads_word_lists_for_all_difficulties(self):
        manager = WordManager()

        assert set(manager.words_by_difficulty) == {"easy", "medium", "hard"}
        assert len(manager.get_words("easy")) > 0
        assert len(manager.get_words("medium")) > 0
        assert len(manager.get_words("hard")) > 0

    def test_choose_word_returns_word_from_requested_difficulty(self):
        manager = WordManager()

        for difficulty in ["easy", "medium", "hard"]:
            chosen = manager.choose_word(difficulty)
            assert chosen in manager.get_words(difficulty)
            assert chosen.isalpha()

    def test_invalid_difficulty_raises_value_error(self):
        manager = WordManager()

        with pytest.raises(ValueError, match="Invalid difficulty"):
            manager.choose_word("expert")

    def test_invalid_word_file_raises_error(self, tmp_path):
        bad_words_dir = tmp_path / "words"
        bad_words_dir.mkdir()
        (bad_words_dir / "easy.txt").write_text("cat\n123\n", encoding="utf-8")
        (bad_words_dir / "medium.txt").write_text("dog\n", encoding="utf-8")
        (bad_words_dir / "hard.txt").write_text("sun\n", encoding="utf-8")

        with pytest.raises(ValueError, match="non-alphabetic"):
            WordManager(bad_words_dir)
