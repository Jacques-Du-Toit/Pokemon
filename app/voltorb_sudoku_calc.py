import copy


def display(grid: list[iter]) -> None:
    for row in grid:
        print(row)


def update_rows_cols(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]]) -> None:
    """Reduces the point and bomb numbers of row and columns by the points and bombs we know of"""
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if '/' in val: # this tells us that we haven't accounted for it yet
                if val[:-1].isdigit():
                    val = val[:-1]
                    grid[r][c] = val
                    rows[r][0] -= int(val)
                    cols[c][0] -= int(val)
                    rows[r][2] -= 1
                    cols[c][2] -= 1

                elif val == 'B/':
                    grid[r][c] = 'B'
                    rows[r][1] -= 1
                    cols[c][1] -= 1
                    rows[r][2] -= 1
                    cols[c][2] -= 1


def is_valid_points_spaces(points: int, spaces: int, low: int = 1, high: int = 3) -> bool:
    return (points / spaces >= low) and (points / spaces <= high)


def find_possible_values(points: int, spaces: int, index: int, line: str,  low: int = 1, high: int = 3) -> list[str]:
    """Determines the possible values a space can have from the points and spaces left in that line"""
    if spaces == 0:
        return ['']

    if not is_valid_points_spaces(points, spaces, low, high):
        return ['Invalid State', line, str(index+1), str(points), str(spaces)]

    if spaces == 1:
        return [str(points)]

    return [str(val) for val in range(low, high + 1) if is_valid_points_spaces(points - val, spaces - 1, low, high)]


def update_val(grid: list[list[str]], row_index: int, col_index: int, possible_vals: list[str]) -> None:
    val = grid[row_index][col_index]
    if val == '?':
        grid[row_index][col_index] = 'B/' + '/'.join(possible_vals)
    elif val.isdigit() or val == 'B':
        pass
    else:
        old_vals = val.split('/')
        grid[row_index][col_index] = 'B/' + '/'.join(set(old_vals).intersection(possible_vals))


def naive_checker(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]]) -> bool:
    """
    Inputs what values are possible for each line based on the total points and spaces.
    Considered 'naive' as only checks which points are possible across the whole line rather than per value
    """
    for r, row in enumerate(rows):
        points = row[0]
        spaces = row[2] - row[1]
        possible_vals = find_possible_values(points, spaces, index=r, line='row')
        if possible_vals[0] == 'Invalid State': return False
        for c, val in enumerate(grid[r]):
            update_val(grid, r, c, possible_vals)

    for c, col in enumerate(cols):
        points = col[0]
        spaces = col[2] - col[1]
        possible_vals = find_possible_values(points, spaces, index=c, line='col')
        if possible_vals[0] == 'Invalid State': return False
        for r in range(len(rows)):
            update_val(grid, r, c, possible_vals)

    return True


def points_bombs_line(vals: list[str], limits: list[int], max_len: int = 5) -> bool:
    point_vals = [int(val) for val in vals if val.isdigit()]
    points = sum(point_vals)
    if points > limits[0]:
        return False
    num_bombs = len([val for val in vals if val == 'B'])
    if num_bombs> limits[1]:
        return False
    if len(point_vals) + num_bombs == max_len:
        if points < limits[0]:
            return False
        if num_bombs < limits[1]:
            return False
    return True


def check_points_bombs(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]]) -> bool:
    for r, row in enumerate(rows):
        if not points_bombs_line(grid[r], row, len(cols)):
            return False

    for c, col in enumerate(cols):
        if not points_bombs_line([grid[r_i][c] for r_i in range(len(rows))], col, len(rows)):
            return False

    return True


def all_futures_checker(
        grid: list[list[str]],
        rows: list[list[int]], cols: list[list[int]],
        og_rows: list[list[int]], og_cols: list[list[int]]
):
    """
    After the possible values per line are determined,
    this tries every possible combination of values to see if there are any paradoxes.
    It removes any values that cause paradoxes
    """

    # Don't want it changing the rows or cols
    check_rows = copy.deepcopy(rows)
    check_cols = copy.deepcopy(cols)
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 'B' or val.isdigit() or ('/' in val and val[:-1].isdigit()):
                # We already know these
                continue
            possible_vals = val.split('/')
            for pos_val in possible_vals:
                possible_grid = copy.deepcopy(grid)
                possible_grid[r][c] = pos_val + '/'
                if not iterate_through(possible_grid, check_rows, check_cols, og_rows, og_cols):
                    grid[r][c] = val.replace(pos_val + '/', '')
                    if grid[r][c] == 'B' or grid[r][c].isdigit():
                        break


def iterate_through(
        grid: list[list[str]],
        rows: list[list[int]], cols: list[list[int]],
        og_rows: list[list[int]], og_cols: list[list[int]]
) -> bool:
    """Calculates the possible values for each value"""
    before = copy.deepcopy(grid)

    # Do this first so we update the rows and values with points we already know
    update_rows_cols(grid, rows, cols)
    naive_checker(grid, rows, cols)

    while before != grid:
        before = copy.deepcopy(grid)
        update_rows_cols(grid, rows, cols)
        if not naive_checker(grid, rows, cols):
            return False
        if not check_points_bombs(grid, og_rows, og_cols):
            return False

    all_futures_checker(grid, rows, cols, og_rows, og_cols)
    if not check_points_bombs(grid, og_rows, og_cols):
        return False

    if not any(any('/' in val for val in row) for row in grid):
        global all_possible
        if grid not in all_possible:
            all_possible.append(grid)
            display(grid)
            print('=============================================')
            indexes = [[r_i, c_i] for r_i in range(len(rows)) for c_i in range(len(cols))]
            final = [[{} for _ in range(len(cols))] for _ in range(len(rows))]

            for index in indexes:
                for pos_grid in all_possible:
                    val = pos_grid[index[0]][index[1]]
                    final[index[0]][index[1]][val] = final[index[0]][index[1]].get(val, 0) + 1

            for r, row in enumerate(final):
                for c, val in enumerate(row):
                    if len(val) == 1:
                        final[r][c] = list(val.keys())[0]

            display(final)
            print('=============================================')
            print('=============================================')

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
        ['?', '?', '?', '1/', '1/'],
        ['?', '?', '?', '?', '2/'],
        ['2/', '1/', '1/', '2/', '1/'],
        ['?', '?', '?', '?', '1/'],
        ['?', '?', '?', '?', '1/']
    ]
    
    rows = [
        [4, 1],
        [6, 1],
        [7, 0],
        [2, 3],
        [6, 1]
    ]
    cols = [
        [5, 1], [4, 1], [2, 3], [8, 1], [6, 0]
    ]

    og_rows = copy.deepcopy(rows)
    og_cols = copy.deepcopy(cols)

    # Add the number of spaces remaining
    rows = [row + [len(cols)] for row in rows]
    cols = [col + [len(rows)] for col in cols]

    iterate_through(grid, rows, cols, og_rows, og_cols)


if __name__ == '__main__':
    all_possible = []
    main()
