import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test12.txt"


def parse(lines):
    return Grid((line.strip() for line in lines))

def test_parse():
    res = parse(fileinput.input(TEST_FILE))

def solve_part1(grid):
    rect = Rect(0, 0, w=len(grid[0])-1, h=len(grid)-1)
    for c, v in grid.items():
        if v == 'E':
            end = c
            break
    else:
        raise ValueError('No end found')
    for c, v in grid.items():
        if v == 'S':
            start = c
            break
    else:
        raise ValueError('No end found')
    grid[start] = 'a'
    grid[end] = 'z'
    h = [(0, start)]
    g = defaultdict(lambda: float('inf'))
    g[start] = 0
    import heapq
    while h:
        fv, pos = heapq.heappop(h)
        if pos == end:
            return g[pos]
        for neighbor in pos.cneighbors():
            if neighbor not in rect:
                continue
            if ord(grid[neighbor]) <= ord(grid[pos]) + 1:
                gv = g[pos] + 1
                if gv < g[neighbor]:
                    g[neighbor] = gv
                    heapq.heappush(h, (gv + (neighbor - end).manhattan(), neighbor))

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 31

def solve_part2(grid):
    rect = Rect(0, 0, w=len(grid[0])-1, h=len(grid)-1)
    for c, v in grid.items():
        if v == 'E':
            end = c
            break
    else:
        raise ValueError('No end found')
    grid[end] = 'z'
    all_starts = []
    for c, v in grid.items():
        if v == 'S' or v == 'a':
            all_starts.append(((c - end).manhattan(), c))
            grid[c] = 'a'
    h = [(0, start[1]) for start in sorted(all_starts)]
    g = defaultdict(lambda: float('inf'))
    for _, start in all_starts:
        g[start] = 0
    import heapq
    while h:
        fv, pos = heapq.heappop(h)
        if pos == end:
            return g[pos]
        for neighbor in pos.cneighbors():
            if neighbor not in rect:
                continue
            if ord(grid[neighbor]) <= ord(grid[pos]) + 1:
                gv = g[pos] + 1
                if gv < g[neighbor]:
                    g[neighbor] = gv
                    heapq.heappush(h, (gv + (neighbor - end).manhattan(), neighbor))


def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 29


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
