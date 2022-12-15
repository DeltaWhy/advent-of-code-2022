import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test15.txt"


def parse(lines):
    # return [line.strip() for line in lines]
    res = []
    for line in lines:
        sx, sy, bx, by = numbers(line)
        res.append((Vec2(sx, sy), Vec2(bx, by)))
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))
    assert res[0][1].x == -2

def find_range(p, dist, row):
    width = dist - abs(p.y - row)
    if width < 0:
        return None
    return range(p.x - width, p.x + width + 1)

class Ranges:
    def __init__(self, iterable=None):
        self.ranges = []
        if iterable:
            for r in iterable:
                self.add(r)

    def __iter__(self):
        return self.ranges.__iter__()

    def add(self, r, _recurse=False):
        new_ranges = list(sorted([r]+self.ranges, key=lambda x: x.start))
        stack = [new_ranges[0]]
        for x in new_ranges[1:]:
            if stack[-1].start <= x.start <= stack[-1].stop:
                stack[-1] = range(stack[-1].start, max(stack[-1].stop, x.stop))
            else:
                stack.append(x)
        self.ranges = stack

    def __repr__(self):
        return self.ranges.__repr__()

    def __contains__(self, other):
        if isinstance(other, range):
            for r in self.ranges:
                if other.start in r and other.stop - 1 in r:
                    break
            else:
                return False
            return True
        else:
            return False

def solve_part1(data, row):
    excluded = Ranges()
    for sensor, beacon in data:
        dist = (sensor - beacon).manhattan()
        #print(sensor, beacon, dist)
        exclude = find_range(sensor, dist, row)
        if exclude:
            excluded.add(exclude)
    #print(excluded.ranges)
    #print(excluded)
    beacons_in_row = set()
    for _, beacon in data:
        if beacon.y == row:
            for exclude in excluded:
                if beacon.x in exclude:
                    #print(beacon)
                    beacons_in_row.add(beacon)
                    break
    return sum((len(x) for x in excluded)) - len(beacons_in_row)

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data, 10) == 26

def solve_part2(data, bound):
    data = [(sensor, (sensor - beacon).manhattan()) for sensor, beacon in data]
    for row in range(0, bound+1):
        if row % 1000 == 0:
            print(row)
        excluded = Ranges()
        for sensor, dist in data:
            exclude = find_range(sensor, dist, row)
            if exclude:
                excluded.add(exclude)
        if range(0, bound+1) not in excluded:
            #print(row)
            print(excluded)
            x = excluded.ranges[0].stop
            print((x,row))
            return x * 4000000 + row

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data, 20) == 56000011


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data, 2000000)
    data = parse(lines)
    part2 = solve_part2(data, 4000000)
    print(part1)
    print(part2)
