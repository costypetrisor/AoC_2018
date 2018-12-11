
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

# import pyximport; 
# pyximport.install()

# from pb01_cython import solve


def print_grid(grid):
    for row in grid:
        print(' '.join('%3s' % v for v in row))


def solve_py(serial_number):
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
    cell_value = None
    for cell_size in range(1, 301):
        cell_value = None
        for row_idx in range(300 - cell_size):
            cell_value = None
            for col_idx in range(300 - cell_size):
                if cell_value is None:
                    cell_value = 0
                    for i in range(cell_size):
                        for j in range(cell_size):
                            cell_value += grid[row_idx + i][col_idx + j]
                else:
                    for i in range(cell_size):
                        cell_value -= grid[row_idx + i][col_idx - 1]
                        cell_value += grid[row_idx + i][col_idx + cell_size - 1]
                if cell_value > max_cell_value:
                    max_cell_id = (row_idx, col_idx, cell_size)
                    max_cell_value = cell_value

    # print_grid([grid[max_cell_id[0] + r][max_cell_id[1] - 1:max_cell_id[1] + 4] for r in range(-1, 4)])

    return max_cell_id


# solve_func = solve
solve_func = solve_py


def main():
    tests = [
        (18, (90,269,16), ),
        (42, (232,251,12), ),
    ]
    for test, expected in tests:
        res = solve_func(test)
        print(test, expected, res)

    result = solve_func(4172)
    print(result)


if __name__ == '__main__':
    main()
