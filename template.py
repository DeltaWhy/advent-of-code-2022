import fileinput
import itertools


def solve(lines):
    lines1, lines2 = itertools.tee(lines)
    part1 = None
    part2 = None
    for line in lines1:
        pass
    for line in lines2:
        pass
    return part1, part2

def test_solve():
    assert solve(fileinput.input("testXX.txt")) == (None, None)

if __name__ == '__main__':
    part1, part2 = solve(fileinput.input())
    print(part1)
    print(part2)
