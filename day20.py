import fileinput
import itertools
import operator
import math
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test20.txt"


def parse(lines):
    # return [line.strip() for line in lines]
    res = []
    for line in lines:
        row = int(line.strip())
        res.append(row)
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))

def mix(data):
    ns = list(range(len(data)))
    for i in range(len(data)):
        op = data[i]
        if op == 0:
            continue
        idx = ns.index(i)
        new_idx = int(math.remainder(idx + op, len(data) - 1))
        #print(op, idx, new_idx)
        del ns[idx]
        if new_idx == 0 and op < 0:
            ns.append(i)
        else:
            ns.insert(new_idx, i)
        #print(ns)
        #print([data[i] for i in ns])
    return [data[i] for i in ns]

def mix2(ops, data, rounds=1):
    #print([int(math.remainder(i, len(data))) for i in ops])
    ns = list(data)
    for i in range(len(data)*rounds):
        op = ops[i%len(data)]
        if op == 0:
            continue
        idx = ns.index(op)
        new_idx = int(math.remainder(idx + op, len(data) - 1))
        del ns[idx]
        if new_idx == 0 and op < 0:
            ns.append(op)
        else:
            ns.insert(new_idx, op)
        #print([data[i] for i in ns])
        #print(ns)
    return ns

def test_mix():
    res = parse(fileinput.input(TEST_FILE))
    a = mix(res)
    assert a == [1, 2, -3, 4, 0, 3, -2]
    assert mix([0, 0, 0, -3, 0, 0, 0]) == [0, 0, 0, 0, 0, 0, -3]
    assert mix([0, 0, 0, -2, 0, 0, 0]) == [0, -2, 0, 0, 0, 0, 0]
    assert mix([0, 0, 0, -4, 0, 0, 0]) == [0, 0, 0, 0, 0, -4, 0]
    assert mix([0, 0, 0, -6, 0, 0, 0]) == [0, 0, 0, -6, 0, 0, 0]
    assert mix([0, 0, 0, -7, 0, 0, 0]) == [0, 0, -7, 0, 0, 0, 0]
    #assert mix([0, 0, 0, 0, 0, 1, 0]) == [0, 0, 0, 0, 0, 0, 1]
    #assert mix([0, 0, 0, 0, 0, 0, 1]) == [1, 0, 0, 0, 0, 0, 0]

def test_mix2():
    res = parse(fileinput.input(TEST_FILE))
    a = mix2(res, res)
    assert a == [1, 2, -3, 4, 0, 3, -2]
    assert mix2([0, 0, 0, -3, 0, 0, 0], [0, 0, 0, -3, 0, 0, 0]) == [0, 0, 0, 0, 0, 0, -3]
    assert mix2([0, 0, 0, -2, 0, 0, 0], [0, 0, 0, -2, 0, 0, 0]) == [0, -2, 0, 0, 0, 0, 0]
    assert mix2([0, 0, 0, -4, 0, 0, 0], [0, 0, 0, -4, 0, 0, 0]) == [0, 0, 0, 0, 0, -4, 0]
    assert mix2([0, 0, 0, -6, 0, 0, 0], [0, 0, 0, -6, 0, 0, 0]) == [0, 0, 0, -6, 0, 0, 0]
    assert mix2([0, 0, 0, -7, 0, 0, 0], [0, 0, 0, -7, 0, 0, 0]) == [0, 0, -7, 0, 0, 0, 0]
    ops = [811589153 * x for x in res]
    data = list(ops)
    a = mix2(ops, data)
    assert a == [0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153]
    a = mix2(ops, data, 2)
    assert a == [0, 2434767459, 1623178306, 3246356612, -2434767459, -1623178306, 811589153]
    a = mix2(ops, data, 3)
    assert a == [0, 811589153, 2434767459, 3246356612, 1623178306, -1623178306, -2434767459]

def solve_part1(data):
    a = mix(data)
    start = a.index(0)
    return a[(start+1000)%len(data)] + a[(start+2000)%len(data)] + a[(start+3000)%len(data)]

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 3

def solve_part2(data):
    ops = [811589153 * x for x in data]
    a = ops
    for i in range(10):
        a = mix2(ops, a)
        #print(i)
        #print(a)
    start = a.index(0)
    return a[(start+1000)%len(data)] + a[(start+2000)%len(data)] + a[(start+3000)%len(data)]

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 1623178306


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
