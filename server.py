"""Flask API for the Hangman game."""

from __future__ import annotations

from uuid import uuid4

from flask import Flask, jsonify, request

from game import HangmanGame
from word_manager import VALID_DIFFICULTIES, WordManager


def create_app(word_manager: WordManager | None = None) -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    manager = word_manager or WordManager()
    games: dict[str, HangmanGame] = {}

    @app.route("/api/games", methods=["POST"])
    def create_game():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        difficulty = str(payload.get("difficulty", "")).strip().lower()
        if difficulty not in VALID_DIFFICULTIES:
            return jsonify({"error": "Invalid difficulty. Choose easy, medium, or hard."}), 400

        word = manager.choose_word(difficulty)
        game = HangmanGame(word=word, difficulty=difficulty)
        game_id = uuid4().hex
        games[game_id] = game

        response = {
            "game_id": game_id,
            "pattern": game.get_state()["pattern"],
            "remaining_guesses": game.get_state()["remaining_guesses"],
            "status": game.get_state()["status"],
        }
        return jsonify(response), 201

    @app.route("/api/games/<game_id>", methods=["GET"])
    def get_game(game_id: str):
        game = games.get(game_id)
        if game is None:
            return jsonify({"error": "Game not found."}), 404

        return jsonify(game.get_state()), 200

    @app.route("/api/games/<game_id>/guess", methods=["POST"])
    def make_guess(game_id: str):
        game = games.get(game_id)
        if game is None:
            return jsonify({"error": "Game not found."}), 404

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        letter = payload.get("letter")
        if letter is None:
            return jsonify({"error": "Guess must include a 'letter' field."}), 400

        try:
            state = game.guess(letter)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        except RuntimeError as exc:
            return jsonify({"error": str(exc)}), 409

        return jsonify(state), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
