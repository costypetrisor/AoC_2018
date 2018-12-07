
import collections
import datetime
import functools
import itertools
import json
import math
import re
import sys

from more_itertools import windowed


def md(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def solve(points):
    max_x = max_y = -sys.maxsize
    for p in points:
        if p[0] > max_x:
            max_x = p[0]
        if p[1] > max_y:
            max_y = p[1]
    max_x += 1
    max_y += 1
    print('max_x, max_y =', max_x, max_y)

    grid = [['.' for _y in range(max_y)] for _x in range(max_x)]
    # print(len(grid), len(grid[0]))
    # print(grid)
    for p_idx, p in enumerate(points):
        print(p)
        grid[p[0]][p[1]] = chr(ord('A') + p_idx)

    point_closest_dests = collections.defaultdict(set)

    unbounded_points = set()

    for x in range(max_x):
        for y in range(max_y):
            distances = []
            for p_idx, p in enumerate(points):
                d = md(p, (x, y))
                distances.append((p_idx, d))
            distances = sorted(distances, key=lambda e: e[1])
            is_boundary = x == 0 or y == 0 or x == (max_x - 1) or y == (max_y - 1)
            if distances[0][1] == distances[1][1]:
                pass
            else:
                p_idx = distances[0][0]
                if is_boundary:
                    unbounded_points.add(p_idx)
                point_closest_dests[p_idx].add((x, y))
                if grid[x][y] == '.':
                    grid[x][y] = chr(ord('a') + p_idx)

    for unbounded_point in unbounded_points:
        del point_closest_dests[unbounded_point]
    point_closest_dests = sorted(point_closest_dests.items(), key=lambda e: len(e[1]), reverse=True)
    print('Winning point id: %s  with closes points %s' % (point_closest_dests[0][0], sorted(point_closest_dests[0][1])))
    # for line in grid:
    #     print(''.join(line))
    return len(point_closest_dests[0][1])


def main():
    tests = [
        ([
            (1, 1, ),
            (1, 6, ),
            (8, 3, ),
            (3, 4, ),
            (5, 5, ),
            (8, 9, ),
        ], 17, ),
    ]
    for test, expected in tests:
        res = solve(test)
        print(test, expected, res)

    test = [
        (61, 90, ),
        (199, 205, ),
        (170, 60, ),
        (235, 312, ),
        (121, 290, ),
        (62, 191, ),
        (289, 130, ),
        (131, 188, ),
        (259, 82, ),
        (177, 97, ),
        (205, 47, ),
        (302, 247, ),
        (94, 355, ),
        (340, 75, ),
        (315, 128, ),
        (337, 351, ),
        (73, 244, ),
        (273, 103, ),
        (306, 239, ),
        (261, 198, ),
        (355, 94, ),
        (322, 69, ),
        (308, 333, ),
        (123, 63, ),
        (218, 44, ),
        (278, 288, ),
        (172, 202, ),
        (286, 172, ),
        (141, 193, ),
        (72, 316, ),
        (84, 121, ),
        (106, 46, ),
        (349, 77, ),
        (358, 66, ),
        (309, 234, ),
        (289, 268, ),
        (173, 154, ),
        (338, 57, ),
        (316, 95, ),
        (300, 279, ),
        (95, 285, ),
        (68, 201, ),
        (77, 117, ),
        (313, 297, ),
        (259, 97, ),
        (270, 318, ),
        (338, 149, ),
        (273, 120, ),
        (229, 262, ),
        (270, 136, ),
    ]
    result = solve(test)
    print(result)




__name__ == '__main__' and main()
