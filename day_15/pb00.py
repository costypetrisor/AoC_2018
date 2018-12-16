
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


Sample = collections.namedtuple('Sample', 'before, code, after')


def read(filepath):
    samples = []
    test_program = []

    before = None
    code = None
    after = None

    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            m = re.search(r'Before:\s*[(\[]([^)\]]+)[)\]]', line)
            if m:
                before = m.group(1)
                before = [int(e.strip()) for e in before.split(',')]
                continue

            m = re.search(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
            if m:
                line_of_code = tuple(map(int, m.groups()))
                if before:
                    code = line_of_code
                else:
                    test_program.append(line_of_code)

            m = re.search(r'After:\s*[(\[]([^)\]]+)[)\]]', line)
            if m:
                after = m.group(1)
                after = [int(e.strip()) for e in after.split(',')]

                samples.append(Sample(before, code, after))
                before = code = after = None
                continue

    print(f'Read {len(samples)} samples and a test program {len(test_program)} instructions long')
    # print(samples[:3])
    # print(samples[-3:])
    # print(test_program[:3])
    # print(test_program[-3:])

    return samples, test_program


def op_addr(registers, code):
    res = list(registers)
    res[code[3]] = registers[code[1]] + registers[code[2]]
    return res


def op_addi(registers, code):
    res = list(registers)
    res[code[3]] = registers[code[1]] + code[2]
    return res


def op_mulr(registers, code):
    res = list(registers)
    res[code[3]] = registers[code[1]] * registers[code[2]]
    return res


def op_muli(registers, code):
    res = list(registers)
    res[code[3]] = registers[code[1]] * code[2]
    return res


def op_banr(registers, code):
    res = list(registers)
    res[code[3]] = registers[code[1]] & registers[code[2]]
    return res


def op_bani(registers, code):
    res = list(registers)
    res[code[3]] = registers[code[1]] & code[2]
    return res


def op_borr(registers, code):
    res = list(registers)
    res[code[3]] = registers[code[1]] | registers[code[2]]
    return res


def op_bori(registers, code):
    res = list(registers)
    res[code[3]] = registers[code[1]] | code[2]
    return res


def op_setr(registers, code):
    res = list(registers)
    res[code[3]] = registers[code[1]]
    return res


def op_seti(registers, code):
    res = list(registers)
    res[code[3]] = code[1]
    return res


def op_gtir(registers, code):
    res = list(registers)
    res[code[3]] = 1 if code[1] > registers[code[2]] else 0
    return res


def op_gtri(registers, code):
    res = list(registers)
    res[code[3]] = 1 if registers[code[1]] > code[2] else 0
    return res


def op_gtrr(registers, code):
    res = list(registers)
    res[code[3]] = 1 if registers[code[1]] > registers[code[2]] else 0
    return res


def op_eqir(registers, code):
    res = list(registers)
    res[code[3]] = 1 if code[1] == registers[code[2]] else 0
    return res


def op_eqri(registers, code):
    res = list(registers)
    res[code[3]] = 1 if registers[code[1]] == code[2] else 0
    return res


def op_eqrr(registers, code):
    res = list(registers)
    res[code[3]] = 1 if registers[code[1]] == registers[code[2]] else 0
    return res


ALL_OPCODES = (
    op_addr,
    op_addi,
    op_mulr,
    op_muli,
    op_banr,
    op_bani,
    op_borr,
    op_bori,
    op_setr,
    op_seti,
    op_gtir,
    op_gtri,
    op_gtrr,
    op_eqir,
    op_eqri,
    op_eqrr,
)


def solve(samples, test_program):
    samples_matching_ge_3_opcodes = 0

    for sample in samples:
        nb_opcodes_matching = 0
        for opcode in ALL_OPCODES:
            res = opcode(sample.before, sample.code)
            if res == sample.after:
                nb_opcodes_matching += 1
        if nb_opcodes_matching >= 3:
            samples_matching_ge_3_opcodes += 1

    print(f'Samples matching >= 3 opcodes: {samples_matching_ge_3_opcodes}')


def main():
    tests = [
        ('pb00_input00.txt', 17, ),
    ]
    for test, expected in tests:
        _input = read(test)
        res = solve(*_input)
        print(test, expected, res)

    # test = 'pb00_input01.txt'
    # graph = read(test)
    # result = solve(graph)
    # print(result)


__name__ == '__main__' and main()
