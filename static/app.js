const difficultySelect = document.getElementById('difficulty');
const newGameButton = document.getElementById('new-game-btn');
const patternEl = document.getElementById('pattern');
const statusTextEl = document.getElementById('status-text');
const remainingGuessesEl = document.getElementById('remaining-guesses');
const guessedLettersEl = document.getElementById('guessed-letters');
const incorrectLettersEl = document.getElementById('incorrect-letters');
const messageEl = document.getElementById('message');
const keyboardEl = document.getElementById('keyboard');
const canvas = document.getElementById('hangman-canvas');
const ctx = canvas.getContext('2d');

const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
let currentGameId = null;
let currentState = null;

function setMessage(text) {
  messageEl.textContent = text;
}

function getCurrentDifficulty() {
  return difficultySelect.value;
}

function formatList(items) {
  return items && items.length ? items.map((letter) => `<span class="pill">${letter}</span>`).join('') : '<span>-</span>';
}

function updateKeyboard(state) {
  const usedLetters = new Set([...state.guessed_letters, ...state.incorrect_letters]);

  keyboardEl.innerHTML = '';
  alphabet.forEach((letter) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = letter;
    button.className = 'key';
    if (usedLetters.has(letter.toLowerCase())) {
      button.classList.add('used');
    }
    button.disabled = usedLetters.has(letter.toLowerCase()) || state.status !== 'playing';
    button.addEventListener('click', () => handleGuess(letter));
    keyboardEl.appendChild(button);
  });
}

function drawHangman(mistakes) {
  const width = canvas.width;
  const height = canvas.height;
  ctx.clearRect(0, 0, width, height);

  ctx.lineWidth = 4;
  ctx.strokeStyle = '#1f2937';
  ctx.beginPath();
  ctx.moveTo(30, 220);
  ctx.lineTo(180, 220);
  ctx.moveTo(60, 220);
  ctx.lineTo(60, 30);
  ctx.lineTo(140, 30);
  ctx.lineTo(140, 60);
  ctx.stroke();

  if (mistakes === 0) {
    return;
  }

  const parts = [
    () => {
      ctx.beginPath();
      ctx.arc(140, 85, 25, 0, Math.PI * 2);
      ctx.stroke();
    },
    () => {
      ctx.beginPath();
      ctx.moveTo(140, 110);
      ctx.lineTo(140, 160);
      ctx.stroke();
    },
    () => {
      ctx.beginPath();
      ctx.moveTo(140, 120);
      ctx.lineTo(115, 145);
      ctx.stroke();
    },
    () => {
      ctx.beginPath();
      ctx.moveTo(140, 120);
      ctx.lineTo(165, 145);
      ctx.stroke();
    },
    () => {
      ctx.beginPath();
      ctx.moveTo(140, 160);
      ctx.lineTo(115, 200);
      ctx.stroke();
    },
    () => {
      ctx.beginPath();
      ctx.moveTo(140, 160);
      ctx.lineTo(165, 200);
      ctx.stroke();
    }
  ];

  for (let i = 0; i < mistakes && i < parts.length; i += 1) {
    parts[i]();
  }
}

function normalizeState(state) {
  return {
    ...state,
    guessed_letters: Array.isArray(state.guessed_letters) ? state.guessed_letters : [],
    incorrect_letters: Array.isArray(state.incorrect_letters) ? state.incorrect_letters : []
  };
}

function renderState(state) {
  const normalizedState = normalizeState(state);
  currentState = normalizedState;
  patternEl.textContent = normalizedState.pattern;
  statusTextEl.textContent = normalizedState.status;
  remainingGuessesEl.textContent = normalizedState.remaining_guesses;
  guessedLettersEl.innerHTML = formatList(normalizedState.guessed_letters);
  incorrectLettersEl.innerHTML = formatList(normalizedState.incorrect_letters);

  const mistakes = 6 - normalizedState.remaining_guesses;
  drawHangman(mistakes);

  if (normalizedState.status === 'playing') {
    setMessage('Make your next guess.');
  } else if (normalizedState.status === 'won') {
    setMessage(`You won! The word was "${normalizedState.word}".`);
  } else if (normalizedState.status === 'lost') {
    setMessage(`You lost. The word was "${normalizedState.word}".`);
  }

  updateKeyboard(normalizedState);
}

async function startNewGame() {
  const difficulty = getCurrentDifficulty();
  setMessage('Starting a new game...');

  const response = await fetch('/api/games', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ difficulty })
  });

  const payload = await response.json();
  if (!response.ok) {
    setMessage(payload.error || 'Could not start a new game.');
    return;
  }

  currentGameId = payload.game_id;
  renderState(payload);
}

async function handleGuess(letter) {
  if (!currentGameId || !currentState || currentState.status !== 'playing') {
    return;
  }

  const response = await fetch(`/api/games/${currentGameId}/guess`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ letter })
  });

  const payload = await response.json();
  if (!response.ok) {
    setMessage(payload.error || 'Invalid guess.');
    return;
  }

  renderState(payload);
}

window.addEventListener('keydown', (event) => {
  const key = event.key.toLowerCase();
  if (!/^[a-z]$/.test(key)) {
    return;
  }
  if (!currentGameId || !currentState || currentState.status !== 'playing') {
    return;
  }
  if (currentState.guessed_letters.includes(key) || currentState.incorrect_letters.includes(key)) {
    return;
  }
  handleGuess(key);
});

newGameButton.addEventListener('click', startNewGame);
difficultySelect.addEventListener('change', startNewGame);

startNewGame();
