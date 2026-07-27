# Refactor a Sudoku Game written in Python Flask

Use this simple Sudoku game as a starting point to practice your skills with GitHub Copilot. The goal is to refactor the code to use modern technologies, while also adding new features and improving the overall user experience.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Dependencies

```
- Modern web browser (Chrome, Firefox, Edge, etc.)
- Python 3
```

### Installation

1. Fork this repository to your GitHub account. (You can use the "Fork" button on the top right corner of the repository page.)

2. Clone your forked repository to your local machine.

3. Open a terminal window and navigate to the "github-copilot-python/starter" directory.

4. Create a Python virtual environment and activate it (optional but highly recommended).

```bash
python3 -m venv .venv
source .venv/bin/activate
```

5. Install required Python packages.

```bash
pip install -r requirements.txt
```

6. Run the Flask app.

```bash
python app.py
```

7. Open http://127.0.0.1:5000 in your browser.

## Running Tests

After installing dependencies, run the test suite from the `starter` directory:

```bash
pytest
```

If you want to run a specific test file, use:

```bash
pytest tests/test_app.py
```

## Features

- **Difficulty Selector**: Choose Easy (45 clues), Medium (35 clues), or Hard (25 clues) — each puzzle is generated with a guaranteed unique solution
- **Real-Time Validation**: Invalid entries are highlighted immediately as you type, checking row, column, and 3x3 box conflicts
- **Hint Button**: Reveals one correct cell at a time and locks it from further editing
- **Check Solution**: Validates the full board against the solution and highlights incorrect cells
- **Timer**: Tracks elapsed time from the start of a new game until completion
- **Top 10 Leaderboard**: Stores player name, completion time, and difficulty in browser local storage, persisting across sessions
- **Dark Mode Toggle**: Switches the entire UI theme via CSS custom properties
- **Responsive Design**: Adapts from a two-column desktop layout to a stacked single-column mobile layout
