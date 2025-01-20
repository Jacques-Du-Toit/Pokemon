from app.voltorb_sudoku_calc import find_possible_values, check_points_bombs


def test_possible_values():
    assert find_possible_values(1, 1, 0, '', 1, 3) == ['1']
    assert find_possible_values(3, 3, 0, '', 1, 3) == ['1']
    assert find_possible_values(4, 3, 0, '', 1, 3) == ['1', '2']
    assert find_possible_values(5, 3, 0, '', 1, 3) == ['1', '2', '3']
    assert find_possible_values(6, 2, 0, '', 1, 3) == ['3']
    assert find_possible_values(7, 3, 0, '', 1, 3) == ['1', '2', '3']
    assert find_possible_values(2, 1, 0, '', 1, 3) == ['2']
    assert find_possible_values(5, 2, 0, '', 1, 3) == ['2', '3']


def test_check_points_bombs():
    grid = [
        ['B', '2', '1', '1', '1'],
        ['B', 'B', '1', '1', '2'],
        ['B', '3', '1', '2', '1'],
        ['1', 'B', 'B', '1', 'B'],
        ['1', '3', '2', 'B', '1']
    ]
    rows = [
        [5, 1],
        [4, 2],
        [7, 1],
        [2, 3],
        [8, 1]
    ]
    cols = [
        [2, 3], [8, 2], [5, 1], [6, 1], [5, 1]
    ]
    assert check_points_bombs(grid, rows, cols) == False

    grid = [
        ['B', '2', '1', '1', '1'],
        ['B', 'B', '1', '1', '2'],
        ['B', '3', '1', '2', '1'],
        ['1', 'B', 'B', '1', 'B'],
        ['1', '3', '2', '1', '1']
    ]
    assert check_points_bombs(grid, rows, cols) == False
