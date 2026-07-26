import copy
import random
from typing import List, Tuple

SIZE = 9
EMPTY = 0
Board = List[List[int]]
DIFFICULTY_CLUES = {
    'easy': 45,
    'medium': 35,
    'hard': 25,
}
DEFAULT_DIFFICULTY = 'medium'
MAX_GENERATION_ATTEMPTS = 10


def deep_copy(board: Board) -> Board:
    """Return a deep copy of a Sudoku board."""
    return copy.deepcopy(board)


def create_empty_board() -> Board:
    """Create an empty 9x9 Sudoku board filled with EMPTY values."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_in_row(board: Board, row: int, num: int) -> bool:
    """Return True if num is present in the given row."""
    return any(cell == num for cell in board[row])


def is_in_col(board: Board, col: int, num: int) -> bool:
    """Return True if num is present in the given column."""
    return any(board[row][col] == num for row in range(SIZE))


def is_in_box(board: Board, row: int, col: int, num: int) -> bool:
    """Return True if num is present in the 3x3 box for the cell."""
    start_row = row - row % 3
    start_col = col - col % 3
    return any(
        board[start_row + dr][start_col + dc] == num
        for dr in range(3)
        for dc in range(3)
    )


def is_safe(board: Board, row: int, col: int, num: int) -> bool:
    """Return True if num can be placed at board[row][col] without conflicts."""
    return not (
        is_in_row(board, row, num)
        or is_in_col(board, col, num)
        or is_in_box(board, row, col, num)
    )


def _get_candidates(board: Board, row: int, col: int) -> List[int]:
    """Return all valid candidate values for a board cell."""
    return [num for num in range(1, SIZE + 1) if is_safe(board, row, col, num)]


def _select_empty_cell(board: Board) -> Tuple[int, int] | None:
    """Select the empty cell with the fewest valid candidates."""
    best_cell = None
    best_count = SIZE + 1

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                candidates = _get_candidates(board, row, col)
                candidate_count = len(candidates)
                if candidate_count == 0:
                    return row, col
                if candidate_count < best_count:
                    best_count = candidate_count
                    best_cell = (row, col)
                    if best_count == 1:
                        return best_cell

    return best_cell


def fill_board(board: Board) -> bool:
    """Fill the board with a valid Sudoku solution using backtracking."""
    next_cell = _select_empty_cell(board)
    if next_cell is None:
        return True

    row, col = next_cell
    candidates = _get_candidates(board, row, col)
    random.shuffle(candidates)

    for candidate in candidates:
        board[row][col] = candidate
        if fill_board(board):
            return True
        board[row][col] = EMPTY

    return False


def _count_solutions(board: Board, max_solutions: int = 2) -> int:
    """Count valid solutions for a board up to max_solutions."""
    empty_cell = _select_empty_cell(board)
    if empty_cell is None:
        return 1

    row, col = empty_cell
    solutions = 0
    candidates = _get_candidates(board, row, col)
    for candidate in candidates:
        board[row][col] = candidate
        solutions += _count_solutions(board, max_solutions)
        board[row][col] = EMPTY
        if solutions >= max_solutions:
            return solutions

    return solutions


def solve(board: Board, max_solutions: int = 2) -> int:
    """Count the number of valid solutions for a board using backtracking.

    The solver stops early once `max_solutions` is reached, which keeps
    uniqueness checking fast for most puzzles.
    """
    return _count_solutions(deep_copy(board), max_solutions)


def count_solutions(board: Board, max_solutions: int = 2) -> int:
    """Count the number of valid solutions for a board without mutating the original."""
    return solve(board, max_solutions)


def get_clue_count(difficulty: str = DEFAULT_DIFFICULTY) -> int:
    """Return the number of clues for a difficulty string."""
    difficulty_key = (difficulty or DEFAULT_DIFFICULTY).lower()
    return DIFFICULTY_CLUES.get(difficulty_key, DIFFICULTY_CLUES[DEFAULT_DIFFICULTY])


def generate_puzzle_for_difficulty(difficulty: str = DEFAULT_DIFFICULTY) -> Tuple[Board, Board]:
    """Generate a Sudoku puzzle and its full solution for the requested difficulty."""
    clues = get_clue_count(difficulty)
    return generate_puzzle(clues)


def remove_cells(board: Board, clues: int) -> bool:
    """Remove cells from a filled board while preserving a unique solution."""
    current_clues = sum(1 for row in board for cell in row if cell != EMPTY)

    while current_clues > clues:
        positions = [
            (row, col)
            for row in range(SIZE)
            for col in range(SIZE)
            if board[row][col] != EMPTY
        ]
        random.shuffle(positions)

        removed = False
        for row, col in positions:
            if current_clues <= clues:
                break

            backup = board[row][col]
            board[row][col] = EMPTY
            if count_solutions(board, 2) == 1:
                current_clues -= 1
                removed = True
            else:
                board[row][col] = backup

        if not removed:
            return False

    return True


def generate_puzzle(clues: int = 35) -> Tuple[Board, Board]:
    """Generate a Sudoku puzzle and its full solution.

    This function generates a fully solved board and then removes cells
    while preserving a unique solution. If the desired clue count cannot be
    reached in one generated board, the generator recreates the board and
    tries again until a valid puzzle is produced.
    """
    while True:
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        if remove_cells(board, clues):
            puzzle = deep_copy(board)
            return puzzle, solution
