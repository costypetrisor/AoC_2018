
import collections
import datetime
import functools
import itertools
import json
import re

from more_itertools import windowed



def read(filepath):
    with open(filepath) as f:
        return f.read().strip()



def solve(polymer):
    polymer = list(polymer)
    while True:
        altered = False
        l = len(polymer) - 1
        i = 0
        while i < l:
            if (polymer[i].upper() == polymer[i + 1] and polymer[i] != polymer[i].upper()) or (polymer[i].lower() == polymer[i + 1] and polymer[i] != polymer[i].lower()):
                # if i > 3 and i < l  - 4:
                #     _s = ''.join(polymer[i - 2: i + 4])
                # else:
                #     _s = ''.join(polymer[i - 2:])
                altered = True
                # print('reacting  %s with %s  l=%s' % (polymer[i], polymer[i + 1], l))
                del polymer[i]
                del polymer[i]
                l -= 2
                # if i > 3 and i < l - 2:
                #     _s2 = ''.join(polymer[i - 2: i + 3])
                #     print(_s, _s2)
                # else:
                #     _s2 = ''.join(polymer[i - 2:])
                #     print(_s, _s2)
                i -= 1
            else:
                i += 1
        break
        if not altered:
            break
    return ''.join(polymer)


def main():
    tests = {
        'dabAcCaCBAcCcaDA': 'dabCBAcaDA',

    }
    for test, expected in tests.items():
        res = solve(test)
        print(test, expected, res, len(res))

    input_00 = read('pb00_input00.txt')
    print(len(input_00))
    result_00 = solve(input_00)
    print('"%s"' % (result_00))
    print(len(result_00))




__name__ == '__main__' and main()
