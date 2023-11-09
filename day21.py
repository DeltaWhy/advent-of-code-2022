import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce, cache
from util import *


TEST_FILE = "test21.txt"


def parse(lines):
    # return [line.strip() for line in lines]
    res = {}
    for line in lines:
        k, _, v = line.partition(': ')
        v2 = v.split()
        if len(v2) == 1:
            res[k] = int(v2[0])
        else:
            res[k] = tuple(v2)
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))
    print(res)

def value(monkeys, monkey):
    if isinstance(monkeys[monkey], int):
        return monkeys[monkey]
    ma, op, mb = monkeys[monkey]
    a = value(monkeys, ma)
    b = value(monkeys, mb)
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
    else:
        raise ValueError()

def solve_part1(data):
    return int(value(data, 'root'))

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 152

def solve_part2(data):
    for line in data:
        pass

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 301


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
