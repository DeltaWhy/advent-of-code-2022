import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from util import *


TEST_FILE = "testXX.txt"


def solve_part1(lines):
    for line in lines:
        pass

def test_solve_part1():
    assert solve_part1(fileinput.input(TEST_FILE)) == None

def solve_part2(lines):
    for line in lines:
        pass

def test_solve_part2():
    assert solve_part2(fileinput.input(TEST_FILE)) == None


if __name__ == '__main__':
    lines1, lines2 = itertools.tee(fileinput.input())
    part1 = solve_part1(lines1)
    part2 = solve_part2(lines2)
    print(part1)
    print(part2)
