def display(grid: list[iter]) -> None:
    for row in grid:
        print(row)


def is_valid_points_spaces(points: int, spaces: int, low: int = 1, high: int = 3) -> bool:
    return (points / spaces >= low) and (points / spaces <= high)


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
    all_possible = set(possible_vals)
    all_possible.add('B')

    if val == '?':
        # Update grid with all possible values, sorted
        grid[row_index][col_index] = '/'.join(sorted(all_possible))
    elif val.isdigit() or val == 'B':
        # Do nothing if it's a digit or 'B'
        return
    else:
        # Intersect current values with possible values
        old_vals = set(val.split('/'))
        updated_vals = old_vals.intersection(all_possible)
        # Only update grid if there's a change
        if updated_vals != old_vals:
            grid[row_index][col_index] = '/'.join(sorted(updated_vals))


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


def grid_complete(grid: list[list[str]]) -> bool:
    return not any(any('/' in val for val in row) for row in grid)


def all_futures(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]]) -> bool:
    """
    Only checks the first branch down
    """
    if not reduce(grid, rows, cols):
        return False

    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            val = grid[r][c]
            if val == 'B' or val.isdigit():
                # We already know these
                continue
            possible_vals = val.split('/')
            completed_futures = 0
            for pos_val in possible_vals:
                possible_grid = [row[:] for row in grid]
                possible_grid[r][c] = pos_val
                if not all_futures(possible_grid, rows, cols):
                    grid[r][c] = val.replace(pos_val + '/', '').rstrip('/')
                    if grid[r][c] == 'B' or grid[r][c].isdigit():
                        # We have found what value this needs to be in this future
                        break
                else:
                    completed_futures += 1

            if completed_futures == len(grid[r][c].split('/')):
                # If every future from this index has a completed grid, we don't need to keep checking
                return True


    return True


def update_final(grid: list[list[str]]) -> bool:
    if grid_complete(grid):
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

        clean = [row[:] for row in final]
        for r, row in enumerate(clean):
            for c, val in enumerate(row):
                if len(val) == 1:
                    clean[r][c] = list(val.keys())[0]
        display(clean)
        print('========================================')
        return True
    return False


def reduce(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]], depth: int = 0) -> bool:
    before = [row[:] for row in grid]

    # Do this first so we update the rows and values with points we already know
    if not naive_checker(grid, rows, cols):
        return False

    while before != grid:
        before = [row[:] for row in grid]
        if not naive_checker(grid, rows, cols):
            return False

    update_final(grid)
    return True


def main():
    grid = [
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?']
    ]

    grid = [
        ['?', '?', '?', '1', '?'],
        ['?', '?', '?', '1', '?'],
        ['?', '?', '?', '1', '?'],
        ['?', '?', '?', '2', '?'],
        ['?', '?', '?', '1', '?']
    ]

    rows = [
        [5, 2],
        [7, 1],
        [3, 2],
        [4, 2],
        [6, 1]
    ]

    cols = [
        [5, 2], [5, 2], [7, 1], [6, 0], [2, 3]
    ]

    global final
    final = [[{} for _ in range(len(cols))] for _ in range(len(rows))]

    all_futures(grid, rows, cols)


if __name__ == '__main__':
    main()
