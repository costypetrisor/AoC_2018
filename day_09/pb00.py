
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
    points = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                # position=<-3,  6> velocity=< 2, -1>
                m = re.search(r'(?i)position=<\s*(?P<pX>-?\d+)\s*,\s*(?P<pY>-?\d+)\s*> velocity=<\s*(?P<vX>-?\d+)\s*,\s*(?P<vY>-?\d+)\s*>', line)
                if not m:
                    raise Exception(line)
                gd = m.groupdict()
                pX, pY, vX, vY = int(m.group('pX')), int(m.group('pY')), int(m.group('vX')), int(m.group('vY'))
                points.append((pX, pY, vX, vY))
    return points


def advance_points(points):
    return [(pX + vX, pY + vY, vX, vY) for pX, pY, vX, vY in points]


def display(points):
    min_x = min_y = sys.maxsize
    max_x = max_y = -sys.maxsize
    for pX, pY, _, _ in points:
        if pX < min_x:
            min_x = pX
        if pX > max_x:
            max_x = pX
        if pY < min_y:
            min_y = pY
        if pY > max_y:
            max_y = pY

    print('max_x, max_y, min_y, max_y, max_x - min_x, max_y - min_y', max_x, max_y, min_y, max_y, max_x - min_x, max_y - min_y)

    if not ((max_x - min_x) < 500 and (max_y - min_y) < 200):
        return

    matrix = [['.' for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
    # matrix = [['.' for _ in range(max_y - min_y + 1)] for _ in range(max_x - min_x + 1)]

    for pX, pY, _, _ in points:
        # print(pX, pY)
        pX -= min_x
        pY -= min_y
        # pX += min_x
        # pY += min_y
        try:
            matrix[pY][pX] = '#'
            # matrix[pX][pY] = '#'
        except IndexError:
            print('pX, pY, pX - min_x, pY - min_y', pX, pY, pX - min_x, pY - min_y)
            raise

    for line in matrix:
        print(''.join(line))
    print('')
    time.sleep(0.5)


def solve(points):
    print(points)
    initial_points = points
    display(points)

    i = 0
    while True:
        i += 1
        print('t=%s' % (i, ))
        points = advance_points(points)
        display(points)



def main():
    tests = [
        ('pb00_input00.txt', 17, ),
    ]
    for test, expected in tests:
        points = read(test)
        res = solve(points)
        print(test, expected, res)

    # test = 'pb00_input01.txt'
    # graph = read(test)
    # result = solve(graph)
    # print(result)


__name__ == '__main__' and main()
