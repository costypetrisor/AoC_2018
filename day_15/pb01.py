
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


class Sample(collections.namedtuple('_Sample', 'before, code, after')):

    def __hash__(self):
        return hash((tuple(self.before), tuple(self.code), tuple(self.after), ))

    def __eq__(self, other):
        if not isinstance(other, Sample):
            raise TypeError(other)
        return self.before == other.before and self.code == other.code and self.after == other.after


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


ALL_OPS = (
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


class OpcodeConflict(Exception):
    pass


def identify_opcodes(samples_to_matching_ops, all_ops, opcodes=None):
    if opcodes:
        opcodes = opcodes.copy()
    else:
        opcodes = {}
    ops_to_codes = {v: k for k, v in opcodes.items()}

    last_nb_identified_ops = len(opcodes)

    while len(opcodes) != len(all_ops):
        for sample, ops_matching in samples_to_matching_ops.items():
            if set(ops_matching) & ops_to_codes.keys():
                ops_matching = [op for op in ops_matching if op not in ops_to_codes]
            if len(ops_matching) == 1:
                if sample.code[0] in opcodes:
                    if ops_matching[0] != opcodes[sample.code[0]]:
                        raise OpcodeConflict(
                            f'Conflict: for code {sample.code[0]} matching op '
                            f'{ops_matching[0].__name__} was previously '
                            f'identified as {opcodes[sample.code[0]].__name__}')
                else:
                    opcodes[sample.code[0]] = ops_matching[0]
                    ops_to_codes[ops_matching[0]] = sample.code[0]

        # print(f'{len(all_ops) - len(opcodes)} opcodes left to identify')
        # pprint(opcodes)
        if len(opcodes) == last_nb_identified_ops:
            break
        last_nb_identified_ops = len(opcodes)

    return opcodes


def identify_opcodes_with_assumption(samples_to_matching_ops, all_ops, opcodes=None):
    if opcodes:
        opcodes = opcodes.copy()
    else:
        opcodes = {}
    ops_to_codes = {v: k for k, v in opcodes.items()}

    for sample, ops_matching in samples_to_matching_ops.items():
        ops_matching = [op for op in ops_matching if op not in ops_to_codes]

        if len(ops_matching) > 1:
            for matching_op in ops_matching:
                opcodes_variant = opcodes.copy()
                opcodes_variant[sample.code[0]] = matching_op

                opcodes_variant, _ = identify_opcodes_with_assumption(samples_to_matching_ops, all_ops, opcodes=opcodes_variant)
                if len(opcodes_variant) == len(all_ops):
                    return opscodes
    print('identify_opcodes_with_assumption  returns None')


def solve(samples, test_program):
    samples_orig = list(samples)

    samples_to_matching_ops = {}
    for sample in samples:
        opcodes_matching = []
        for opcode in ALL_OPS:
            res = opcode(sample.before, sample.code)
            if res == sample.after:
                opcodes_matching.append(opcode)
        samples_to_matching_ops[sample] = opcodes_matching

    OPCODES = identify_opcodes(samples_to_matching_ops, ALL_OPS)
    pprint(OPCODES)
    print('-----')

    # NO need to backtrack anymore
    # OPCODES = identify_opcodes_with_assumption(samples_to_matching_ops, ALL_OPS, opcodes=OPCODES)

    pprint(OPCODES)
    if len(OPCODES) != len(ALL_OPS):
        raise Exception("not all OPCODES identified")

    registers = [0, 0, 0, 0]
    for code in test_program:
        registers = OPCODES[code[0]](registers, code)

    print(f'Registers at the end: {registers}')



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
