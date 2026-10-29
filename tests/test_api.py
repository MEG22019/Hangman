import pytest

from server import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_create_game_returns_game_id_and_safe_state(client):
    response = client.post("/api/games", json={"difficulty": "easy"})

    assert response.status_code == 201
    payload = response.get_json()
    assert "game_id" in payload
    assert payload["status"] == "playing"
    assert payload["remaining_guesses"] == 6
    assert "word" not in payload
    assert payload["pattern"]


def test_create_game_rejects_invalid_difficulty(client):
    response = client.post("/api/games", json={"difficulty": "insane"})

    assert response.status_code == 400
    assert "Invalid difficulty" in response.get_json()["error"]


def test_get_game_returns_current_state(client):
    create_response = client.post("/api/games", json={"difficulty": "medium"})
    game_id = create_response.get_json()["game_id"]

    response = client.get(f"/api/games/{game_id}")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "playing"
    assert payload["remaining_guesses"] == 6
    assert "word" not in payload


def test_get_unknown_game_returns_404(client):
    response = client.get("/api/games/not-real-id")

    assert response.status_code == 404
    assert "Game not found" in response.get_json()["error"]


def test_guess_updates_state_and_keeps_word_hidden(client):
    create_response = client.post("/api/games", json={"difficulty": "easy"})
    game_id = create_response.get_json()["game_id"]

    response = client.post(f"/api/games/{game_id}/guess", json={"letter": "a"})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] in {"playing", "won", "lost"}
    assert "word" not in payload
    assert "a" in payload["guessed_letters"] or payload["incorrect_letters"]


def test_guess_rejects_invalid_payloads(client):
    create_response = client.post("/api/games", json={"difficulty": "easy"})
    game_id = create_response.get_json()["game_id"]

    response = client.post(f"/api/games/{game_id}/guess", json={"letter": "ab"})
    assert response.status_code == 400

    response = client.post(f"/api/games/{game_id}/guess", json={})
    assert response.status_code == 400


def test_guess_rejects_after_game_ends(client):
    create_response = client.post("/api/games", json={"difficulty": "easy"})
    game_id = create_response.get_json()["game_id"]

    # Force a lost game by guessing incorrectly six times.
    for letter in ["x", "y", "z", "q", "m", "n"]:
        client.post(f"/api/games/{game_id}/guess", json={"letter": letter})

    response = client.post(f"/api/games/{game_id}/guess", json={"letter": "a"})

    assert response.status_code == 409
    assert "ended" in response.get_json()["error"].lower()


def test_game_reveals_word_only_after_game_ends(client):
    # Use a deterministic word by creating a custom app with a controlled WordManager.
    class FixedWordManager:
        def choose_word(self, difficulty):
            return "cat"

    app = create_app(FixedWordManager())
    app.config["TESTING"] = True
    with app.test_client() as fixed_client:
        create_response = fixed_client.post("/api/games", json={"difficulty": "easy"})
        game_id = create_response.get_json()["game_id"]

        playing_state = fixed_client.get(f"/api/games/{game_id}").get_json()
        assert "word" not in playing_state

        for letter in ["x", "y", "z", "q", "m", "n"]:
            fixed_client.post(f"/api/games/{game_id}/guess", json={"letter": letter})

        final_state = fixed_client.get(f"/api/games/{game_id}").get_json()
        assert final_state["status"] == "lost"
        assert final_state["word"] == "cat"


def test_each_difficulty_creates_game_successfully(client):
    for difficulty in ["easy", "medium", "hard"]:
        response = client.post("/api/games", json={"difficulty": difficulty})
        assert response.status_code == 201
        payload = response.get_json()
        assert payload["status"] == "playing"
        assert payload["remaining_guesses"] == 6


def test_correct_and_incorrect_guesses_update_state(client):
    response = client.post("/api/games", json={"difficulty": "easy"})
    game_id = response.get_json()["game_id"]

    correct = client.post(f"/api/games/{game_id}/guess", json={"letter": "a"})
    payload = correct.get_json()
    assert correct.status_code == 200
    assert payload["status"] in {"playing", "won"}
    assert "a" in payload["guessed_letters"]

    incorrect = client.post(f"/api/games/{game_id}/guess", json={"letter": "x"})
    payload = incorrect.get_json()
    assert incorrect.status_code == 200
    assert payload["status"] in {"playing", "won", "lost"}
    assert "x" in payload["incorrect_letters"]
    assert payload["remaining_guesses"] == 5


def test_invalid_json_and_missing_body_are_rejected(client):
    response = client.post("/api/games", data="not-json", content_type="application/json")
    assert response.status_code == 400

    create_response = client.post("/api/games", json={"difficulty": "easy"})
    game_id = create_response.get_json()["game_id"]

    response = client.post(f"/api/games/{game_id}/guess", data="[]", content_type="application/json")
    assert response.status_code == 400


def test_game_can_be_restarted_after_ending_previous_one(client):
    create_response = client.post("/api/games", json={"difficulty": "easy"})
    first_game_id = create_response.get_json()["game_id"]

    for letter in ["x", "y", "z", "q", "m", "n"]:
        client.post(f"/api/games/{first_game_id}/guess", json={"letter": letter})

    second_response = client.post("/api/games", json={"difficulty": "medium"})
    assert second_response.status_code == 201
    second_payload = second_response.get_json()
    assert second_payload["status"] == "playing"
    assert second_payload["remaining_guesses"] == 6
    assert second_payload["game_id"] != first_game_id
