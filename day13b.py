import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce, cmp_to_key
from util import *


TEST_FILE = "test13.txt"


def parse(lines):
    # return [line.strip() for line in lines]
    res = []
    for r1, r2 in isplit(lines):
        group = eval(r1), eval(r2)
        res.append(group)
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))

def cmp(left, right) -> int:
    """
    >>> cmp([1,1,3,1,1],[1,1,5,1,1])
    -1
    >>> cmp([[1],[2,3,4]],[[1],4])
    -1
    >>> cmp([9],[[8,7,6]])
    1
    >>> cmp([7,7,7,7],[7,7,7])
    1
    >>> cmp([],[3])
    -1
    >>> cmp([[[]]],[[]])
    1
    >>> cmp([[],9],[1,1])
    -1
    >>> cmp(\
    [[4, [1, []]], [8, 3, [[0, 2], [5, 2, 6], [7, 0, 10, 0], 2, [5, 7, 10, 2]], [[5, 9], 5, 10, [9, 7, 7]]]],\
    [[[], 9], [[[3, 2, 6, 3], [7, 8]], 10], [1]])
    1
    >>> cmp(\
    [[[], 9], [[[3, 2, 6, 3], [7, 8]], 10], [1]],\
    [[4, [1, []]], [8, 3, [[0, 2], [5, 2, 6], [7, 0, 10, 0], 2, [5, 7, 10, 2]], [[5, 9], 5, 10, [9, 7, 7]]]])
    -1
    >>> cmp([[0], [[[1], 0, []]]], [[[[10, 8], [3,6,7]]]])
    -1
    """
    while left and right:
        x, *left = left
        y, *right = right
        #print((x,y))
        match x, y:
            case list(x), list(y):
                res = cmp(x, y)
                if res:
                    return res
            case list(x), y:
                res = cmp(x, [y])
                if res:
                    return res
            case x, list(y):
                res = cmp([x], y)
                if res:
                    return res
            case x, y:
                if x < y:
                    return -1
                elif x > y:
                    return 1
    if left and not right:
        return 1
    elif not left and right:
        return -1
    return 0

def solve_part1(data):
    res = [cmp(l, r) for l, r in data]
    for l, r in data:
        if cmp(l, r) != -cmp(r, l):
            print(l)
            print(r)
            raise ValueError((l, r))
    return sum((i+1 for i, c in with_index(res) if c == -1))

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 13

def solve_part2(data):
    data.append(([[2]], [[6]]))
    packets = itertools.chain.from_iterable(data)
    res = list(sorted(packets, key=cmp_to_key(cmp)))
    i1 = res.index([[2]]) + 1
    i2 = res.index([[6]]) + 1
    return i1 * i2


def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 140


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
