import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from util import *


TEST_FILE = "test09.txt"


def parse(lines):
    # return [line.strip() for line in lines]
    res = []
    for line in lines:
        row = line.strip().split()
        res.append((row[0], int(row[1])))
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))
    assert isinstance(res[0][1], int)

def touching(head, tail):
    """
    >>> touching([0,0], [0,1])
    True
    >>> touching([1,1], [0,0])
    True
    >>> touching([1,2], [3,1])
    False
    """
    return abs(head[0]-tail[0]) <= 1 and abs(head[1]-tail[1]) <= 1

def sign(n):
    if n == 0:
        return 0
    return int(n / abs(n))

def next_tail(head, tail):
    """
    >>> next_tail([0,0], [0,2])
    (0, 1)
    >>> next_tail([0,0], [1,1])
    (1, 1)
    >>> next_tail([0,0], [1,2])
    (0, 1)
    """
    if touching(head, tail):
        return tuple(tail)
    dx = tail[0] - head[0]
    dy = tail[1] - head[1]
    if dx == 0:
        return (tail[0], tail[1] - sign(dy))
    if dy == 0:
        return (tail[0] - sign(dx), tail[1])
    return (tail[0] - sign(dx), tail[1] - sign(dy))

def solve_part1(data):
    head = [0,0]
    tail = [0,0]
    visited = set()
    visited.add(tuple(tail))
    for direction, count in data:
        diff = {'U': (0, -1),
                'D': (0, 1),
                'L': (-1, 0),
                'R': (1, 0)}[direction]
        for i in range(count):
            head = (head[0] + diff[0], head[1] + diff[1])
            tail = next_tail(head, tail)
            visited.add(tuple(tail))

    return len(visited)

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 13

def solve_part2(data):
    rope = [(0, 0)] * 10
    visited = set()
    visited.add(tuple(rope[-1]))
    for direction, count in data:
        diff = {'U': (0, -1),
                'D': (0, 1),
                'L': (-1, 0),
                'R': (1, 0)}[direction]
        for i in range(count):
            rope[0] = (rope[0][0] + diff[0], rope[0][1] + diff[1])
            for j in range(0, len(rope) - 1):
                rope[j+1] = next_tail(rope[j], rope[j+1])
            visited.add(tuple(rope[-1]))

    return len(visited)

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 1


if __name__ == '__main__':
    data = parse(fileinput.input())
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
