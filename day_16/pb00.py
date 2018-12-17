
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


ClayPatch = collections.namedtuple('ClayPatch', 'x,y')


def read(filepath):
    clay_patches = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            elems = dict(e.strip().split('=') for e in line.split(','))
            elems = {k: tuple(v.split('..', 1)) if '..' in v else (v, v) for k, v in elems.items()}
            elems = {k: (int(v[0]), int(v[1])) for k, v in elems.items()}
            clay_patch = ClayPatch(**elems)
            assert clay_patch.x[0] <= clay_patch.x[1]
            assert clay_patch.y[0] <= clay_patch.y[1]
            clay_patches.append(clay_patch)
    return (clay_patches, )


def print_grid(grid, range_current_point=None):
    if range_current_point:
        for line in grid[range_current_point[1] - range_current_point[3]: range_current_point[1] + range_current_point[3]]:
            print(''.join(line[range_current_point[0] - range_current_point[2]: range_current_point[0] + range_current_point[2]]))
    else:
        for line in grid:
            print(''.join(line))
    print('')


def drip_down(grid, current_pos):
    print(f'drip_down current_pos={current_pos}')
    print_grid(grid,range_current_point=current_pos + (20, 5))
    while True:
        next_pos = (current_pos[0], current_pos[1] + 1)
        if grid[next_pos[1]][next_pos[0]] in ('.', '|', ):
            grid[next_pos[1]][next_pos[0]] = '|'
            current_pos = next_pos
        else:
            break

    drip_horizontally(grid, current_pos)  # ???
    spread_and_fill(grid, current_pos)


def spread_and_fill(grid, current_pos):
    ##
    if current_pos[0] == 165 and current_pos[1] == 30:
        _x = 0
    ##
    if current_pos[1] == len(grid[1]):
        return
    print(f'spread_and_fill current_pos={current_pos}')
    print_grid(grid,range_current_point=current_pos + (20, 5))
    leaks = False

    while not leaks:
        left_bound = current_pos
        while True:
            next_left_bound = (left_bound[0] - 1, left_bound[1])
            try:
                if next_left_bound[0] < 0:
                    leaks = True
                    break
                if grid[next_left_bound[1]][next_left_bound[0]] == '#':
                    break
                if grid[next_left_bound[1] + 1][next_left_bound[0]] == '#' and grid[next_left_bound[1] + 1][next_left_bound[0] - 1] in ('.', '|', ):
                    leaks = True
                    drip_horizontally(grid, current_pos)
                    break
            except IndexError:
                leaks = True
                break
            left_bound = next_left_bound
        width = len(grid[0])
        right_bound = current_pos
        while True:
            next_right_bound = (right_bound[0] + 1, right_bound[1])
            try:
                if next_right_bound[0] >= width:
                    leaks = True
                    break
                if grid[next_right_bound[1]][next_right_bound[0]] == '#':
                    break
                if grid[next_right_bound[1] + 1][next_right_bound[0]] == '#' and grid[next_right_bound[1] + 1][next_right_bound[0] + 1] in ('.', '|', ):
                    leaks = True
                    drip_horizontally(grid, current_pos)
                    break
            except IndexError:
                leaks = True
                break
            right_bound = next_right_bound

        if not leaks:
            print(f'  spread_and_fill filling ~ from {left_bound[0]},{current_pos[1]} to {right_bound[0]},{current_pos[1]} inclusive')
            for x in range(left_bound[0], right_bound[0] + 1):
                grid[current_pos[1]][x] = '~'

            if current_pos[1] - 1 >= 0:
                current_pos = (current_pos[0], current_pos[1] - 1)
                # spread_and_fill(grid, (current_pos[0], current_pos[1] - 1))
                # # for x in range(left_bound[0], right_bound[0] + 1):
                # #     spread_and_fill(grid, (x, current_pos[1] - 1))


def drip_horizontally(grid, current_pos):
    ##
    if current_pos[0] == 165 and current_pos[1] == 30:
        _x = 0
    ##
    print(f'drip_horizontally current_pos={current_pos}')
    print_grid(grid,range_current_point=current_pos + (20, 5))
    assert grid[current_pos[1]][current_pos[0]] != '#'
    grid[current_pos[1]][current_pos[0]] = '|'

    left_cursor = current_pos
    drip_down_left = False
    while True:
        left_cursor = (left_cursor[0] - 1, left_cursor[1])
        if left_cursor[0] < 0:
            drop_down_left = True
            break
        try:
            if grid[left_cursor[1]][left_cursor[0]] != '#':
                grid[left_cursor[1]][left_cursor[0]] = '|'
            else:
                break
            if grid[left_cursor[1] + 1][left_cursor[0]] == '|':
                break
            if grid[left_cursor[1] + 1][left_cursor[0]] == '.':
                drip_down_left = True
                drip_down(grid, left_cursor)
                break
        except IndexError:
            break

    width = len(grid[0])
    right_cursor = current_pos
    drip_down_right = False
    while True:
        right_cursor = (right_cursor[0] + 1, right_cursor[1])
        if right_cursor[0] >= width:
            drip_down_right = True
            break
        try:
            if grid[right_cursor[1]][right_cursor[0]] != '#':
                grid[right_cursor[1]][right_cursor[0]] = '|'
            else:
                break
            if grid[right_cursor[1] + 1][right_cursor[0]] == '|':
                break
            if grid[right_cursor[1] + 1][right_cursor[0]] == '.':
                drip_down_right = True
                drip_down(grid, right_cursor)
                break
        except IndexError:
            break

    # if ((not drip_down_left or (drip_down_left and grid[left_cursor[1] + 1][left_cursor[0]] == '~'))
    #         and (not drip_down_right or (drip_down_right and grid[right_cursor[1] + 1][right_cursor[0]] == '~'))):
    if ((drip_down_left and grid[left_cursor[1] + 1][left_cursor[0]] == '~')
            or (drip_down_right and grid[right_cursor[1] + 1][right_cursor[0]] == '~')):
        print(f'    drip_horizontally drip_down_left_right={drip_down_left},{drip_down_right} AND it was filled')
        # print_grid(grid)
        spread_and_fill(grid, current_pos)
    else:
        print(f'    drip_horizontally drip_down_left_right={drip_down_left},{drip_down_right} AND NOTHING was filled')


def solve(clay_patches_orig):
    well = (500, 0)

    min_x = sys.maxsize
    max_x = -sys.maxsize
    min_y = sys.maxsize
    max_y = -sys.maxsize
    for cp in clay_patches_orig:
        if cp.x[0] < min_x:
            min_x = cp.x[0]
        if cp.x[1] > max_x:
            max_x = cp.x[1]
        if cp.y[0] < min_y:
            min_y = cp.y[0]
        if cp.y[1] > max_y:
            max_y = cp.y[1]
    size_x, size_y = (max_x - min_x + 2), (max_y - min_y + 1)
    print(f'minmax_x={min_x}..{max_x}  minmax_y={min_y}..{max_y}  size={size_x}x{size_y}')

    well = (well[0] - min_x, well[1])

    grid = [['.' for _ in range(size_x)] for _ in range(size_y)]

    clay_patches = [
        ClayPatch(
            x=(cp.x[0] - min_x + 1, cp.x[1] - min_x + 1),
            y=(cp.y[0] - min_y, cp.y[1] - min_y),
        )
        for cp in clay_patches_orig
    ]

    for cp in clay_patches:
        for x in range(cp.x[0], cp.x[1] + 1):
            for y in range(cp.y[0], cp.y[1] + 1):
                grid[y][x] = '#'
    # print_grid(grid)

    grid[well[1]][well[0]] = '|'
    drip_down(grid, well)

    water_at_rest_count = 0
    dripped_count = 0
    for y in range(size_y):
        for x in range(size_x):
            v = grid[y][x]
            if v == '~':
                water_at_rest_count += 1
            elif v == '|':
                dripped_count += 1

    print_grid(grid)
    print(f'Water at rest: {water_at_rest_count}  dripped: {dripped_count}.  Sum: {water_at_rest_count + dripped_count}')
    return water_at_rest_count + dripped_count


def main():
    tests = [
        ('pb00_input00.txt', 57, ),
    ]
    for test, expected in tests:
        _input = read(test)
        res = solve(*_input)
        print(test, expected, res)

    test = 'pb00_input01.txt'
    _input = read(test)
    result = solve(*_input)
    print(result)


__name__ == '__main__' and main()
