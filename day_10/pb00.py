
import collections
import datetime
import functools
import itertools
import json
import math
from pprint import pformat, pprint
import re
import sys

from more_itertools import windowed


def print_grid(grid):
    for row in grid:
        print(' '.join('%3s' % v for v in row))


def solve(serial_number):
    grid = [[0 for _ in range(300)] for _ in range(300)]
    for col_idx, row_idx in itertools.product(range(300), range(300)):
        rack_id = row_idx + 10
        power_level = rack_id * col_idx
        power_level += serial_number
        power_level *= rack_id
        power_level = int(power_level / 100) % 10
        power_level -= 5
        grid[row_idx][col_idx] = power_level

    # print_grid(grid)

    max_cell_id = None
    max_cell_value = -sys.maxsize
    for col_idx, row_idx in itertools.product(range(300 - 3), range(300 - 3)):
        cell_value = 0
        for i, j in itertools.product(range(3), range(3)):
            cell_value += grid[row_idx + i][col_idx + j]
        if cell_value > max_cell_value:
            max_cell_id = (row_idx, col_idx)
            max_cell_value = cell_value

    print_grid([grid[max_cell_id[0] + r][max_cell_id[1] - 1:max_cell_id[1] + 4] for r in range(-1, 4)])

    return max_cell_id


def main():
    tests = [
        (18, (33, 45, ), ),
        (42, (21, 61, ), ),
    ]
    for test, expected in tests:
        res = solve(test)
        print(test, expected, res)

    result = solve(4172)
    print(result)


__name__ == '__main__' and main()
