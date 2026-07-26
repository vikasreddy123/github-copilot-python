import random
from flask import Flask, render_template, jsonify, request

try:
    from . import sudoku_logic
except ImportError:
    import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty')
    if difficulty:
        puzzle, solution = sudoku_logic.generate_puzzle_for_difficulty(difficulty)
    else:
        clues = int(request.args.get('clues', 35))
        puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            value = board[i][j]
            if value != 0 and value != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})

@app.route('/hint', methods=['POST'])
def hint_cell():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    empty_cells = [
        (i, j)
        for i in range(sudoku_logic.SIZE)
        for j in range(sudoku_logic.SIZE)
        if board[i][j] == 0
    ]

    if not empty_cells:
        return jsonify({'error': 'No empty cells remain'}), 400

    row, col = random.choice(empty_cells)
    return jsonify({'row': row, 'col': col, 'value': solution[row][col]})

if __name__ == '__main__':
    app.run(debug=True)