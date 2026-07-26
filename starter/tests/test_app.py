from starter import app

def test_index_route_returns_html():
    with app.app.test_client() as client:
        response = client.get('/')

    assert response.status_code == 200
    assert b'<html' in response.data or b'<!DOCTYPE html>' in response.data


def test_new_game_returns_puzzle_and_sets_solution():
    app.CURRENT['solution'] = None
    with app.app.test_client() as client:
        response = client.get('/new?clues=81')

    assert response.status_code == 200
    data = response.get_json()
    assert 'puzzle' in data
    puzzle = data['puzzle']
    assert len(puzzle) == app.sudoku_logic.SIZE
    assert all(len(row) == app.sudoku_logic.SIZE for row in puzzle)
    assert all(1 <= cell <= app.sudoku_logic.SIZE for row in puzzle for cell in row)
    assert app.CURRENT['solution'] is not None


def test_new_game_with_difficulty():
    app.CURRENT['solution'] = None
    with app.app.test_client() as client:
        response = client.get('/new?difficulty=hard')

    assert response.status_code == 200
    data = response.get_json()
    assert 'puzzle' in data
    puzzle = data['puzzle']
    clues = sum(cell != 0 for row in puzzle for cell in row)
    assert clues >= 25
    assert clues <= 35
    assert app.CURRENT['solution'] is not None


def test_hint_cell_returns_empty_cell_hint():
    with app.app.test_client() as client:
        response = client.get('/new?difficulty=medium')
        puzzle = response.get_json()['puzzle']
        board = [row[:] for row in puzzle]
        hint_response = client.post('/hint', json={'board': board})

    assert hint_response.status_code == 200
    hint = hint_response.get_json()
    assert 'row' in hint and 'col' in hint and 'value' in hint
    assert board[hint['row']][hint['col']] == 0
    assert hint['value'] == app.CURRENT['solution'][hint['row']][hint['col']]


def test_check_solution_with_correct_board():
    app.CURRENT['solution'] = None
    with app.app.test_client() as client:
        new_response = client.get('/new?clues=81')
        solution = new_response.get_json()['puzzle']
        response = client.post('/check', json={'board': solution})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_check_solution_with_incorrect_board():
    app.CURRENT['solution'] = None
    with app.app.test_client() as client:
        new_response = client.get('/new?clues=81')
        solution = new_response.get_json()['puzzle']
        board = [row[:] for row in solution]
        board[0][0] = 1 if solution[0][0] != 1 else 2
        response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json()['incorrect'] == [[0, 0]]


def test_check_solution_without_game_in_progress():
    app.CURRENT['solution'] = None
    with app.app.test_client() as client:
        response = client.post('/check', json={'board': [[0] * app.sudoku_logic.SIZE for _ in range(app.sudoku_logic.SIZE)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_solution_ignores_empty_cells():
    app.CURRENT['solution'] = None
    with app.app.test_client() as client:
        new_response = client.get('/new?clues=81')
        solution = new_response.get_json()['puzzle']
        board = [[0] * app.sudoku_logic.SIZE for _ in range(app.sudoku_logic.SIZE)]
        board[0][0] = 1 if solution[0][0] != 1 else 2
        response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json()['incorrect'] == [[0, 0]]
