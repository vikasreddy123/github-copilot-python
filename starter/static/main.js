// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let timerInterval = null;
let elapsedSeconds = 0;
let gameCompleted = false;
let currentDifficulty = 'medium';
let hintsUsed = 0;
const THEME_KEY = 'sudoku_theme';

function setThemeButtonState(theme) {
  const toggle = document.getElementById('theme-toggle');
  if (!toggle) {
    return;
  }
  const darkMode = theme === 'dark';
  toggle.textContent = darkMode ? 'Light Mode' : 'Dark Mode';
  toggle.setAttribute('aria-pressed', darkMode.toString());
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  setThemeButtonState(theme);
}

function loadTheme() {
  const storedTheme = localStorage.getItem(THEME_KEY);
  const preferredTheme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  applyTheme(storedTheme || preferredTheme);
}

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
  const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
  localStorage.setItem(THEME_KEY, nextTheme);
  applyTheme(nextTheme);
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remaining = seconds % 60;
  return `${minutes.toString().padStart(2, '0')}:${remaining.toString().padStart(2, '0')}`;
}

function updateTimerDisplay() {
  const timer = document.getElementById('timer');
  if (timer) {
    timer.innerText = `Time: ${formatTime(elapsedSeconds)}`;
  }
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  gameCompleted = false;
  hintsUsed = 0;
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
  document.getElementById('hint-cell').disabled = false;
  document.getElementById('check-solution').disabled = false;
}

function disableBoardInputs() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (const input of inputs) {
    input.disabled = true;
  }
}

function getLeaderboard() {
  return JSON.parse(localStorage.getItem('sudoku_leaderboard') || '[]');
}

function setLeaderboard(entries) {
  localStorage.setItem('sudoku_leaderboard', JSON.stringify(entries));
}

function addLeaderboardEntry(entry) {
  const leaderboard = getLeaderboard();
  leaderboard.push(entry);
  leaderboard.sort((a, b) => a.time - b.time);
  leaderboard.splice(10);
  setLeaderboard(leaderboard);
  renderLeaderboard();
}

function askPlayerName() {
  const name = prompt('You solved the puzzle! Enter your name for the leaderboard:', '');
  return name && name.trim() ? name.trim() : 'Anonymous';
}

function renderLeaderboard() {
  const leaderboard = getLeaderboard();
  const table = document.getElementById('leaderboard');
  if (!table) {
    return;
  }
  const tbody = table.querySelector('tbody');
  tbody.innerHTML = '';

  leaderboard.forEach((entry, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${entry.name}</td>
      <td>${formatTime(entry.time)}</td>
      <td>${entry.difficulty}</td>
      <td>${entry.hints ?? 0}</td>
    `;
    tbody.appendChild(row);
  });
}

function saveLeaderboard(timeSeconds) {
  addLeaderboardEntry({
    name: askPlayerName(),
    time: timeSeconds,
    difficulty: currentDifficulty,
    hints: hintsUsed,
    when: new Date().toISOString()
  });
}

async function completeGame() {
  if (gameCompleted) {
    return;
  }
  gameCompleted = true;
  stopTimer();
  disableBoardInputs();
  document.getElementById('hint-cell').disabled = true;
  document.getElementById('check-solution').disabled = true;
  const msg = document.getElementById('message');
  msg.style.color = '#388e3c';
  msg.innerText = `Congratulations! You solved it in ${formatTime(elapsedSeconds)}.`;
  saveLeaderboard(elapsedSeconds);
}

async function checkForCompletion() {
  if (gameCompleted) {
    return;
  }

  const board = getCurrentBoard();
  if (!isPuzzleComplete(board)) {
    return;
  }

  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let idx = 0; idx < inputs.length; idx++) {
    if (inputs[idx].classList.contains('invalid')) {
      return;
    }
  }

  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  if (res.ok && data.incorrect.length === 0) {
    await completeGame();
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', async (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        validateInputCell(e.target);
        await checkForCompletion();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function getCurrentBoard() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];

  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }

  return board;
}

function isValueValidForCell(board, row, col, value) {
  if (value === 0) {
    return true;
  }

  for (let j = 0; j < SIZE; j++) {
    if (j !== col && board[row][j] === value) {
      return false;
    }
  }

  for (let i = 0; i < SIZE; i++) {
    if (i !== row && board[i][col] === value) {
      return false;
    }
  }

  const startRow = Math.floor(row / 3) * 3;
  const startCol = Math.floor(col / 3) * 3;
  for (let i = startRow; i < startRow + 3; i++) {
    for (let j = startCol; j < startCol + 3; j++) {
      if ((i !== row || j !== col) && board[i][j] === value) {
        return false;
      }
    }
  }

  return true;
}

function validateInputCell(input) {
  const row = parseInt(input.dataset.row, 10);
  const col = parseInt(input.dataset.col, 10);
  const board = getCurrentBoard();
  const value = board[row][col];

  if (isValueValidForCell(board, row, col, value)) {
    input.classList.remove('invalid');
  } else {
    input.classList.add('invalid');
  }
}

function isPuzzleComplete(board) {
  return board.every(row => row.every(cell => cell !== 0));
}

function updateHintButtonState() {
  const hintButton = document.getElementById('hint-cell');
  const board = getCurrentBoard();
  hintButton.disabled = isPuzzleComplete(board);
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
  updateHintButtonState();
}

async function newGame() {
  currentDifficulty = document.getElementById('difficulty-select').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(currentDifficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  startTimer();
}

async function checkSolution() {
  const board = getCurrentBoard();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  let missingCount = 0;
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    // FIX: previously only cells with a wrong value were highlighted.
    // Empty (missing) cells on an incomplete board were left unmarked,
    // even though Check should flag both missing and incorrect fields.
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    } else if (!inp.value) {
      inp.className = 'sudoku-cell incorrect';
      missingCount += 1;
    }
  }

  if (incorrect.size === 0 && missingCount === 0) {
    await completeGame();
    return;
  }

  msg.style.color = '#d32f2f';
  if (incorrect.size > 0 && missingCount > 0) {
    msg.innerText = `${incorrect.size} incorrect and ${missingCount} empty cell(s) remain.`;
  } else if (incorrect.size > 0) {
    msg.innerText = 'Some cells are incorrect.';
  } else {
    msg.innerText = `${missingCount} empty cell(s) remain.`;
  }
  updateHintButtonState();
}

async function hintCell() {
  const board = getCurrentBoard();
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');

  if (!res.ok || data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error || 'Unable to get a hint.';
    updateHintButtonState();
    return;
  }

  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const idx = data.row * SIZE + data.col;
  const input = inputs[idx];
  input.value = data.value;
  input.disabled = true;
  input.className = 'sudoku-cell hinted';
  hintsUsed += 1;

  msg.style.color = '#1976d2';
  msg.innerText = 'Hint applied to one empty cell.';
  updateHintButtonState();
  await checkForCompletion();
}

// Wire buttons
window.addEventListener('load', () => {
  loadTheme();
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
  }
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint-cell').addEventListener('click', hintCell);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  renderLeaderboard();
  // initialize
  newGame();
});
