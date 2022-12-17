import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test17.txt"

rocks = [
        Grid(['@@@@']),
        Grid(['.@.',
              '@@@',
              '.@.']),
        Grid(['@@@',
              '..@',
              '..@']),
        Grid(['@','@','@','@']),
        Grid(['@@',
              '@@'])
]

def parse(lines):
    return ''.join((line.strip() for line in lines))

def test_parse():
    res = parse(fileinput.input(TEST_FILE))

def collide(grid, rock, pos):
    for p in rock.coords():
        if rock[p] != '.' and (pos+p) in grid.rect() and grid[pos+p] != '.':
            return True
    return False

def merge(grid, rock, pos, sym='#'):
    for p in rock.coords():
        if rock[p] != '.':
            while (p+pos).y >= len(grid):
                grid.append(list('.......'))
            grid[p+pos] = sym
    while grid[-4] != list('.......'):
        grid.append(list('.......'))

def pr(grid, rock, pos):
    g2 = grid[:]
    merge(g2, rock, pos, '@')
    print()
    print(g2[::-1].compact())

def solve_part1(data):
    grid = Grid.of('.', 7, 4)
    rock_iter = itertools.cycle(rocks)
    move_iter = itertools.cycle(data)
    offset = 0
    for i in range(2022):
        rock = next(rock_iter)
        pos = Vec2(2, len(grid)-1)
        while True:
            move = next(move_iter)
            if move == '<' and pos.x > 0:
                pos -= (1, 0)
                if collide(grid, rock, pos):
                    pos += (1, 0)
                #pr(grid, rock, pos)
            elif move == '>' and pos.x + len(rock[0]) < len(grid[0]):
                pos += (1, 0)
                if collide(grid, rock, pos):
                    pos -= (1, 0)
                #pr(grid, rock, pos)
            pos -= (0, 1)
            if pos.y < 0:
                pos += (0, 1)
                merge(grid, rock, pos)
                break
            if collide(grid, rock, pos):
                pos += (0, 1)
                merge(grid, rock, pos)
                break
            #pr(grid, rock, pos)
        # print()
        # print(grid[::-1].compact())
        # if len(grid) > 1000:
        #     offset += len(grid) - 500
        #     grid = grid[-500:]
    while grid[-1] == list('.......'):
        del grid[-1]
    return len(grid) + offset

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 3068

def line(n, sym='#'):
    """
    >>> line(1)
    '......#'
    >>> line(10)
    '...#.#.'
    """
    return ''.join([sym if (n>>(6-i))%2 else '.' for i in range(7)])

def pr2(grid, rock=None, pos=None):
    g = Grid([line(n) for n in grid])
    if rock:
        r = Grid([line(n) for n in rock])
        merge(g, r, Vec2(0, pos.y), '@')
    print()
    print(g[::-1].compact())

def collide2(grid, rock, pos):
    for y in range(len(rock)):
        if y + pos.y >= len(grid):
            return False
        if grid[y + pos.y] & rock[y]:
            return True
    return False

def merge2(grid, rock, pos):
    for y in range(len(rock)):
        while y + pos.y >= len(grid):
            grid.append(0)
        grid[y + pos.y] = grid[y + pos.y] | rock[y]
    while grid[-4] != 0:
        grid.append(0)

rocks2 = [
        [0b1111000],
        [0b0100000, 0b1110000, 0b0100000],
        [0b1110000, 0b0010000, 0b0010000],
        [0b1000000, 0b1000000, 0b1000000, 0b1000000],
        [0b1100000, 0b1100000]]

def solve_part2(data):
    grid = [0]*4
    pr2(grid)
    rock_iter = itertools.cycle(rocks2)
    move_iter = itertools.cycle(data)
    offset = 0
    for i in range(1000000000000):
        if i % 2000 == 0:
            print(i)
        rock = next(rock_iter)
        pos = Vec2(2, len(grid)-1)
        rock = [n>>2 for n in rock]
        while True:
            move = next(move_iter)
            if move == '<' and pos.x > 0:
                pos -= (1, 0)
                rock = [n<<1 for n in rock]
                if collide2(grid, rock, pos):
                    pos += (1, 0)
                    rock = [n>>1 for n in rock]
                #pr2(grid, rock, pos)
            elif move == '>' and all((n%2==0 for n in rock)):
                pos += (1, 0)
                rock = [n>>1 for n in rock]
                if collide2(grid, rock, pos):
                    pos -= (1, 0)
                    rock = [n<<1 for n in rock]
                #pr2(grid, rock, pos)
            pos -= (0, 1)
            if pos.y < 0:
                pos += (0, 1)
                merge2(grid, rock, pos)
                break
            if collide2(grid, rock, pos):
                pos += (0, 1)
                merge2(grid, rock, pos)
                break
            #pr2(grid, rock, pos)
        #print()
        #print(grid[::-1].compact())
        #pr2(grid)
        if len(grid) > 1000:
            offset += len(grid) - 500
            grid = grid[-500:]
    while grid[-1] == 0:
        del grid[-1]
    return len(grid) + offset

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 3068


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
