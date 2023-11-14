import fileinput
import itertools
import operator
import re
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test22.txt"


def parse(lines):
    lines = list(lines)
    grid = lines[0:-2]
    instructions = lines[-1]
    width = max((len(line) for line in grid)) - 1
    res = []
    for line in grid:
        line = line.replace('\n', '')
        if len(line) < width:
            line = line + ' ' * (width - len(line))
        res.append(line)
    ops = []
    while instructions:
        if instructions[0] in ('L', 'R'):
            ops.append(instructions[0])
            instructions = instructions[1:]
        else:
            match = re.match('^([0-9]+)(.*)$', instructions)
            if not match:
                raise ValueError()
            ops.append(int(match[1]))
            instructions = match[2]
    return Grid(res), ops

def test_parse():
    grid, instructions = parse(fileinput.input(TEST_FILE))
    start = grid[0].index('.')
    print(start)
    print(grid.compact())
    print(instructions)

# right, down, left, up
DIRECTIONS = [Vec2(1, 0), Vec2(0, 1), Vec2(-1, 0), Vec2(0, -1)]
SYMBOLS = '>v<^'

def wrap(grid: Grid, pos: Vec2, facing: int) -> Vec2:
    if facing == 0:
        # left
        for i, c in with_index(grid[pos.y]):
            if c != ' ':
                return Vec2(i, pos.y)
    elif facing == 2:
        # right
        for i in range(len(grid[pos.y]) - 1, -1, -1):
            if grid[(i, pos.y)] != ' ':
                return Vec2(i, pos.y)
    elif facing == 1:
        # down
        pos = Vec2(pos.x, 0)
        while grid[pos] == ' ':
            pos += pos.direction('D')
        return pos
    elif facing == 3:
        # up
        pos = Vec2(pos.x, len(grid) - 1)
        while grid[pos] == ' ':
            pos += pos.direction('U')
        return pos

def solve_part1(grid, instructions):
    visited = Grid(grid)
    pos = Vec2(grid[0].index('.'), 0)
    facing = 0

    for op in instructions:
        print(pos, facing, op)
        if op == 'R':
            facing = (facing + 1) % 4
        elif op == 'L':
            facing = (facing - 1) % 4
        else:
            for i in range(op):
                nextpos = pos + DIRECTIONS[facing]
                nextpos = Vec2(nextpos.x % len(grid[0]), nextpos.y % len(grid))
                if grid[nextpos] == '#':
                    break
                elif grid[nextpos] == '.':
                    pos = nextpos
                    visited[pos] = SYMBOLS[facing]
                elif grid[nextpos] == ' ':
                    #import pdb; pdb.set_trace()
                    nextpos = wrap(grid, pos, facing)
                    if grid[nextpos] == '#':
                        break
                    pos = nextpos
                    visited[pos] = SYMBOLS[facing]
        visited[pos] = SYMBOLS[facing]
        # print()
        # print(visited.compact())

    # print()
    # print(visited.compact())
    row = pos.y + 1
    column = pos.x + 1
    return 1000 * row + 4 * column + facing

def test_solve_part1():
    grid, instructions = parse(fileinput.input(TEST_FILE))
    assert solve_part1(grid, instructions) == 6032

def simplified(grid, size=50):
    res = Grid.of(' ', len(grid[0]) // size, len(grid) // size)
    print(res)
    for y in range(0, len(grid), size):
        for x in range(0, len(grid[0]), size):
            res[(x // size, y // size)] = grid[(x, y)]
    return res

def fold(grid, size=50):
    res = {'F': (None, None),
           'L': (None, None),
           'R': (None, None),
           'B': (None, None),
           'U': (None, None),
           }
    print(simplified(grid, size).compact())
    pos = Vec2(grid[0].index('.'), 0)
    visited = set()
    def visit(pos, facing, face):
        if grid[pos] == ' ' or pos in visited:
            return
        res[face] = (Rect(pos, w=size, h=size), facing)
        visited.add(pos)
        if pos.x > 0:
            # check left
            visit(Vec2(pos.x - size, pos.y), facing, face)
        if pos.x + size < len(grid[0]):
            # check right
            visit(Vec2(pos.x + size, pos.y), facing, face)
        if pos.y > 0:
            # check up
            visit(Vec2(pos.x, pos.y - size), facing, face)
        if pos.y + size < len(grid):
            # check down
            visit(Vec2(pos.x, pos.y + size), facing, face)
    visit(pos, 0, 'F')
    print(res)
    #folded = Grid(grid)
    #for c in Rect(pos, w=size, h=size).coords():
    #    folded[c] = 'F'
    #if pos.x + size < len(grid[0]) and grid[(pos.x + size, pos.y)] != ' ':
    #    # R right of F
    #    if pos.x + 2*size < len(grid[0]) and grid[(pos.x + 2*size, pos.y)] != ' ':
    #        # B right of R
    #        pass

    #print(folded.compact())

def test_fold():
    grid, instructions = parse(fileinput.input(TEST_FILE))
    print(fold(grid, size=4))

def solve_part2(grid, instructions):
    pass

def test_solve_part2():
    grid, instructions = parse(fileinput.input(TEST_FILE))
    assert solve_part2(grid, instructions) == None


if __name__ == '__main__':
    lines = list(fileinput.input())
    grid, instructions = parse(lines)
    part1 = solve_part1(grid, instructions)
    print(part1)
    grid, instructions = parse(lines)
    part2 = solve_part2(grid, instructions)
    print(part1)
    print(part2)
