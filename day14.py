import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test14.txt"


def parse(lines):
    # return [line.strip() for line in lines]
    res = []
    for line in lines:
        parts = lmap(lambda x: x.split(','), line.strip().split(' -> '))
        res.append([Vec2(int(x),int(y)) for x,y in parts])
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))
    #print(res)

def make_grid(paths, part2=False):
    max_x = max((max((p.x for p in path)) for path in paths))
    max_y = max((max((p.y for p in path)) for path in paths))
    min_x = min((min((p.x for p in path)) for path in paths))
    min_y = min((min((p.y for p in path)) for path in paths))
    if part2:
        max_y += 2
    grid = Grid.of('.', max_x+1, max_y+1)
    for path in paths:
        for p1, p2 in itertools.pairwise(path):
            if p1.x > p2.x or p1.y > p2.y:
                p2, p1 = p1, p2
            for p in Rect(p1, p2).coords():
                grid[p] = '#'
    if part2:
        for x in range(0, max_x+1):
            grid[(x, max_y)] = '#'
    return Rect(min_x, min_y, max_x, max_y), grid

def solve_part1(paths):
    rect, grid = make_grid(paths)
    #print()
    #print(grid[rect].compact())
    grains = 0
    while True:
        try:
            pos = Vec2(500, 0)
            while True:
                if grid[pos + (0, 1)] == '.':
                    pos += (0, 1)
                elif grid[pos + (-1, 1)] == '.':
                    pos += (-1, 1)
                elif grid[pos + (1, 1)] == '.':
                    pos += (1, 1)
                else:
                    # at rest
                    grains += 1
                    grid[pos] = 'o'
                    #print(grid[rect].compact())
                    break
        except IndexError:
            break
    return grains

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 24

def solve_part2(paths):
    rect, grid = make_grid(paths, True)
    #print()
    #print(grid[rect].compact())
    grains = 0
    offset = 0
    #print(rect)
    while True:
        pos = Vec2(500 + offset, 0)
        while True:
            if grid[pos + (0, 1)] == '.':
                pos += (0, 1)
            elif pos.x == 0:
                # shift the whole grid
                offset += 1
                pos = Vec2(pos.x+1, pos.y)
                grid = Grid([['.']+row for row in grid])
                grid[-1][0] = '#'
                rect = Rect(rect.x1+1, rect.y1, rect.x2+1, rect.y2)
                #print(grid[rect].compact())
                #print(rect)
                continue
            elif grid[pos + (-1, 1)] == '.':
                pos += (-1, 1)
            elif pos.x == rect.x2 + offset:
                # extend the grid
                grid = Grid([row+['.'] for row in grid])
                grid[-1][-1] = '#'
                rect = Rect(rect.x1, rect.y1, rect.x2+1, rect.y2)
                #print(grid[rect].compact())
                #print(rect)
                continue
            elif grid[pos + (1, 1)] == '.':
                pos += (1, 1)
            else:
                # at rest
                grains += 1
                grid[pos] = 'o'
                #print(grid[rect].compact())
                break
        if pos == Vec2(500 + offset, 0):
            break
    return grains

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 93


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
