import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from util import *


TEST_FILE = "test06.txt"


def solve_part1(line):
    buf = line[0:4]
    i = 4
    while len(set(buf)) != 4:
        i += 1
        buf = line[i-4:i]
    return i

def test_solve_part1():
    assert solve_part1('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 7
    assert solve_part1('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
    assert solve_part1('nppdvjthqldpwncqszvftbrmjlhg') == 6
    assert solve_part1('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
    assert solve_part1('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11

def solve_part2(line):
    buf = line[0:14]
    i = 14
    while len(set(buf)) != 14:
        i += 1
        buf = line[i-14:i]
    return i

def test_solve_part2():
    assert solve_part2('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 19
    assert solve_part2('bvwbjplbgvbhsrlpgdmjqwftvncz') == 23
    assert solve_part2('nppdvjthqldpwncqszvftbrmjlhg') == 23
    assert solve_part2('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 29
    assert solve_part2('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 26


if __name__ == '__main__':
    lines1, lines2 = itertools.tee(fileinput.input())
    part1 = solve_part1(''.join(lines1))
    part2 = solve_part2(''.join(lines2))
    print(part1)
    print(part2)
