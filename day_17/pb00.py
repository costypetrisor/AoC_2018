
import collections
import datetime
import functools
import itertools
import json
import math
from pprint import pformat, pprint
import re
import sys
import time

from more_itertools import windowed


def read(filepath):
    grid = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            grid.append(line)
    return (grid, )


def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print('')


def solve(grid):
    grid = [list(row) for row in grid]
    original_grid = grid
    width, height = len(grid[0]), len(grid)
    print_grid(original_grid)

    for minute in range(10):
        new_grid = []
        for row_idx in range(height):
            row = list(grid[row_idx])
            for col_idx in range(width):
                adjiacent_open = 0
                adjiacent_trees = 0
                adjiacent_lumberyards = 0
                for offset_x, offset_y in itertools.product((-1, 0, 1), (-1, 0, 1)):
                    if offset_x == 0 and offset_y == 0:
                        continue
                    x = row_idx + offset_x
                    y = col_idx + offset_y
                    if x < 0 or y < 0 or x >= height or y >= width:
                        continue
                    if grid[x][y] == '.':
                        adjiacent_open += 1
                    elif grid[x][y] == '|':
                        adjiacent_trees += 1
                    elif grid[x][y] == '#':
                        adjiacent_lumberyards += 1

                current_land = grid[row_idx][col_idx]
                if current_land == '.':
                    if adjiacent_trees >= 3:
                        row[col_idx] = '|'
                elif current_land == '|':
                    if adjiacent_lumberyards >= 3:
                        row[col_idx] = '#'
                elif current_land == '#':
                    if not (adjiacent_lumberyards >= 1 and adjiacent_trees >= 1):
                        row[col_idx] = '.'

            new_grid.append(row)
        grid = new_grid
        print_grid(grid)

    open_count = trees_count = lumberyards_count = 0
    for row_idx in range(height):
        for col_idx in range(width):
            current_land = grid[row_idx][col_idx]
            if current_land == '.':
                open_count += 1
            elif current_land == '|':
                trees_count += 1
            elif current_land == '#':
                lumberyards_count += 1

    return trees_count * lumberyards_count


def main():
    # tests = [
    #     ('pb00_input00.txt', 1147, ),
    # ]
    # for test, expected in tests:
    #     _input = read(test)
    #     res = solve(*_input)
    #     print(test, expected, res)

    test = 'pb00_input01.txt'
    _input = read(test)
    result = solve(*_input)
    print(result)


__name__ == '__main__' and main()
