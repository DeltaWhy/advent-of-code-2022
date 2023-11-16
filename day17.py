import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *
import pytest


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

def simulate(data, grid, rounds, n_rock, n_move):
    orig_height = len(grid)
    for i in range(rounds):
        rock = rocks[n_rock]
        n_rock = (n_rock + 1) % len(rocks)
        pos = Vec2(2, len(grid)-1)
        while True:
            move = data[n_move]
            n_move = (n_move + 1) % len(data)
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
    return n_rock, n_move, len(grid) - orig_height

def solve_part2(data):
    grid = Grid.of('.', 7, 4)
    n_rock = 0
    n_move = 0
    known_cycles = {}
    for i in range(1000000000000//len(rocks)):
        # initial setup
        n_rock, next_move, added_height = simulate(data, grid, len(rocks), n_rock, n_move)
        #print(f'{n_move=} {added_height=}')
        known_cycles[n_move] = added_height
        n_move = next_move
        if next_move in known_cycles:
            break
    print(f'start new cycle at {i=} {n_move=}')
    i0 = i
    repeat_move = next_move
    grid0 = Grid(grid)
    for i in range(i0 + 1, 1000000000000//len(rocks)):
        # find cycle length
        n_rock, next_move, added_height = simulate(data, grid, len(rocks), n_rock, n_move)
        #print(f'{n_move=} {added_height=}')
        known_cycles[n_move] = added_height
        n_move = next_move
        if next_move == repeat_move:
            break
    print(f'repeat at {i=} {n_move=}')
    cycle_length = i - i0
    print(f'{cycle_length=}')
    added_height_per_cycle = len(grid) - len(grid0)
    print(f'{added_height_per_cycle=}')
    height_after_first_cycle = len(grid) - 4
    print(f'{height_after_first_cycle=}')
    # do full cycles
    remaining = 1000000000000 // len(rocks) - i - 1
    remaining_full_cycles = remaining // cycle_length
    height = height_after_first_cycle + added_height_per_cycle * remaining_full_cycles
    remaining -= remaining_full_cycles * cycle_length
    print(f'{remaining=}')
    for i in range(remaining):
        n_rock, n_move, added_height = simulate(data, grid, len(rocks), n_rock, n_move)
        height += added_height
    return height

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 1514285714288


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
