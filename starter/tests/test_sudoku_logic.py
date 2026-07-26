from starter import sudoku_logic


def test_create_empty_board():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_is_safe_for_empty_board():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.is_safe(board, 0, 0, 1)
    board[0][1] = 1
    assert not sudoku_logic.is_safe(board, 0, 0, 1)
    board[1][0] = 1
    assert not sudoku_logic.is_safe(board, 0, 0, 1)
    board[1][1] = 1
    assert not sudoku_logic.is_safe(board, 0, 0, 1)


def test_generate_puzzle_returns_valid_puzzle_and_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=81)

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert all(len(row) == sudoku_logic.SIZE for row in solution)
    assert puzzle != solution or all(cell != sudoku_logic.EMPTY for row in puzzle for cell in row)
    assert all(1 <= cell <= sudoku_logic.SIZE for row in solution for cell in row)
    assert all(cell == sudoku_logic.EMPTY or 1 <= cell <= sudoku_logic.SIZE for row in puzzle for cell in row)


def test_generate_puzzle_for_difficulty_easy():
    puzzle, solution = sudoku_logic.generate_puzzle_for_difficulty('easy')
    clues = sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row)

    assert clues == sudoku_logic.DIFFICULTY_CLUES['easy']
    assert sudoku_logic.count_solutions(puzzle, 2) == 1
    assert solution != puzzle


def test_generate_puzzle_for_difficulty_medium():
    puzzle, solution = sudoku_logic.generate_puzzle_for_difficulty('medium')
    clues = sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row)

    assert clues == sudoku_logic.DIFFICULTY_CLUES['medium']
    assert sudoku_logic.count_solutions(puzzle, 2) == 1
    assert solution != puzzle


def test_generate_puzzle_for_difficulty_hard():
    puzzle, solution = sudoku_logic.generate_puzzle_for_difficulty('hard')
    clues = sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row)

    assert clues == sudoku_logic.DIFFICULTY_CLUES['hard']
    assert sudoku_logic.count_solutions(puzzle, 2) == 1
    assert solution != puzzle
