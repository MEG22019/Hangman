# Hangman Online

A lightweight Python Hangman game with a server-authoritative Flask API and a browser client. Players choose a difficulty (Easy, Medium, or Hard), guess letters, and the server tracks the game state while keeping the hidden word private until the game ends.

## Features

- Python game engine with separate difficulty word lists
- Flask REST API for game creation and letter guessing
- Browser-based Hangman UI using HTML, CSS, and vanilla JavaScript
- Automated tests for the game logic and API behavior
- Render-ready deployment configuration

## Requirements

- Python 3.10+
- pip

## Installation

1. Clone the repository.
2. Create and activate a virtual environment:

   python3 -m venv .venv
   source .venv/bin/activate

3. Install dependencies:

   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt

## Run the application locally

From the project root:

   source .venv/bin/activate
   python server.py

Then visit:

   http://127.0.0.1:5000/

## How to play in the browser

1. Open the app in a browser.
2. Choose Easy, Medium, or Hard.
3. Click New Game.
4. Use the on-screen A-Z keyboard or your physical keyboard to guess letters.
5. The server is authoritative. The browser never stores or displays the hidden word while the game is active.

## REST API

The server exposes a JSON API for game creation and guesses.

### Create a game

Request:

   POST /api/games
   Content-Type: application/json

   {"difficulty": "easy"}

Example response:

   {
     "game_id": "abc123",
     "pattern": "_ _ _ _",
     "remaining_guesses": 6,
     "status": "playing"
   }

### Get a game state

Request:

   GET /api/games/<game_id>

Returns the current safe state, including the masked word and guessed/incorrect letters.

The hidden word is included only after the game ends (`won` or `lost`).

### Guess a letter

Request:

   POST /api/games/<game_id>/guess
   Content-Type: application/json

   {"letter": "a"}

Example response:

   {
     "pattern": "_ a _ _",
     "guessed_letters": ["a"],
     "incorrect_letters": [],
     "remaining_guesses": 6,
     "status": "playing"
   }

## Project structure

- `game.py` — core Hangman game engine
- `word_manager.py` — loads word lists and chooses random words by difficulty
- `server.py` — Flask app and REST API
- `static/` — browser client (`index.html`, `style.css`, `app.js`)
- `words/` — Easy, Medium, and Hard word lists
- `tests/` — automated tests
- `requirements.txt` — project dependencies
- `pytest.ini` — pytest configuration

## Run the automated tests

From the project root:

   source .venv/bin/activate
   pytest -q

## Render deployment

This project is ready to deploy to Render using Gunicorn.

Recommended Render Build Command:

   pip install -r requirements.txt

Recommended Render Start Command:

   gunicorn --bind 0.0.0.0:$PORT --workers 1 server:app

Notes:

- No secrets or credentials are required for this project.
- Render should use the Python environment and the root project directory.
- The app is already configured to expose `app` from `server.py`.

## Notes

The Flask server remains authoritative. The browser client does not contain game logic or hidden-word logic; it only renders the safe state returned by the API.
