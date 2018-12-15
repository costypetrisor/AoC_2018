
import collections
import datetime
import functools
import itertools
import json
import math
from pprint import pformat, pprint
import re
import sys
import uuid

from more_itertools import windowed

UNIT_TYPES = ('G', 'E', )
OTHER_UNIT_TYPE = {
    'G': 'E',
    'E': 'G',
}
MOVE_OFFSETS = ((-1, 0), (0, -1), (0, 1), (1, 0))


class Unit:
    def __init__(self, _type, pos, hitpoints=200, attack=3):
        self._id = uuid.uuid4()
        self._type = _type
        self.pos = pos
        self.hitpoints = hitpoints
        self.attack = attack

    def __repr__(self):
        return f'Unit({self._type!r}, {self.pos}, {self.hitpoints})'


class Example:

    def __init__(
            self, starting_grid=None, ending_grid=None, ending_units=None,
            nb_rounds_end=None, winner_team=None, hp_left=None, outcome=None):
        self.starting_grid = starting_grid
        self.ending_grid = ending_grid
        self.ending_units = ending_units
        self.nb_rounds_end = nb_rounds_end
        self.winner_team = winner_team
        self.hp_left = hp_left
        self.outcome = outcome

    def show(self):
        units_by_row = collections.defaultdict(list)
        for u in self.ending_units:
            units_by_row[u.pos[0]].append(u)

        middle_row = len(self.starting_grid) // 2
        for row_idx, starting_row, ending_row in zip(
                itertools.count(), self.starting_grid, self.ending_grid):
            if middle_row == row_idx:
                line = f'{starting_row}  -->  {ending_row}'
            else:
                line = f'{starting_row}       {ending_row}'
            if units_by_row[row_idx]:
                units_str = ', '.join(
                    f'{u._type}({u.hitpoints})' for u in units_by_row[row_idx])
                line += f'   {units_str}'
            print(line)
        print('')
        print(f'Combat ends after {self.nb_rounds_end} full rounds')
        print(f'{self.winner_team} win with {self.hp_left} total hit points left')
        print(f'Outcome: {self.nb_rounds_end} * {self.hp_left} = {self.outcome}')
        print('')


def read(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]
    return lines


def read_example(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    nb_cols = 0
    while lines[nb_cols][0] == '#':
        nb_cols += 1

    first_space = lines[0].find(' ')
    starting_grid = [l[:first_space] for l in lines[:nb_cols]]

    second_grid = first_space + lines[0][first_space:].find('#')
    ending_grid = [
        l[second_grid:second_grid+first_space]
        for l in lines[:nb_cols]]

    ending_units = []
    for row_idx, line in enumerate(lines[:nb_cols]):
        units_in_ending_grid = [
            (col_idx, unit)
            for col_idx, unit in enumerate(ending_grid[row_idx])
            if unit in UNIT_TYPES]

        line = line[second_grid + first_space:]
        line = line.strip()
        elems = [e.strip() for e in line.split(',') if e.strip()]
        for elem_idx, elem in enumerate(elems):
            unit_type = elem[0]
            unit_hp = int(re.search(r'(\d+)', elem).group(0))
            unit = Unit(
                unit_type, [row_idx, units_in_ending_grid[elem_idx][0]],
                hitpoints=unit_hp)
            ending_units.append(unit)

    nb_rounds_end = int(re.search(
        r'Combat ends after (\d+) full rounds', lines[nb_cols + 1]).group(1))
    winner_team, hp_left = re.search(
        r'(\w+) win with (\d+) total hit points left',
        lines[nb_cols + 2]).groups()
    hp_left = int(hp_left)
    nb_rounds_end_check, hp_left_check, outcome = map(int, re.search(
        r'Outcome: (\d+) \* (\d+) = (\d+)', lines[nb_cols + 3]).groups())
    assert nb_rounds_end_check == nb_rounds_end
    assert hp_left_check == hp_left
    assert nb_rounds_end * hp_left == outcome

    ex = Example(
        starting_grid, ending_grid, ending_units, nb_rounds_end,
        winner_team, hp_left, outcome)

    return ex


def find_dest_and_shortest_path(
        grid, starting_pos, destinations):
    grid = [list(row) for row in grid]
    print(f'starting_pos={starting_pos}  destinations={destinations}')

    def print_grid():
        for row in grid:
            print(''.join(map(str, row)))
        print('')

    steps = [[starting_pos, ], ]
    while True:
        step_idx = len(steps)
        possible_moves = []
        reached_destinations = []
        for pos in steps[-1]:
            for offset_x, offset_y in MOVE_OFFSETS:
                new_move = [pos[0] + offset_x, pos[1] + offset_y]
                if grid[new_move[0]][new_move[1]] == '.':
                    grid[new_move[0]][new_move[1]] = step_idx
                    possible_moves.append(new_move)

                    for dest in destinations:
                        if abs(dest[0] - new_move[0]) + abs(dest[1] - new_move[1]) == 1:
                            reached_destinations.append(new_move)
            # print_grid()
        if not possible_moves:
            break

        steps.append(possible_moves)

        if reached_destinations:
            print_grid()
            break

    if reached_destinations:
        reached_destinations = sorted(reached_destinations)
        reached_dest = reached_destinations[0]

        # print(f'steps={len(steps)} {steps}')
        path = [reached_dest, ]
        for i in range(len(steps) - 2, 0, -1):
            old_pos = path[-1]
            # print(f'backtracking for pos {old_pos} path={path}  i={i}')
            for offset_x, offset_y in MOVE_OFFSETS:
                new_pos = [old_pos[0] + offset_x, old_pos[1] + offset_y]
                # print(new_pos, grid[new_pos[0]][new_pos[1]])
                if grid[new_pos[0]][new_pos[1]] == i:
                    path.append(new_pos)
                    break
        path = list(reversed(path))

        print(f'reached_dest={reached_dest}  path={path}')
        return reached_dest, path
    return None, None


def solve(starting_grid, elf_attack=3):
    grid = [list(row) for row in starting_grid]

    units = []
    for row_idx, row in enumerate(grid):
        for col_idx, elem in enumerate(row):
            if elem in UNIT_TYPES:
                unit = Unit(
                    elem, [row_idx, col_idx],
                    attack=(elf_attack if elem == 'E' else 3))
                units.append(unit)
    starting_units = list(units)

    round_idx = 0
    combat_ended = False
    while not combat_ended:
        round_idx += 1
        print(f'Round: {round_idx}')
        units = sorted(units, key=lambda u: u.pos)
        # print(units)

        # grid_unit_order = [list(row) for row in grid]
        # for u_idx, u in enumerate(units):
        #     grid_unit_order[u.pos[0]][u.pos[1]] = str(u_idx)
        # for row in grid_unit_order:
        #     print(''.join(row))
        # print('')

        unit_positions_at_turn_start = {u._id: u.pos for u in units}

        for unit in list(units):
            if unit.hitpoints <= 0:
                continue
            print(f'Turn of {unit}')
            units_by_pos = {tuple(u.pos): u for u in units}  # computed here because they move
            units_by_type = collections.defaultdict(list)
            for u in units:
                units_by_type[u._type].append(u)

            if any(len(units_by_type[t]) == 0 for t in UNIT_TYPES):
                combat_ended = True
                break

            # move
            units_in_range_of_attack = []
            for offset_x, offset_y in MOVE_OFFSETS:
                pos = [unit.pos[0] + offset_x, unit.pos[1] + offset_y]
                try:
                    other_unit = grid[pos[0]][pos[1]]
                except IndexError:
                    continue
                if other_unit != unit._type and other_unit in UNIT_TYPES:
                    units_in_range_of_attack.append(units_by_pos[tuple(pos)])

            if units_in_range_of_attack:
                pass
            else:
                # find all empty spots around enemy units
                empty_spots_around_enemies = set()
                for enemy_unit in units_by_type[OTHER_UNIT_TYPE[unit._type]]:
                    for empty_spot in [
                        [enemy_unit.pos[0] + offset_x, enemy_unit.pos[1] + offset_y]
                        for offset_x, offset_y in MOVE_OFFSETS
                    ]:
                        if grid[empty_spot[0]][empty_spot[1]] == '.':
                            empty_spots_around_enemies.add(tuple(empty_spot))
                if not empty_spots_around_enemies:
                    continue

                # print(units_by_type)
                # print(units_by_type[OTHER_UNIT_TYPE[unit._type]])
                enemy_positions = [eu.pos for eu in units_by_type[OTHER_UNIT_TYPE[unit._type]]]

                dest, shorted_path = find_dest_and_shortest_path(
                    grid, unit.pos, enemy_positions)
                if dest:
                    new_pos = shorted_path[0]
                    assert abs(unit.pos[0] - new_pos[0]) <= 1 and abs(unit.pos[1] - new_pos[1]) <= 1
                    print(f'{unit} moves to position {new_pos}')
                    grid[unit.pos[0]][unit.pos[1]] = '.'
                    unit.pos = new_pos
                    grid[unit.pos[0]][unit.pos[1]] = unit._type
                # else:
                #     continue

            # attack
            units_in_range_of_attack = []
            for offset_x, offset_y in MOVE_OFFSETS:
                pos = [unit.pos[0] + offset_x, unit.pos[1] + offset_y]
                try:
                    other_unit = grid[pos[0]][pos[1]]
                except IndexError:
                    continue
                if other_unit != unit._type and other_unit in UNIT_TYPES:
                    units_in_range_of_attack.append(units_by_pos[tuple(pos)])

            if units_in_range_of_attack:
                units_in_range_of_attack = sorted(units_in_range_of_attack, key=lambda u: (u.hitpoints, u.pos))
                if len(units_in_range_of_attack) > 1:
                    print(f'{unit} can attack: {units_in_range_of_attack}')

                unit_to_attack = units_in_range_of_attack[0]
                unit_to_attack.hitpoints -= unit.attack
                if unit_to_attack.hitpoints <= 0:
                    units.remove(unit_to_attack)

                    grid[unit_to_attack.pos[0]][unit_to_attack.pos[1]] = '.'
                    print(f'{unit} attacks {unit_to_attack} and that unit is killed')
                else:
                    print(f'{unit} attacks {unit_to_attack}')

            # units_in_range_of_attack = []
            # for enemy_unit in units:
            #     if enemy_unit.hitpoints <= 0:
            #         continue
            #     if enemy_unit._type == unit._type:
            #         continue
            #     pos_at_turn_start = unit_positions_at_turn_start[enemy_unit._id]
            #     if abs(unit.pos[0] - pos_at_turn_start[0]) + abs(unit.pos[1] - pos_at_turn_start[1]) == 1:
            #         units_in_range_of_attack.append(enemy_unit)

            # if units_in_range_of_attack:
            #     units_in_range_of_attack = sorted(units_in_range_of_attack, key=lambda u: (u.hitpoints, u.pos))
            #     if len(units_in_range_of_attack) > 1:
            #         print(f'{unit} can attack: {units_in_range_of_attack}')

            #     unit_to_attack = units_in_range_of_attack[0]
            #     unit_to_attack.hitpoints -= unit.attack
            #     if unit_to_attack.hitpoints <= 0:
            #         units.remove(unit_to_attack)

            #         grid[unit_to_attack.pos[0]][unit_to_attack.pos[1]] = '.'
            #         print(f'{unit} attacks {unit_to_attack} and that unit is killed')
            #     else:
            #         print(f'{unit} attacks {unit_to_attack}')

        print(f'Final positions at end of round {round_idx}')
        units_by_row = collections.defaultdict(list)
        for u in units:
            units_by_row[u.pos[0]].append(u)
        for row_idx, row in enumerate(grid):
            line = ''.join(row)
            if units_by_row[row_idx]:
                units_str = ', '.join(
                    f'{u._type}({u.hitpoints})' for u in sorted(units_by_row[row_idx], key=lambda u: u.pos))
                line += f'   {units_str}'
            print(line)
        print('')
        print('')
        print('')

    winning_unit_type = {u._type for u in units}
    assert len(winning_unit_type) == 1
    winning_unit_type = list(winning_unit_type)[0]
    winning_team = {'G': 'Goblins', 'E': 'Elves'}[winning_unit_type]
    hp_left = sum(u.hitpoints for u in units)
    nb_rounds_end = round_idx - 1
    outcome = nb_rounds_end * hp_left
    print(f'Combat ends after {nb_rounds_end} full rounds')
    print(f'{winning_team} win with {hp_left} total hit points left')
    print(f'Outcome: {nb_rounds_end} * {hp_left} = {outcome}')

    starting_elves = [u for u in starting_units if u._type == 'E']
    ending_elves = [u for u in units if u._type == 'E']
    return winning_unit_type, len(starting_elves) - len(ending_elves), outcome


def solve_2(starting_grid):
    elf_attack = 4
    while True:
        winning_unit_type, deaths, outcome = solve(starting_grid, elf_attack=elf_attack)
        print('')
        if winning_unit_type == 'E' and deaths == 0:
            print(f'Answer 2: elf_attack={elf_attack} outcome={outcome}')
            break
        elf_attack += 1
    return elf_attack, outcome


def main():
    tests = [
        # ('pb01_input00.txt', (15, 4988), ),
        # ('pb01_input01.txt', (4, 31284), ),
        # ('pb01_input02.txt', (15, 3478), ),
        # ('pb01_input03.txt', (12, 6474), ),
        # ('pb01_input04.txt', (34, 1140), ),
    ]
    for testfile, expected in tests:
        test = read_example(testfile)
        res = solve_2(test.starting_grid)
        print('')
        test.show()
        print(expected, res)
        print('')
        print('')

    test = None
    # test = 'pb00_testinput00.txt'
    # test = 'pb00_testinput01.txt'
    test = 'pb00_realinput00.txt'
    if test:
        graph = read(test)
        result = solve_2(graph)
    # print(result)


__name__ == '__main__' and main()
