
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


def read(filepath):
    with open(filepath) as f:
        pass
    return elements


table = [3, 7]
elves_pos = [0, 1]


def solve(_input):

    for i, window in enumerate(windowed(table, len(_input))):
        if list(window) == _input:
            return i

    while True:
        s = sum(table[e] for e in elves_pos)
        if s >= 10:
            table.append((s // 10) % 10)
        table.append(s % 10)

        for elf_idx in range(len(elves_pos)):
            pos = elves_pos[elf_idx]
            pos += 1 + table[pos]
            pos %= len(table)
            elves_pos[elf_idx] = pos
        # print(' '.join(
        #     f'({r})' if r_idx == elves_pos[0] else (f'[{r}]' if r_idx == elves_pos[1] else f'{r:^3}')
        #     for r_idx, r in enumerate(table)
        # ))
        # print(table)
        # print(elves_pos)

        print(_input, table[len(table) - len(_input) - 1: len(table) - 1])
        if _input == table[len(table) - len(_input) - 1: len(table) - 1]:
            return len(table) - len(_input) - 1
        if _input == table[len(table) - len(_input):]:
            return len(table) - len(_input)


def main():
    tests = [
        # ('pb00_input00.txt', 17, ),
        # (9, '5158916779', ),
        # (5, '0124515891', ),
        # (18, '9251071085', ),
        # (2018, '5941429882', ),
        # (760221, '0000', ),

        ([5, 1, 5, 8, 9, ], 9, ),
        ([0, 1, 2, 4, 5, ], 5, ),
        ([9, 2, 5, 1, 0, ], 18, ),
        ([5, 9, 4, 1, 4, ], 2018, ),
        ([7, 6, 0, 2, 2, 1, ], 0, ),
    ]
    for test, expected in tests:
        # graph = read(test)
        res = solve(test)
        print(test, expected, res)

    # test = 'pb00_input01.txt'
    # graph = read(test)
    # result = solve(graph)
    # print(result)


__name__ == '__main__' and main()
