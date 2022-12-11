import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from util import *
from pathlib import PosixPath


TEST_FILE = "test07.txt"


def solve_part1(lines):
    tree = Counter()
    all_dirs = set()
    pwd = PosixPath('/')
    for line in lines:
        match line.strip().split():
            case ['$', 'ls']:
                continue
            case ['$', 'cd', d]:
                if d.startswith('/'):
                    pwd = PosixPath(d)
                elif d == '..':
                    pwd = pwd.parent
                else:
                    pwd = pwd / d
                all_dirs.add(pwd)
            case ['dir', d]:
                all_dirs.add(pwd / d)
            case [size_s, name]:
                size = int(size_s)
                tree[pwd / name] = size
                dirs = str(pwd).split('/')
                print(pwd, list(pwd.parents))
                for d in [pwd] + list(pwd.parents):
                    tree[d] += size
    print(all_dirs)
    print(tree)
    res = sum((tree[x] for x in all_dirs if tree[x] < 100000))
    return all_dirs, tree, res

def test_solve_part1():
    all_dirs, tree, total = solve_part1(fileinput.input(TEST_FILE))
    assert total == 95437

def solve_part2(lines):
    all_dirs, tree, res = solve_part1(lines)
    free = 70000000 - tree[PosixPath('/')]
    print(free)
    needed = 30000000 - free
    print(needed)
    l = list(sorted((tree[x] for x in tree if x in all_dirs)))
    print(l)
    for x in l:
        if x >= needed:
            return x
    assert False

def test_solve_part2():
    assert solve_part2(fileinput.input(TEST_FILE)) == 24933642


if __name__ == '__main__':
    lines1, lines2 = itertools.tee(fileinput.input())
    part1 = solve_part1(lines1)
    part2 = solve_part2(lines2)
    print(part1)
    print(part2)
