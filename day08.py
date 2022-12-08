import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from util import *


TEST_FILE = "test08.txt"


def solve_part1(lines):
    grid = [[int(c) for c in line.strip()] for line in lines]
    # skip outer ring
    visible = 2 * len(grid[0]) + 2 * (len(grid) - 2)
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            done = False
            for y2 in range(0, y):
                # up
                if grid[y2][x] >= grid[y][x]:
                    break
            else:
                visible += 1
                done = True
            if done:
                continue
            for y2 in range(y+1, len(grid)):
                # down
                if grid[y2][x] >= grid[y][x]:
                    break
            else:
                visible += 1
                done = True
            if done:
                continue
            for x2 in range(0, x):
                # left
                if grid[y][x2] >= grid[y][x]:
                    break
            else:
                visible += 1
                done = True
            if done:
                continue
            for x2 in range(x+1, len(grid[y])):
                # right
                if grid[y][x2] >= grid[y][x]:
                    break
            else:
                visible += 1
                done = True
    return visible

def test_solve_part1():
    assert solve_part1(fileinput.input(TEST_FILE)) == 21

def scenic_score(grid, x, y):
    up = 0
    down = 0
    left = 0
    right = 0
    for y2 in range(y-1, -1, -1):
        up += 1
        if grid[y2][x] >= grid[y][x]:
            break
    for y2 in range(y+1, len(grid)):
        down += 1
        if grid[y2][x] >= grid[y][x]:
            break
    for x2 in range(x-1, -1, -1):
        left += 1
        if grid[y][x2] >= grid[y][x]:
            break
    for x2 in range(x+1, len(grid[y])):
        right += 1
        if grid[y][x2] >= grid[y][x]:
            break
    return up * down * left * right

def solve_part2(grid):
    l = []
    for y in range(1, len(grid)-1):
        for x in range(1, len(grid[0])-1):
            l.append(scenic_score(grid, x, y))
    return max(l)

def test_solve_part2():
    grid = [[int(c) for c in line.strip()] for line in fileinput.input(TEST_FILE)]
    assert scenic_score(grid, 2, 1) == 4
    assert scenic_score(grid, 2, 3) == 8
    assert solve_part2(grid) == 8


if __name__ == '__main__':
    lines1, lines2 = itertools.tee(fileinput.input())
    part1 = solve_part1(lines1)
    grid = [[int(c) for c in line.strip()] for line in lines2]
    part2 = solve_part2(grid)
    print(part1)
    print(part2)
