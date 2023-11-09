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

class Grid3(list):
    def __init__(self, max_x, max_y, max_z):
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
        super().__init__([False] * (max_x * max_y * max_z))
    
    def __getitem__(self, coord):
        return super().__getitem__(coord[0] + coord[1] * self.max_x + coord[2] * self.max_x * self.max_y)

    def __setitem__(self, coord, value):
        super().__setitem__(coord[0] + coord[1] * self.max_x + coord[2] * self.max_x * self.max_y, value)

    def clone(self):
        res = Grid3.__new__(Grid3)
        res.max_x = self.max_x
        res.max_y = self.max_y
        res.max_z = self.max_z
        list.__init__(res, self)
        return res

def solve_part1(data):
    res = 0
    max_size = max((max(vec) for vec in data)) + 1
    grid = Grid3(max_size, max_size, max_size)
    for cur in data:
        grid[cur] = True
    for cur in data:
        sides = 6
        for other in cur.cneighbors():
            if max(other) < max_size and grid[other]:
                sides -= 1
        # for other in data:
        #     if other != cur and abs(cur - other).manhattan() == 1:
        #         sides -= 1
        res += sides
    return res

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 64

def can_escape(grid: Grid3, coord: Vec3) -> bool:
    if grid[coord]:
        return False
    seen = grid.clone()
    queue = deque()
    for c in coord.cneighbors():
        if min(c) < 0 or c.x >= grid.max_x or c.y >= grid.max_y or c.z >= grid.max_z:
            return True
        if not seen[c]:
            queue.append(c)
    while queue:
        cur = queue.popleft()
        if seen[cur]:
            continue
        seen[cur] = True
        for c in cur.cneighbors():
            if min(c) < 0 or c.x >= grid.max_x or c.y >= grid.max_y or c.z >= grid.max_z:
                return True
            if not seen[c]:
                queue.append(c)
    return False

def test_can_escape():
    # create a hollow cube
    grid = Grid3(7, 7, 7)
    for x in range(1, 6):
        for y in range(1, 6):
            grid[(x, y, 1)] = True
            grid[(x, y, 5)] = True
    for z in range(2, 5):
        for x in range(1, 6):
            grid[(x, 1, z)] = True
            grid[(x, 5, z)] = True
        for y in range(2, 5):
            grid[(1, y, z)] = True
            grid[(5, y, z)] = True
    assert grid[(0,0,0)] == False
    assert grid[(2,1,3)] == True
    assert grid[(2,2,2)] == False
    assert grid[(3,3,3)] == False
    assert can_escape(grid, Vec3(0, 0, 0)) == True
    assert can_escape(grid, Vec3(1, 1, 1)) == False
    assert can_escape(grid, Vec3(2, 2, 2)) == False
    assert can_escape(grid, Vec3(3, 3, 3)) == False

def solve_part2(data):
    res = 0
    max_size = max((max(vec) for vec in data)) + 1
    grid = Grid3(max_size, max_size, max_size)
    for cur in data:
        grid[cur] = True
    for z in range(max_size):
        for y in range(max_size):
            for x in range(max_size):
                c = Vec3(x, y, z)
                if not grid[c] and not can_escape(grid, c):
                    grid[c] = True
                    #print(c)
    for cur in data:
        sides = 6
        for other in cur.cneighbors():
            if max(other) < max_size and grid[other]:
                sides -= 1
        # for other in data:
        #     if other != cur and abs(cur - other).manhattan() == 1:
        #         sides -= 1
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
