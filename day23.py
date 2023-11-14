import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test23.txt"


def parse(lines):
    # return [line.strip() for line in lines]
    res = []
    for line in lines:
        row = line.strip()
        res.append(row)
    return Grid(res)

def test_parse():
    res = parse(fileinput.input(TEST_FILE))
    print()
    print(res.compact())

ROUNDS = [
        [(0, -1), (-1, -1), (1, -1)],  # north
        [(0, 1), (-1, 1), (1, 1)],  # south
        [(-1, 0), (-1, -1), (-1, 1)],  # west
        [(1, 0), (1, -1), (1, 1)],  # east
        ]
def advance(grid, round):
    elves = []
    for c in grid.coords():
        if grid[c] == '#':
            elves.append(c)
    proposed = []
    for i, c in with_index(elves):
        if all((grid.get(d, '.') == '.' for d in c.neighbors())):
            # no adjacents
            proposed.append(c)
            continue
        for r in range(4):
            ds = ROUNDS[(round + r) % 4]
            if all((grid.get(c + d, '.') == '.' for d in ds)):
                proposed.append(c + ds[0])
                break
        else:
            # can't move anywhere
            proposed.append(c)
    if any((c not in grid for c in proposed)):
        # grow the grid
        res = Grid.of('.', w=len(grid[0]) + 2, h = len(grid) + 2)
        elves = [c + (1, 1) for c in elves]
        proposed = [c + (1, 1) for c in proposed]
    else:
        res = Grid.of('.', w=len(grid[0]), h=len(grid))
    for i, c in with_index(proposed):
        for j in range(len(proposed)):
            if i == j:
                continue
            if proposed[i] == proposed[j]:
                # conflict
                res[elves[i]] = '#'
                break
        else:
            res[c] = '#'

    return res

def test_advance():
    given = """
        .....
        ..##.
        ..#..
        .....
        ..##.
        .....
    """.strip().split('\n')
    grid = parse(given)
    print()
    print(grid.compact())
    grid = advance(grid, 0)
    expected = """
        ..##.
        .....
        ..#..
        ...#.
        ..#..
        .....
    """.strip().split('\n')
    assert grid.compact().split('\n') == [line.strip() for line in expected]
    expected = """
        .....
        ..##.
        .#...
        ....#
        .....
        ..#..
    """.strip().split('\n')
    grid = advance(grid, 1)
    assert grid.compact().split('\n') == [line.strip() for line in expected]
    expected = """
        ..#..
        ....#
        #....
        ....#
        .....
        ..#..
    """.strip().split('\n')
    grid = advance(grid, 2)
    assert grid.compact().split('\n') == [line.strip() for line in expected]
    assert grid == advance(grid, 3)

def test_advance2():
    given = """
        ..##.
        .....
        ..#..
        .###.
        ..#..
    """.strip().split('\n')
    grid = parse(given)
    print()
    print(grid.compact())
    grid = advance(grid, 0)
    expected = """
        ...##..
        .......
        ...#...
        .......
        .#.#.#.
        .......
        ...#...
    """.strip().split('\n')
    assert grid.compact().split('\n') == [line.strip() for line in expected]

def solve_part1(grid):
    for i in range(10):
        grid = advance(grid, i)
        print()
        print(grid.compact())
    elves = []
    for c in grid.coords():
        if grid[c] == '#':
            elves.append(c)
    rect = Rect(min((c.x for c in elves)), min((c.y for c in elves)),
                max((c.x for c in elves)), max((c.y for c in elves)))
    print(rect)
    res = 0
    for c in rect.coords():
        if grid[c] == '.':
            res += 1
    return res

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 110

def solve_part2(grid):
    prev = grid
    for i in range(9999):
        print(i)
        grid = advance(prev, i)
        if grid == prev:
            break
        prev = grid
    return i + 1

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 20


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
