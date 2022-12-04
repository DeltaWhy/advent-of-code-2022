import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from util import *


TEST_FILE = "test04.txt"


def solve_part1(lines):
    # fully contained
    sum = 0
    for line in lines:
        elf1, _, elf2 = line.strip().partition(',')
        start1, _, end1 = elf1.partition('-')
        start2, _, end2 = elf2.partition('-')
        if int(start1) <= int(start2) and int(end1) >= int(end2):
            sum += 1
        elif int(start2) <= int(start1) and int(end2) >= int(end1):
            sum += 1
    return sum

def test_solve_part1():
    assert solve_part1(fileinput.input(TEST_FILE)) == 2

def solve_part2(lines):
    sum = 0
    for line in lines:
        elf1, _, elf2 = line.strip().partition(',')
        start1, _, end1 = elf1.partition('-')
        start2, _, end2 = elf2.partition('-')
        r1 = range(int(start1), int(end1)+1)
        r2 = range(int(start2), int(end2)+1)
        if int(start1) in r2 or int(end1) in r2 or int(start2) in r1 or int(end2) in r1:
            sum += 1
    return sum


def test_solve_part2():
    assert solve_part2(fileinput.input(TEST_FILE)) == 4


if __name__ == '__main__':
    lines1, lines2 = itertools.tee(fileinput.input())
    part1 = solve_part1(lines1)
    part2 = solve_part2(lines2)
    print(part1)
    print(part2)
