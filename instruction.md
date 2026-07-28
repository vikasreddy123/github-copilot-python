# GitHub Copilot Instructions for Sudoku Application

## Project Overview

This is a 9x9 Sudoku web application built with Flask (Python backend) and vanilla JavaScript/CSS (frontend). The backend generates puzzles and validates solutions; the frontend renders the board, handles user interaction, and persists leaderboard/theme data in localStorage.

## Code Standards and Architecture

- **Modular design**: keep puzzle-generation logic (`sudoku_logic.py`), Flask routes (`app.py`), and frontend rendering/interaction (`main.js`) in separate, single-responsibility files.
- **Documentation**: add comments explaining non-obvious logic, especially the backtracking puzzle generator and the unique-solution check in `sudoku_logic.py`.
- **Error handling**: Flask routes should return clear JSON error messages (e.g. `{'error': 'No game in progress'}`) with appropriate status codes when no puzzle is active.
- **Testing**: every new feature should have a corresponding pytest test in `starter/tests/`. Run `pytest` after any change and confirm all tests still pass before considering a feature complete.
- **Build & run**: the app must install cleanly via `pip install -r requirements.txt` and run with `python app.py` without console errors in the browser.

## User Interface Requirements

- Use plain CSS (no framework) with CSS custom properties (`--bg`, `--text`, `--block-bg`, etc.) for theming.
- 3x3 Sudoku sub-grids must alternate background color using `:nth-child` selectors scoped precisely to each block's row and column range — double check ranges don't accidentally bleed into neighboring blocks.
- Layout must adapt cleanly between desktop (two-column grid) and mobile (single column, resized cells) using media queries at 900px and 640px breakpoints.
- Dark mode is toggled via a `data-theme` attribute on `<html>`, persisted in `localStorage`, and must keep all text/buttons readable in both themes.

## Core Sudoku Logic

- Puzzles must have exactly one unique solution, verified via `count_solutions()` before removing any additional clue.
- Difficulty levels use `DIFFICULTY_CLUES`: Easy = 45 clues, Medium = 35 clues, Hard = 25 clues.
- Prefilled cells must be locked (`disabled` input, `.prefilled` class).

## Interactive Features

- **Hint**: pick a random empty cell, fill it from the stored solution, disable it, and mark it `.hinted`. Increment a `hintsUsed` counter for leaderboard tracking.
- **Check**: compare all filled cells against the solution AND flag any still-empty cells as missing — both should be visually marked red. Do not treat an "all filled cells correct" board as solved unless it is also fully filled.
- **Timer**: start on new game, stop on completion, format as `MM:SS`.
- **Leaderboard**: on genuine completion (fully filled and correct), prompt for a name and save `{name, time, difficulty, hints}` to `localStorage`, keeping only the fastest 10 entries.

## When Suggesting Code

- Prefer small, targeted changes over rewriting whole files.
- When generating CSS selectors for the grid, always double-check `:nth-child` ranges against a concrete 1-9 column mapping rather than assuming a pattern is correct.
- When touching completion-detection logic, always verify both "no incorrect cells" AND "no empty cells" before declaring a puzzle solved.
