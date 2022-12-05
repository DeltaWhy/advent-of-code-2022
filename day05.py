import fileinput
import itertools
import operator
import re
from collections import Counter, defaultdict, deque
from util import *


TEST_FILE = "test05.txt"


def solve_part1(lines):
    layout, moves = tuple(isplit(lines, lambda x: not x.split()))
    stacks = defaultdict(deque)
    for row in layout:
        if '[' not in row:
            break
        for i in range(1, len(row), 4):
            if row[i] != ' ':
                stacks[int(i/4)+1].append(row[i])
    print(stacks)
    for row in moves:
        match = re.match('move ([0-9]+) from ([0-9]+) to ([0-9]+)', row)
        count, fromstack, tostack = match.groups()
        for i in range(int(count)):
            stacks[int(tostack)].appendleft(stacks[int(fromstack)].popleft())
    print(stacks)
    res = ''
    for i in range(1, max(stacks.keys())+1):
        res += stacks[i][0]
    return res

def test_solve_part1():
    assert solve_part1(fileinput.input(TEST_FILE)) == 'CMZ'

def solve_part2(lines):
    layout, moves = tuple(isplit(lines, lambda x: not x.split()))
    stacks = defaultdict(deque)
    for row in layout:
        if '[' not in row:
            break
        for i in range(1, len(row), 4):
            if row[i] != ' ':
                stacks[int(i/4)+1].append(row[i])
    print(stacks)
    for row in moves:
        match = re.match('move ([0-9]+) from ([0-9]+) to ([0-9]+)', row)
        count, fromstack, tostack = match.groups()
        tempstack = deque()
        for i in range(int(count)):
            tempstack.appendleft(stacks[int(fromstack)].popleft())
        stacks[int(tostack)].extendleft(tempstack)
    print(stacks)
    res = ''
    for i in range(1, max(stacks.keys())+1):
        res += stacks[i][0]
    return res

def test_solve_part2():
    assert solve_part2(fileinput.input(TEST_FILE)) == 'MCD'


if __name__ == '__main__':
    lines1, lines2 = itertools.tee(fileinput.input())
    part1 = solve_part1(lines1)
    part2 = solve_part2(lines2)
    print(part1)
    print(part2)
