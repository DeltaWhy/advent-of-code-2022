import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from util import *


TEST_FILE = "testXX.txt"


def parse(lines):
    return [line.strip() for line in lines]
    # res = []
    # for line in lines:
    #     row = line.strip().split()
    #     res.append(row)
    # return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))

def solve_part1(data):
    for line in data:
        pass

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == None

def solve_part2(data):
    for line in data:
        pass

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == None


if __name__ == '__main__':
    data = parse(fileinput.input())
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
