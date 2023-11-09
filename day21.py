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

def symvalue(monkeys, monkey):
    if monkey == 'humn':
        return 'humn'
    if isinstance(monkeys[monkey], int):
        return monkeys[monkey]
    ma, op, mb = monkeys[monkey]
    a = symvalue(monkeys, ma)
    b = symvalue(monkeys, mb)
    if isinstance(a, int) and isinstance(b, int):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a // b
        else:
            raise ValueError()
    return (a, op, b)

def solve(eqn, answer):
    """
    >>> solve('humn', 42)
    42
    >>> solve(('humn', '+', 2), 42)
    40
    >>> solve((2, '*', ('humn', '+', 4)), 42)
    17
    >>> solve((42, '-', 'humn'), 40)
    2
    """
    if isinstance(eqn, str):
        return answer
    a, op, b = eqn
    if isinstance(a, int):
        if op == '+':
            return solve(b, answer - a)
        elif op == '-':
            return solve(b, -(answer - a))
        elif op == '*':
            return solve(b, answer // a)
        elif op == '/':
            raise ValueError()
            return solve(b, answer * a)
    elif isinstance(b, int):
        if op == '+':
            return solve(a, answer - b)
        elif op == '-':
            return solve(a, answer + b)
        elif op == '*':
            return solve(a, answer // b)
        elif op == '/':
            return solve(a, answer * b)
    raise ValueError()

def solve_part2(data):
    del data['humn']
    a = symvalue(data, data['root'][0])
    b = symvalue(data, data['root'][2])
    if isinstance(a, int):
        return solve(b, a)
    else:
        return solve(a, b)

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
