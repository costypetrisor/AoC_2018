
import collections
import dataclasses
import datetime
import enum
import functools
import itertools
import json
import math
from pprint import pformat, pprint
import re
import sys
from typing import Iterator, List, Tuple

from more_itertools import peekable, windowed


@enum.unique
class CartDirection(enum.Enum):
    UP = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT = '>'


@enum.unique
class CartDecision(enum.Enum):
    TAKE_LEFT = 1
    GO_STRAIGHT = 2
    TAKE_RIGHT = 3


def read(filepath):
    grid = []
    with open(filepath) as f:
        for line in f:
            line = line.rstrip('\n')
            if len(line):
                grid.append(line)
    return grid


class Cart:
    def __init__(self, position: List[int], direction: str):
        self.position = position
        self.direction = direction
        self.turn_decision: Iterator = peekable(itertools.cycle(CartDecision))

    def __repr__(self):
        return f'Cart(position={self.position}, direction={self.direction!r}, next_turn_decision={self.turn_decision.peek().name}'

    def next_position(self):
        new_position = list(self.position)
        if self.direction == CartDirection.UP.value:
            new_position[0] -= 1
        elif self.direction == CartDirection.DOWN.value:
            new_position[0] += 1
        elif self.direction == CartDirection.LEFT.value:
            new_position[1] -= 1
        elif self.direction == CartDirection.RIGHT.value:
            new_position[1] += 1
        else:
            raise Exception(f'unknown facing direction: {self.direction!r}')
        return new_position

    INVALID_NEXT_DIRECTION = object()
    _next_direction_map = {
        CartDirection.UP.value: {
            '/': CartDirection.RIGHT.value,
            '-': INVALID_NEXT_DIRECTION,
            '\\': CartDirection.LEFT.value,
            '|': CartDirection.UP.value,
        },
        CartDirection.DOWN.value: {
            '/': CartDirection.LEFT.value,
            '-': INVALID_NEXT_DIRECTION,
            '\\': CartDirection.RIGHT.value,
            '|': CartDirection.DOWN.value,
        },
        CartDirection.LEFT.value: {
            '/': CartDirection.DOWN.value,
            '-': CartDirection.LEFT.value,
            '\\': CartDirection.UP.value,
            '|': INVALID_NEXT_DIRECTION,
        },
        CartDirection.RIGHT.value: {
            '/': CartDirection.UP.value,
            '-': CartDirection.RIGHT.value,
            '\\': CartDirection.DOWN.value,
            '|': INVALID_NEXT_DIRECTION,
        },
    }

    def next_direction(self, new_track):
        next_dir = self._next_direction_map[self.direction][new_track]
        if next_dir is self.INVALID_NEXT_DIRECTION:
            raise Exception(f"Invalid next direction for current direction {self.direction!r} and new track {new_track!r}")
        return next_dir

    _next_direction_for_turn_decision_map = {
        CartDirection.UP.value: {
            CartDecision.TAKE_LEFT: CartDirection.LEFT.value,
            CartDecision.GO_STRAIGHT: CartDirection.UP.value,
            CartDecision.TAKE_RIGHT: CartDirection.RIGHT.value,
        },
        CartDirection.DOWN.value: {
            CartDecision.TAKE_LEFT: CartDirection.RIGHT.value,
            CartDecision.GO_STRAIGHT: CartDirection.DOWN.value,
            CartDecision.TAKE_RIGHT: CartDirection.LEFT.value,
        },
        CartDirection.LEFT.value: {
            CartDecision.TAKE_LEFT: CartDirection.DOWN.value,
            CartDecision.GO_STRAIGHT: CartDirection.LEFT.value,
            CartDecision.TAKE_RIGHT: CartDirection.UP.value,
        },
        CartDirection.RIGHT.value: {
            CartDecision.TAKE_LEFT: CartDirection.UP.value,
            CartDecision.GO_STRAIGHT: CartDirection.RIGHT.value,
            CartDecision.TAKE_RIGHT: CartDirection.DOWN.value,
        },
    }

    def next_direction_for_turn_decision(self, turn_decision):
        return self._next_direction_for_turn_decision_map[self.direction][turn_decision]



def _find_carts(grid):
    carts = []
    cart_types = set([e.value for e in CartDirection])
    for row_idx, row in enumerate(grid):
        for col_idx in range(len(row)):
            c = row[col_idx]
            if c in cart_types:
                cart = Cart(position=[row_idx, col_idx], direction=c)
                carts.append(cart)
    return carts


def _replace_carts(grid):
    replacement_track = {
        CartDirection.UP: '|',
        CartDirection.DOWN: '|',
        CartDirection.LEFT: '-',
        CartDirection.RIGHT: '-',
    }
    new_grid = []
    for line in grid:
        for direction in CartDirection:
            line = line.replace(direction.value, replacement_track[direction])
        new_grid.append(line)
    return new_grid


def _print_grid(grid):
    for line in grid:
        print(line)


def _print_grid_with_carts(grid, carts):
    grid = list(grid)
    for cart in carts:
        row = grid[cart.position[0]]
        row = row[:cart.position[1]] + cart.direction + row[cart.position[1] + 1:]
        grid[cart.position[0]] = row
    _print_grid(grid)


def _check_collisions(carts: List[Cart]):
    positions = collections.defaultdict(list)
    for cart in carts:
        positions[tuple(cart.position)].append(cart)
    # print(positions)
    collisions = []
    for position, collided_carts in positions.items():
        if len(collided_carts) > 1:
            collisions.append(collided_carts)
    # print(collisions)
    return collisions


def solve(grid):
    _orig_grid = grid
    _print_grid(_orig_grid)

    carts = _find_carts(grid)
    grid = _replace_carts(grid)

    _crash_at = None
    while not _crash_at:
        carts = sorted(carts, key=lambda c: c.position)
        print(carts)
        # _print_grid(grid)
        _print_grid_with_carts(grid, carts)

        for cart in carts:
            new_position = cart.next_position()
            new_track = grid[new_position[0]][new_position[1]]
            if new_track == '+':
                turn_decision = next(cart.turn_decision)
                new_direction = cart.next_direction_for_turn_decision(turn_decision)
            else:
                new_direction = cart.next_direction(new_track)

            print(f'Cart {cart.position} {cart.direction!r}  =>  {new_position} {new_direction!r}')
            cart.position = new_position
            cart.direction = new_direction

            collisions = _check_collisions(carts)
            if collisions:
                # print(collections)
                _crash_at = collisions[0][0].position
    return list(reversed(_crash_at))




def main():
    tests = [
        ('pb00_input00.txt', (7, 3, ), ),
    ]
    for test, expected in tests:
        grid = read(test)
        res = solve(grid)
        print(test, expected, res)

    test = 'pb00_input01.txt'
    graph = read(test)
    result = solve(graph)
    print(result)


__name__ == '__main__' and main()
