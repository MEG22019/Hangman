# TODO — Required Hangman Assignment Plan

This file is the implementation roadmap for the required assignment scope only.

The project must include the Python Hangman game engine, Easy/Medium/Hard word lists, Flask server, REST API, browser client, testing/debugging, deployment to Render, and documentation. Out-of-scope features such as terminal clients, bot evaluation, scoring, replay systems, and leaderboards are intentionally excluded.

## Implementation Rules

- Implement one phase at a time.
- Complete and validate each phase before moving on to the next.
- Keep the game engine independent from Flask and browser code.
- Treat the server as the authoritative source of game state.
- Never reveal the hidden word before a game ends.
- Add tests as each phase is built rather than deferring all tests until the end.
- Deploy the final assignment only after local functionality is working.

---

## Phase 1 — Project Skeleton and Core Game Engine

### Tasks

- [x] Create the project directory structure.
- [x] Add the word-list files in the required `words/` directory structure.
- [x] Create `game.py`.
- [x] Implement a `HangmanGame` class.
- [x] Store the hidden word internally.
- [x] Track guessed letters and incorrect letters.
- [x] Track the maximum number of incorrect guesses.
- [x] Validate that guesses are single alphabetic letters.
- [x] Handle duplicate guesses consistently.
- [x] Generate the masked word pattern.
- [x] Detect win and loss states.
- [x] Represent game status such as `playing`, `won`, and `lost`.
- [x] Return a client-safe state dictionary that hides the answer until the game ends.
- [x] Add unit tests for core game rules.

### Completion Criteria

The game engine can be tested without a web server.

Core Hangman rules are covered by automated tests.

---

## Phase 2 — Word Management

### Tasks

- [x] Create a word-loading helper or module.
- [x] Load Easy, Medium, and Hard word lists.
- [x] Validate that words contain only alphabetic characters.
- [x] Remove accidental duplicates from each list.
- [x] Support random word selection by difficulty.
- [x] Reject invalid difficulty values cleanly.
- [x] Add tests for word loading and selection logic.

### Completion Criteria

The program can select a random valid word for each difficulty level.

Invalid difficulty inputs are rejected with a clear error.

---

## Phase 3 — Flask Server and REST API

### Tasks

- [x] Create `server.py`.
- [x] Configure Flask.
- [x] Maintain in-memory storage for active games.
- [x] Generate unique game IDs.
- [x] Implement `POST /api/games` to start a new game.
- [x] Implement `GET /api/games/<game_id>` to fetch the current game state.
- [x] Implement `POST /api/games/<game_id>/guess` to submit a letter.
- [x] Validate difficulty input.
- [x] Validate guess input.
- [x] Return consistent JSON responses.
- [x] Return correct HTTP status codes for success and errors.
- [x] Handle unknown game IDs and malformed requests.
- [x] Ensure the hidden word is not leaked while a game is in progress.
- [x] Add API tests for the main request flows.

### Completion Criteria

A full game can be played over HTTP using only the REST API.

The web browser client is not required to complete this phase.

---

## Phase 4 — Browser Client (HTML/CSS/JavaScript)

### Tasks

- [x] Create `static/index.html`.
- [x] Create `static/style.css`.
- [x] Create `static/app.js`.
- [x] Add a difficulty selector.
- [x] Add a New Game button.
- [x] Display the masked word to the player.
- [x] Display guessed and incorrect letters.
- [x] Display remaining wrong-guess count.
- [x] Use `fetch()` to call the Flask API.
- [x] Add a keyboard or clickable letter input for guesses.
- [x] Disable already-guessed letters in the UI.
- [x] Display win/loss outcomes to the user.
- [x] Provide a restart/new-game flow.
- [x] Make the interface usable on common desktop and mobile sizes.

### Completion Criteria

A user can play the game in a browser against the server without any hidden-word logic in the browser.

The UI reflects the server-authoritative state after every guess.

---

## Phase 5 — Testing, Debugging, and Verification

### Tasks

- [x] Run the unit tests for the game engine.
- [x] Run the API tests for the REST server.
- [x] Verify valid game states and error conditions.
- [x] Check that the hidden word remains protected during play.
- [x] Fix bugs discovered during testing.
- [x] Confirm that the browser client works against the API in a local browser session.

### Completion Criteria

The project works locally end-to-end without known logic or API issues.

The app behaves correctly for both standard gameplay and error cases.

---

## Phase 6 — Deployment to Render

### Tasks

- [x] Prepare the app for deployment on Render.
- [x] Add the required dependencies and runtime configuration.
- [x] Configure the WSGI entrypoint for Flask.
- [x] Set production environment values if needed.
- [x] Verify the deployed app loads successfully and the API responds locally with Gunicorn.
- [ ] Deploy the application to Render from the GitHub repository using the configured start command.

### Completion Criteria

The application is prepared for successful deployment on Render.

The project serves the same core Hangman functionality locally with Gunicorn as it does in development.

---

## Phase 7 — README and Project Documentation

### Tasks

- [x] Write a clear project overview.
- [x] Document the required features and architecture.
- [x] Explain how to install dependencies and run the app locally.
- [x] Document the REST API endpoints.
- [x] Explain how to use the browser client.
- [x] Include deployment steps for Render.
- [x] Summarize any assumptions or design decisions.

### Completion Criteria

The README provides enough information for another developer to run, test, and deploy the assignment.

---

## Explicitly Out of Scope for This Assignment

The following items are intentionally not included in this roadmap because they are outside the required assignment scope:

- Terminal client
- Automated bot clients
- Bot evaluation mode
- Scoring system
- Leaderboards
- Replay systems
- Advanced anti-cheat or session-management features
- Any other features not listed in the required deliverables

These features were removed from the implementation plan to keep the project aligned with the assignment requirements and to avoid building extra, ungraded functionality.
