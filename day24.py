import fileinput
import itertools
import operator
import math
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from functools import reduce, cache
from util import *
from queue import PriorityQueue
from typing import Any


TEST_FILE = "test24.txt"


RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
WAIT = 4
SYMBOLS = '>v<^'
DIRECTIONS = [Vec2(1, 0), Vec2(0, 1), Vec2(-1, 0), Vec2(0, -1), Vec2(0, 0)]

def parse(lines):
    # return [line.strip() for line in lines]
    res = []
    for line in lines:
        row = line.strip()
        res.append(row)
    start = Vec2(res[0].index('.'), 0)
    goal = Vec2(res[-1].index('.'), len(res) - 1)
    blizzards = set()
    grid = Grid(res)
    for c in grid.coords():
        if grid[c] == '>':
            blizzards.add((c, RIGHT))
        elif grid[c] == 'v':
            blizzards.add((c, DOWN))
        elif grid[c] == '<':
            blizzards.add((c, LEFT))
        elif grid[c] == '^':
            blizzards.add((c, UP))
    return grid.rect(), start, blizzards, goal

def render(bounds, start, blizzards, goal, pos = None):
    g = Grid.of('.', w=bounds.w, h=bounds.h)
    for x in range(bounds.w):
        g[(x, 0)] = '#'
        g[(x, bounds.h - 1)] = '#'
    for y in range(bounds.h):
        g[(0, y)] = '#'
        g[(bounds.w - 1, y)] = '#'
    g[start] = '.'
    g[goal] = '.'
    if pos:
        g[pos] = 'E'
    for c, direction in blizzards:
        if g[c] == '.':
            g[c] = SYMBOLS[direction]
        elif g[c] in SYMBOLS:
            g[c] = '2'
        elif g[c] in '23456789':
            g[c] = chr(ord(g[c]) + 1)
        else:
            g[c] = '*'
    print()
    print(g.compact())

def advance(bounds, blizzards):
    res = set()
    for c, direction in blizzards:
        c += DIRECTIONS[direction]
        c2 = Vec2(((c.x - 1) % (bounds.w - 2)) + 1,
                    ((c.y - 1) % (bounds.h - 2)) + 1)
        res.add((c2, direction))
    return res

def test_parse():
    bounds, start, blizzards, goal = parse(fileinput.input(TEST_FILE))
    render(bounds, start, blizzards, goal, start)

def test_advance():
    bounds, start, blizzards, goal = parse(fileinput.input(TEST_FILE))
    for i in range(18):
        blizzards = advance(bounds, blizzards)
        #render(bounds, start, blizzards, goal)

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

def solve_part1(bounds, start, blizzards, goal):
    # steps repeat after LCM of height and width
    # precompute blizzard positions at each time
    mod = math.lcm(bounds.w - 2, bounds.h - 2)
    print('mod: ', mod)
    times = []
    for i in range(mod):
        times.append(blizzards)
        blizzards = advance(bounds, blizzards)
    res = float('inf')
    pruned = 0
    # earliest time we've seen each state
    visited = {}
    best_actions = {}

    q = PriorityQueue()
    q.put(PrioritizedItem((start - goal).manhattan(), (start, 0)))

    while q.qsize() > 0:
        item = q.get()
        pos, round = item.item
        if round < visited.get((pos, round % mod), float('inf')):
            visited[(pos, round % mod)] = round
        if pos == goal:
            print(pos, round)
            if round < res:
                res = round
            continue
        blizzards = times[(round + 1) % mod]
        # order matters a bit here - prefer not to backtrack
        possible_actions = [DOWN, RIGHT, WAIT, UP, LEFT]
        for action in possible_actions:
            next_pos = pos + DIRECTIONS[action]
            next_round = round + 1
            if next_pos not in bounds or next_pos.x <= 0 or next_pos.x >= (bounds.w - 1) or next_pos.y <= 0 and next_pos != start or next_pos.y >= (bounds.h - 1) and next_pos != goal:
                # invalid position
                continue
            if visited.get((next_pos, next_round % mod), float('inf')) <= next_round:
                # we've already visited this state earlier, prune
                pruned += 1
                continue
            if (next_pos - goal).manhattan() + round > res:
                # we already know a better solution than the best case for this state
                pruned += 1
                continue
            if next_pos not in [b[0] for b in blizzards]:
                q.put(PrioritizedItem((next_pos - goal).manhattan(), (next_pos, next_round)))
    return res

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(*data) == 18

def solve_part2(data):
    for line in data:
        pass

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == None


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(*data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
