import copy


def display(grid: list[list[str]]) -> None:
    for row in grid:
        print(row)


def check_for_no_bombs(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]]) -> None:
    """Checks if any rows or column contain no bombs - indicating they should reveal all the spaces left"""
    for r, row in enumerate(rows):
        if row[1] == 0:
            grid[r] = ['_' if val.startswith('B/') else val for val in grid[r]]
            display(grid)
            exit(0)

    for c, col in enumerate(cols):
        if col[1] == 0:
            for r in range(len(rows)):
                grid[r][c] = '_'
            display(grid)
            exit(0)


def update_rows_cols(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]]) -> None:
    """Reduces the point and bomb numbers of row and columns by the points and bombs we know of"""
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val.isdigit():
                rows[r][0] -= int(val)
                cols[c][0] -= int(val)

            elif val == 'B/':
                grid[r][c] = 'B'
                rows[r][1] -= 1
                cols[c][1] -= 1
                rows[r][2] -= 1
                cols[c][2] -= 1
                check_for_no_bombs(grid, rows, cols)


def is_valid_points_spaces(points: int, spaces: int, low: int = 1, high: int = 3) -> bool:
    return (points / spaces >= low) and (points / spaces <= high)


def find_possible_values(points: int, spaces: int, index: int, line: str,  low: int = 1, high: int = 3) -> list[str]:
    """Determines the possible values a space can have from the points and spaces left in that line"""
    if spaces == 0:
        return []

    if not is_valid_points_spaces(points, spaces, low, high):
        raise ValueError(f"Invalid State at {line} {index+1}: {points=}, {spaces=}, {low=}, {high=}")

    if spaces == 1:
        return [str(points)]

    return [str(val) for val in range(low, high + 1) if is_valid_points_spaces(points - val, spaces - 1, low, high)]


def val_checker(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]]):
    """Inputs what values are possible at each point in the grid"""
    for r, row in enumerate(rows):
        points = row[0]
        spaces = row[2] - row[1]
        possible_vals = find_possible_values(points, spaces, index=r, line='row')
        for c, val in enumerate(grid[r]):
            if val == '?':
                grid[r][c] = 'B/' + '/'.join(possible_vals)
            elif val.isdigit() or val == 'B':
                pass
            else:
                old_vals = val.split('/')
                grid[r][c] = 'B/' + '/'.join(set(old_vals).intersection(possible_vals))

    for c, col in enumerate(cols):
        points = col[0]
        spaces = len(rows) - col[1]
        possible_vals = find_possible_values(points, spaces, index=c, line='col')
        for r_i in range(len(rows)):
            val = grid[r_i][c]
            if grid[r_i][c] == '?':
                grid[r_i][c] = 'B/' + '/'.join(possible_vals)
            elif val.isdigit() or val == 'B':
                pass
            else:
                old_vals = val.split('/')
                grid[r_i][c] = 'B/' + '/'.join(set(old_vals).intersection(possible_vals))


    display(grid)
    print('=================================================')


def iterate_through(grid: list[list[str]], rows: list[list[int]], cols: list[list[int]]):
    # Add the number of spaces remaining
    rows = [row + [len(cols)] for row in rows]
    cols = [col + [len(rows)] for col in cols]

    before = copy.deepcopy(grid)

    # Do this first so we update the rows and values with points we already know
    update_rows_cols(grid, rows, cols)
    check_for_no_bombs(grid, rows, cols)
    val_checker(grid, rows, cols)

    while before != grid:
        before = copy.deepcopy(grid)
        update_rows_cols(grid, rows, cols)
        check_for_no_bombs(grid, rows, cols)
        val_checker(grid, rows, cols)



def main():
    grid = [
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?'],
        ['?', '?', '?', '?', '?']
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

    iterate_through(grid, rows, cols)


if __name__ == '__main__':
    main()
