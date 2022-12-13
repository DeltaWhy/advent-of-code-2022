import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test13.txt"


def parse(lines):
    # return [line.strip() for line in lines]
    res = []
    for r1, r2 in isplit(lines):
        group = eval(r1), eval(r2)
        res.append(group)
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))

def is_ordered(left, right, _inner=False):
    """
    >>> is_ordered([1,1,3,1,1],[1,1,5,1,1])
    True
    >>> is_ordered([[1],[2,3,4]],[[1],4])
    True
    >>> is_ordered([9],[[8,7,6]])
    False
    >>> is_ordered([7,7,7,7],[7,7,7])
    False
    >>> is_ordered([],[3])
    True
    >>> is_ordered([[[]]],[[]])
    False
    >>> is_ordered([[],9],[1,1])
    True
    >>> is_ordered(\
    [[4, [1, []]], [8, 3, [[0, 2], [5, 2, 6], [7, 0, 10, 0], 2, [5, 7, 10, 2]], [[5, 9], 5, 10, [9, 7, 7]]]],\
    [[[], 9], [[[3, 2, 6, 3], [7, 8]], 10], [1]])
    False
    >>> is_ordered(\
    [[[], 9], [[[3, 2, 6, 3], [7, 8]], 10], [1]],\
    [[4, [1, []]], [8, 3, [[0, 2], [5, 2, 6], [7, 0, 10, 0], 2, [5, 7, 10, 2]], [[5, 9], 5, 10, [9, 7, 7]]]])
    True
    >>> is_ordered([[0], [[[1], 0, []]]], [[[[10, 8], [3,6,7]]]])
    True
    """
    #print(left)
    #print(right)
    if len(left) == 0:
        return True
    elif len(right) == 0:
        return False

    for i in range(max(len(left), len(right))):
        if i >= len(right):
            return False
        elif i >= len(left):
            return 'sentry' if _inner else True
        match left[i], right[i]:
            case [], []:
                continue
            case [], _:
                return 'sentry' if _inner else True
            case list(l), []:
                return False
            case list(l), list(r):
                x = is_ordered(l, r, True)
                #print(x)
                if not x:
                    return False
                elif x == 'sentry':
                    return 'sentry' if _inner else True
            case list(l), r:
                x = is_ordered(l, [r], True)
                #print(x)
                if not x:
                    return False
                elif x == 'sentry':
                    return 'sentry' if _inner else True
            case l, list(r):
                x = is_ordered([l], r, True)
                #print(x)
                if not x:
                    return False
                elif x == 'sentry':
                    return 'sentry' if _inner else True
            case l, r:
                if l < r:
                    return 'sentry' if _inner else True
                elif l > r:
                    return False
            case _:
                raise ValueError()
    return True if len(left) <= len(right) else False
        
def solve_part1(data):
    res = [is_ordered(l, r) for l, r in data]
    for l, r in data:
        if is_ordered(l, r) == is_ordered(r, l):
            print(l)
            print(r)
            raise ValueError((l, r))
    return sum((i+1 for i, (l, r) in with_index(data) if is_ordered(l, r)))

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 13

@dataclass
class Packet:
    l: list
    def __lt__(self, other):
        return is_ordered(self.l, other.l)
    def __eq__(self, other):
        return False

def solve_part2(data):
    data.append(([[2]], [[6]]))
    packets = [Packet(p) for p in itertools.chain.from_iterable(data)]
    res = [p.l for p in sorted(packets)]
    i1 = res.index([[2]]) + 1
    i2 = res.index([[6]]) + 1
    return i1 * i2


def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 140


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
