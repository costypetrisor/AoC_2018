
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


def solve(_input):
    nb_players, max_marble = _input

    score_table = {i: 0 for i in range(nb_players)}

    circle = [0, ]
    last_marble_idx = 0

    # player_cycler = itertools.cycle(range(1, nb_players + 1))
    player = -1

    for marble in range(1, max_marble + 1):
        # player = next(player_cycler)
        player += 1
        player %= nb_players

        if marble == 1:
            circle.append(marble)
            last_marble_idx = 1
            continue

        is_23_multiple = (marble % 23) == 0

        if is_23_multiple:
            score_table[player] += marble
            last_marble_idx -= 7
            while last_marble_idx < 0:
                last_marble_idx += len(circle)
            marble_removed = circle[last_marble_idx]
            del circle[last_marble_idx]
            last_marble_idx %= len(circle)
            score_table[player] += marble_removed
        else:
            new_marble_idx = (last_marble_idx + 2) % len(circle)
            circle.insert(new_marble_idx, marble)
            last_marble_idx = new_marble_idx

        # print(marble, last_marble_idx, circle)
        # print('[%s] %s (%s) %s' % (
        #     player, ' '.join(map(str, circle[:last_marble_idx])), circle[last_marble_idx], ' '.join(map(str, circle[last_marble_idx + 1:])) if last_marble_idx + 1 < len(circle) else '' ))

    # pprint(score_table)
    winner = sorted(score_table.items(), key=lambda e: e[1], reverse=True)
    return winner[0]


def main():
    tests = [
        # ('pb00_input00.txt', 17, ),
        ((9, 25, ), 32, ),
        ((10, 1618, ), 8317, ),
        ((13, 7999, ), 146373, ),
        ((17, 1104, ), 2764, ),
        ((21, 6111, ), 54718, ),
        ((30, 5807, ), 37305, ),
    ]
    for test, expected in tests:
        # graph = read(test)
        res = solve(test)
        print(test, expected, res)

    # test = 'pb00_input01.txt'
    # graph = read(test)
    result = solve((458, 71307, ))
    print(result)

    result = solve((458, 71307 * 100, ))
    print(result)


__name__ == '__main__' and main()
