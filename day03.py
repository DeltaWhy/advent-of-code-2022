import fileinput
import itertools
from util import groups


TEST_FILE = "test03.txt"


def solve_part1(lines):
    sum = 0
    for line in lines:
        sack = line.strip()
        half = int(len(sack)/2)
        p1 = sack[0:half]
        p2 = sack[half:]
        assert p1 + p2 == sack
        common = set(p1).intersection(set(p2))
        assert len(common) == 1
        sum += prio(common.pop())
    return sum

def prio(item):
    """
    >>> prio('a')
    1
    >>> prio('z')
    26
    >>> prio('A')
    27
    >>> prio('Z')
    52
    """
    if 'a' <= item <= 'z':
        return ord(item) - ord('a') + 1
    elif 'A' <= item <= 'Z':
        return ord(item) - ord('A') + 27
    else:
        raise ValueError()

def test_solve_part1():
    assert solve_part1(fileinput.input(TEST_FILE)) == 157

def solve_part2(lines):
    sum = 0
    for group in groups(map(lambda x: x.strip(), lines), 3):
        badgeSet = set(group[0]).intersection(set(group[1])).intersection(set(group[2]))
        assert len(badgeSet) == 1
        sum += prio(badgeSet.pop())
    return sum

def test_solve_part2():
    assert solve_part2(fileinput.input(TEST_FILE)) == 70


if __name__ == '__main__':
    lines1, lines2 = itertools.tee(fileinput.input())
    part1 = solve_part1(lines1)
    part2 = solve_part2(lines2)
    print(part1)
    print(part2)
