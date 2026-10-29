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

- [ ] Create `server.py`.
- [ ] Configure Flask.
- [ ] Maintain in-memory storage for active games.
- [ ] Generate unique game IDs.
- [ ] Implement `POST /api/games` to start a new game.
- [ ] Implement `GET /api/games/<game_id>` to fetch the current game state.
- [ ] Implement `POST /api/games/<game_id>/guess` to submit a letter.
- [ ] Validate difficulty input.
- [ ] Validate guess input.
- [ ] Return consistent JSON responses.
- [ ] Return correct HTTP status codes for success and errors.
- [ ] Handle unknown game IDs and malformed requests.
- [ ] Ensure the hidden word is not leaked while a game is in progress.
- [ ] Add API tests for the main request flows.

### Completion Criteria

A full game can be played over HTTP using only the REST API.

The web browser client is not required to complete this phase.

---

## Phase 4 — Browser Client (HTML/CSS/JavaScript)

### Tasks

- [ ] Create `static/index.html`.
- [ ] Create `static/style.css`.
- [ ] Create `static/app.js`.
- [ ] Add a difficulty selector.
- [ ] Add a New Game button.
- [ ] Display the masked word to the player.
- [ ] Display guessed and incorrect letters.
- [ ] Display remaining wrong-guess count.
- [ ] Use `fetch()` to call the Flask API.
- [ ] Add a keyboard or clickable letter input for guesses.
- [ ] Disable already-guessed letters in the UI.
- [ ] Display win/loss outcomes to the user.
- [ ] Provide a restart/new-game flow.
- [ ] Make the interface usable on common desktop and mobile sizes.

### Completion Criteria

A user can play the game in a browser against the server without any hidden-word logic in the browser.

The UI reflects the server-authoritative state after every guess.

---

## Phase 5 — Testing, Debugging, and Verification

### Tasks

- [ ] Run the unit tests for the game engine.
- [ ] Run the API tests for the REST server.
- [ ] Verify valid game states and error conditions.
- [ ] Check that the hidden word remains protected during play.
- [ ] Fix bugs discovered during testing.
- [ ] Confirm that the browser client works against the API in a local browser session.

### Completion Criteria

The project works locally end-to-end without known logic or API issues.

The app behaves correctly for both standard gameplay and error cases.

---

## Phase 6 — Deployment to Render

### Tasks

- [ ] Prepare the app for deployment on Render.
- [ ] Add the required dependencies and runtime configuration.
- [ ] Configure the WSGI entrypoint for Flask.
- [ ] Set production environment values if needed.
- [ ] Deploy the application to Render.
- [ ] Verify the deployed app loads successfully and the API responds.

### Completion Criteria

The application is successfully deployed and reachable on Render.

The deployed version serves the same core Hangman functionality as the local build.

---

## Phase 7 — README and Project Documentation

### Tasks

- [ ] Write a clear project overview.
- [ ] Document the required features and architecture.
- [ ] Explain how to install dependencies and run the app locally.
- [ ] Document the REST API endpoints.
- [ ] Explain how to use the browser client.
- [ ] Include deployment steps for Render.
- [ ] Summarize any assumptions or design decisions.

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
