from copy import deepcopy
from time import sleep
from functools import lru_cache


def display(grid: list[iter]) -> None:
    for row in grid:
        print(row)


def is_valid_points_spaces(points: int, spaces: int, low: int = 1, high: int = 3) -> bool:
    return (points / spaces >= low) and (points / spaces <= high)

@lru_cache(maxsize=None)
def find_possible_values(points: int, spaces: int, low: int = 1, high: int = 3) -> list[str]:
    """Determines the possible values a space can have from the points and spaces left in that line"""
    if spaces == 0:
        return ['']

    if not is_valid_points_spaces(points, spaces, low, high):
        return ['Invalid State', str(points), str(spaces)]

    if spaces == 1:
        return [str(points)]

    return [str(val) for val in range(low, high + 1) if is_valid_points_spaces(points - val, spaces - 1, low, high)]


def update_val(grid: list[list[str]], row_index: int, col_index: int, possible_vals: list[str]) -> None:
    val = grid[row_index][col_index]
    possible_vals = ['B'] + possible_vals
    if val == '?':
        possible_vals.sort()
        grid[row_index][col_index] = '/'.join(possible_vals)
    elif val.isdigit() or val == 'B':
        pass
    else:
        old_vals = val.split('/')
        possible_vals = list(set(old_vals).intersection(['B'] + possible_vals))
        possible_vals.sort()
        grid[row_index][col_index] = '/'.join(possible_vals)


def naive_checker(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]]) -> bool:
    """
    Inputs what values are possible for each line based on the total points and spaces.
    Considered 'naive' as only checks which points are possible across the whole line rather than per value
    """
    for r, row in enumerate(rows):
        vals = grid[r]
        if vals.count('') > 0:
            return False
        points = row[0] - sum([int(val) for val in vals if val.isdigit()])
        spaces = len(cols) - len([val for val in vals if val.isdigit()]) - row[1]
        if points < 0 or spaces < 0:
            return False
        possible_vals = find_possible_values(points, spaces)
        if possible_vals[0] == 'Invalid State':
            return False
        for c, val in enumerate(grid[r]):
            update_val(grid, r, c, possible_vals)

    for c, col in enumerate(cols):
        vals = [grid[r][c] for r in range(len(rows))]
        if vals.count('') > 0:
            return False
        points = col[0] - sum([int(val) for val in vals if val.isdigit()])
        spaces = len(rows) - len([val for val in vals if val.isdigit()]) - col[1]
        if points < 0 or spaces < 0:
            return False
        possible_vals = find_possible_values(points, spaces)
        if possible_vals[0] == 'Invalid State':
            return False
        for r in range(len(rows)):
            update_val(grid, r, c, possible_vals)

    return cancel_out_bombs_points(grid, rows, cols)


def cancel_out_bombs_points(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]]):
    """If there are enough bombs in a line - it removes it from other vals in that line."""
    for r, row in enumerate(rows):
        vals = grid[r]
        num_bombs = vals.count('B')
        if num_bombs > row[1]:
            return False
        if num_bombs == row[1]:
            grid[r] = [val.replace('B/', '').replace('/B', '') for val in vals]

        if len([val for val in vals if val.isdigit() or val == 'B']) == len(cols):
            if sum([int(val) for val in vals if val.isdigit()]) != row[0]:
                return False


    for c, col in enumerate(cols):
        vals = [grid[r][c] for r in range(len(rows))]
        num_bombs = vals.count('B')
        if num_bombs > col[1]:
            return False
        if num_bombs == col[1]:
            new_vals = [val.replace('B/', '').replace('/B', '') for val in vals]
            for r in range(len(rows)):
                grid[r][c] = new_vals[r]

        if len([val for val in vals if val.isdigit() or val == 'B']) == len(rows):
            if sum([int(val) for val in vals if val.isdigit()]) != col[0]:
                return False

    return True


def shallow_future(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]], level: int) -> bool:
    """
    Only checks the first branch down
    """
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            val = grid[r][c]
            if not naive_checker(grid, rows, cols):
                return False
            if val == 'B' or val.isdigit():
                # We already know these
                continue
            possible_vals = val.split('/')
            for pos_val in possible_vals:
                possible_grid = deepcopy(grid)
                possible_grid[r][c] = pos_val
                if False:
                    display(grid)
                    print('====================================')
                    display(possible_grid)
                    print(f'{r=}, {c=}, {val=}, {pos_val=}')
                    sleep(0.5)
                    print('====================================')
                    print('====================================')
                if not iterate(possible_grid, rows, cols, level-1):
                    grid[r][c] = val.replace(pos_val + '/', '').rstrip('/')
                    if grid[r][c] == 'B' or grid[r][c].isdigit():
                        # We have found what value this needs to be in this future
                        break

    return True


def update_final(grid: list[list[str]]) -> None:
    if not any(any('/' in val for val in row) for row in grid):
        global final

        best_ratio = 1
        best_co_ords = []
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                final[r][c][val] = final[r][c].get(val, 0) + 1
                vals = final[r][c].values()
                if len(vals) > 1:
                    ratio = final[r][c].get('B', 0) / sum(vals)
                    if ratio < best_ratio:
                        best_ratio = ratio
                        best_co_ords = [r+1, c+1]
        print(f'{best_ratio=:.2f}, {best_co_ords=}')

        clean = deepcopy(final)
        for r, row in enumerate(clean):
            for c, val in enumerate(row):
                if len(val) == 1:
                    clean[r][c] = list(val.keys())[0]

        print('========================================')
        display(clean)
        print('========================================')


def iterate(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]], depth: int = 0) -> bool:
    before = [row[:] for row in grid]

    # Do this first so we update the rows and values with points we already know
    if not naive_checker(grid, rows, cols):
        return False

    while before != grid:
        before = deepcopy(grid)
        if not naive_checker(grid, rows, cols):
            return False

    if depth > 0:
        shallow_search(grid, rows, cols, depth)
        update_final(grid)

    return True


def shallow_search(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]], level: int):
    before = [row[:] for row in grid]
    shallow_future(grid, rows, cols, level)

    while before != grid:
        shallow_future(grid, rows, cols, level)
        before = deepcopy(grid)


def main():
    grid = [
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?']
    ]

    grid = [
        ['?', '?', '3', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?']
    ]

    rows = [
        [6, 1],
        [6, 1],
        [4, 3],
        [5, 2],
        [6, 1]
    ]
    cols = [
        [6, 1], [4, 1], [6, 1], [4, 3], [7, 2]
    ]

    global final
    final = [[{} for _ in range(len(cols))] for _ in range(len(rows))]

    for depth in range(1, 100):
        iterate(grid, rows, cols, depth)


if __name__ == '__main__':
    main()
