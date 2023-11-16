import fileinput
import itertools
import operator
import math
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test25.txt"


def parse(lines):
    # return [line.strip() for line in lines]
    res = []
    for line in lines:
        row = line.strip()
        res.append(row)
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))

def snafu_to_int(s):
    """
    >>> snafu_to_int('1=-0-2')
    1747
    >>> snafu_to_int('12111')
    906
    """
    digits = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    res = 0
    place = 1
    for c in ''.join(list(s)[::-1]):
        res += digits[c] * place
        place *= 5
    return res

def int_to_snafu(i):
    """
    >>> int_to_snafu(1747)
    '1=-0-2'
    >>> int_to_snafu(906)
    '12111'
    >>> int_to_snafu(314159265)
    '1121-1110-1=0'
    """
    digits = {2: '2', 1: '1', 0: '0', -1: '-', -2: '='}
    res = ''
    place = 0
    while i != 0:
        digit = i % (5 ** (place + 1)) // (5 ** place)
        if digit > 2:
            digit -= 5
        res = digits[digit] + res
        i -= digit * 5 ** place
        place += 1
    return res

def solve_part1(data):
    res = sum((snafu_to_int(x) for x in data))
    return int_to_snafu(res)

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == '2=-1=0'

def solve_part2(data):
    for line in data:
        pass

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == None


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
