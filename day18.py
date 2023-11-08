import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test18.txt"


def parse(lines):
    res = []
    for line in lines:
        row = [int(x) for x in line.strip().split(',')]
        res.append(Vec3(*row))
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))
    print(res)

def solve_part1(data):
    res = 0
    for cur in data:
        sides = 6
        for other in data:
            if other != cur and abs(cur - other).manhattan() == 1:
                sides -= 1
        res += sides
    return res

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 64

def solve_part2(data):
    res = 0
    max_x = max((n.x for n in data))
    max_y = max((n.y for n in data))
    max_z = max((n.z for n in data))
    for x in range(max_x):
        for y in range(max_y):
            for z in range(max_z):
                if Vec3(x, y, z) in data:
                    continue
                if all((n in data for n in Vec3(x, y, z).cneighbors())):
                    print((x, y, z))
                    res -= 6
    for i in range(len(data)):
        sides = 6
        x1, y1, z1 = data[i]
        for j in range(len(data)):
            if i == j:
                continue
            x2, y2, z2 = data[j]
            if x1 == x2 and y1 == y2 and abs(z1 - z2) == 1:
                sides -= 1
            elif abs(x1 - x2) == 1 and y1 == y2 and z1 == z2:
                sides -= 1
            elif x1 == x2 and abs(y1 - y2) == 1 and z1 == z2:
                sides -= 1
        res += sides
    return res

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 58


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
