from app.voltorb_sudoku_calc import find_possible_values


def test_possible_values():
    assert find_possible_values(1, 1, 0, '', 1, 3) == ['1']
    assert find_possible_values(3, 3, 0, '', 1, 3) == ['1']
    assert find_possible_values(4, 3, 0, '', 1, 3) == ['1', '2']
    assert find_possible_values(5, 3, 0, '', 1, 3) == ['1', '2', '3']
    assert find_possible_values(6, 2, 0, '', 1, 3) == ['3']
    assert find_possible_values(7, 3, 0, '', 1, 3) == ['1', '2', '3']
    assert find_possible_values(2, 1, 0, '', 1, 3) == ['2']
    assert find_possible_values(5, 2, 0, '', 1, 3) == ['2', '3']
