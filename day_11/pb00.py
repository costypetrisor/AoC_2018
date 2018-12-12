
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
        initial_state_line = f.readline().strip()
        initial_state = initial_state_line[max(0, min(initial_state_line.index('.'), initial_state_line.index('#'))):]

        conditions = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            condition = tuple(e.strip() for e in line.split('=>', 1))
            condition = (tuple(condition[0]), condition[1])
            conditions.append(condition)

    # print(initial_state, conditions)
    return initial_state, conditions


def solve(_input):
    initial_state, conditions = _input
    conditions_dict = dict(conditions)

    state = list(initial_state)
    print('%2s: %s' % (0, ''.join(state)))
    total_plants = 0
    # total_plants += state.count('#')
    quiz = set()
    insertion_size = 2

    left_offset = 0
    target_generation = 50000000000  # counting from 1
    reached_stability = None
    stable_quizes = []

    for generation_idx in range(target_generation):
        new_state = (['.'] * insertion_size) + list(state) + (['.'] * insertion_size)
        left_offset -= insertion_size
        quiz = set()

        for pot_idx in range(len(state)):
            if pot_idx < 2:
                selection = (['.', ] * (2 - pot_idx)) + state[:pot_idx + 3]
            elif pot_idx >= len(state) - 2:
                selection = state[pot_idx - 2:] + (['.', ] * (2 - (len(state) - pot_idx - 1)))
            else:
                selection = state[pot_idx - 2: pot_idx+3]
            assert len(selection) == 5

            # print('%s => %s' % (''.join(selection), conditions_dict.get(tuple(selection), '.')))

            new_plant = conditions_dict.get(tuple(selection))
            new_plant = new_plant or '.'
            new_state[pot_idx + insertion_size] = new_plant

            # if generation_idx + 1 == target_generation or reached_stability:
            if True:
                # real_pot_idx = pot_idx - (generation_idx * insertion_size)
                real_pot_idx = left_offset + pot_idx + 2
                if new_plant == '#':
                    # print(len(new_state), left_offset, pot_idx, real_pot_idx)
                    quiz.add(real_pot_idx)

        first_plant_idx = new_state.index('#')
        if first_plant_idx >= 0 and first_plant_idx > 4:
            new_state = new_state[first_plant_idx - 4:]
            left_offset += (first_plant_idx - 4)
        last_plant_idx = len(new_state) - 1
        while new_state[last_plant_idx] != '#' and last_plant_idx > 0:
            last_plant_idx -= 1
        if last_plant_idx >= 0 and last_plant_idx + 4 <= len(new_state) - 1:
            new_state = new_state[:last_plant_idx + 5]

        if reached_stability:
            if (generation_idx + 1) % 100 == 0:
                stable_quizes.append(sum(quiz))
            if (generation_idx + 1) % 2000 == 0:
                break
        # if reached_stability:
        #     drift = left_offset - reached_stability[1]
        #     break
        if not reached_stability and state == new_state:
            reached_stability = (generation_idx, left_offset)
        state = new_state

        if not reached_stability or (generation_idx + 1) % 10000 == 0:
            print('%2s: %s  left_offset=%s  generation_quiz=%s' % (generation_idx + 1, ''.join(state), left_offset, sum(quiz)))
        total_plants += state.count('#')
    print('total_plants: %s    quiz: %s' % (total_plants, sum(quiz)))

    second_quiz = stable_quizes[-1]
    second_quiz += int((target_generation - 2000) / 100) * (stable_quizes[-1] - stable_quizes[-2])
    print('second_quiz=%s' % (second_quiz, ))

    return
    print('drift=%s  left_offset=%s  generation_idx=%s' % (drift, left_offset, generation_idx, ))
    quiz = set()
    left_offset += (drift * (target_generation - generation_idx - 1))
    for pot_idx in range(len(new_state)):
        if new_state[pot_idx] == '#':
            real_pot_idx = left_offset + pot_idx + 2
            quiz.add(real_pot_idx)
    print(sorted(quiz))
    second_quiz = sum(quiz)
    # second_quiz -= (drift * (target_generation - generation_idx - 1)) * new_state.count('#')
    print('second_quiz=%s' % (second_quiz, ))


def main():
    # tests = [
    #     ('pb00_input00.txt', 325, ),
    # ]
    # for test, expected in tests:
    #     graph = read(test)
    #     res = solve(graph)
    #     print(test, expected, res)

    test = 'pb00_input01.txt'
    graph = read(test)
    result = solve(graph)
    print(result)


__name__ == '__main__' and main()
