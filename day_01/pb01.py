
import collections
import itertools
import difflib
import re


def solve(list_of_ids):
    for a, b in itertools.combinations(list_of_ids, 2):
        diffs = []
        idx = 0
        for la, lb in zip(a, b):
            if la != lb:
                diffs.append(idx)
            idx += 1
        if len(diffs) == 1:
            return a[: diffs[0]] + a[diffs[0] + 1:]



def main():
    list_of_ids = [
        'abcde',
        'fghij',
        'klmno',
        'pqrst',
        'fguij',
        'axcye',
        'wvxyz',
    ]
    common = solve(list_of_ids)
    print(common)

    with open('pb00_input.txt') as f:
        list_of_ids = [e.strip() for e in f.readlines() if e.strip()]
    checksum = solve(list_of_ids)
    print(checksum)


__name__ == '__main__' and main()

