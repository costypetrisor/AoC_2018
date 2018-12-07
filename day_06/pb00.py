
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
    all_states = set()
    graph = collections.defaultdict(set)
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                m = re.search(r'Step (?P<dependency>[\S+]) must be finished before step (?P<dependent>[\S+]) can begin.', line)
                if m:
                    # print(m.groupdict())
                    all_states.add(m.group('dependent'))
                    all_states.add(m.group('dependency'))
                    graph[m.group('dependent')].add(m.group('dependency'))
                else:
                    print('failed to match: ', line)
    return dict(graph), all_states


def solve(_input):
    graph, all_states = _input
    print(graph)

    ordering = []

    starting_states = sorted(all_states - set(graph.keys()))
    ordering.append(starting_states[0])
    # print('initial_add: ', ordering)

    added_states = set(ordering)
    remaining_states = sorted(all_states - added_states)

    while remaining_states:
        # for state, dependencies in sorted(graph.keys())):
        possibles = set()
        for state in remaining_states:
            dependencies = graph.get(state, set())
            if dependencies.issubset(added_states):
                possibles.add(state)
        if not possibles:
            raise Exception("impossible")
        possibles = sorted(possibles)
        # print('possibles: %s' % (possibles, ))
        for state in possibles[:1]:
            ordering.append(state)
            # print(ordering)
            remaining_states.remove(state)
            added_states.add(state)

    print(''.join(ordering))



def main():
    tests = [
        ('pb00_input00.txt', 17, ),
    ]
    for test, expected in tests:
        graph = read(test)
        res = solve(graph)
        print(test, expected, res)

    test = 'pb00_input01.txt'
    graph = read(test)
    result = solve(graph)
    print(result)


__name__ == '__main__' and main()
