
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
        line = f.readline().strip()
        elements = line.split()
        elements = [int(e.strip()) for e in elements]
    return elements


class Node(object):

    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def sum(self):
        return sum(self.metadata) + sum(c.sum() for c in self.children)

    def value(self):
        if not self.children:
            return sum(self.metadata)
        else:
            V = 0
            for m in self.metadata:
                m -= 1
                if m < len(self.children):
                    V += self.children[m].value()
            return V


def make_tree(elements):
    if len(elements) < 2:
        raise Exception
    nb_children = elements[0]
    nb_meta = elements[1]
    kids = []
    elem_idx = 2
    for kid_idx in range(nb_children):
        kid, consumed = make_tree(elements[elem_idx:])
        elem_idx += consumed
        kids.append(kid)
    metadata = list(elements[elem_idx: elem_idx + nb_meta])
    elem_idx += nb_meta
    node = Node(kids, metadata)
    return node, elem_idx


def solve(_input):
    root, _consumed = make_tree(_input)
    assert _consumed == len(_input)

    s = root.sum()
    print('Sum: %s' % (s))

    v = root.value()
    print('Value: %s' % (v))



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
