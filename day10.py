import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from util import *


TEST_FILE = "test10.txt"


def parse(lines):
    # return [line.strip() for line in lines]
    res = []
    for line in lines:
        row = line.strip().split()
        if row[0] == 'noop':
            res.append((row[0], None))
        elif row[0] == 'addx':
            res.append((row[0], int(row[1])))
        else:
            raise ValueError(line)
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))

def execute(instructions):
    x = 1
    cycle = 0
    for op, arg in instructions:
        if op == 'noop':
            scan = cycle % 40
            cycle += 1
            px = '#' if x-1 <= scan <= x+1 else '.'
            yield x, px, scan
        elif op == 'addx':
            scan = cycle % 40
            cycle += 1
            px = '#' if x-1 <= scan <= x+1 else '.'
            yield x, px, scan
            scan = cycle % 40
            cycle += 1
            px = '#' if x-1 <= scan <= x+1 else '.'
            yield x, px, scan
            x += arg
    yield x, ''

def test_execute():
    instructions = parse("""noop
addx 3
addx -5""".split('\n'))
    values = list(map(lambda x: x[0], execute(instructions)))
    assert values == [1, 1, 1, 4, 4, -1]

def solve_part1(data):
    l = list(execute(data))
    vals = []
    for i in range(19, len(l), 40):
        vals.append(l[i][0] * (i+1))
    print(vals)
    return sum(vals)

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 13140

def solve_part2(data):
    l = list(execute(data))
    print(l)
    screen = '\n'.join([
            ''.join(line) for line in
            groups(map(lambda x: x[1], l), 40)])
    return screen

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data).strip() == """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
""".strip()


if __name__ == '__main__':
    data = parse(fileinput.input())
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
