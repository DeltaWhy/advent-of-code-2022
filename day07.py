import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from util import *


TEST_FILE = "test07.txt"


def solve_part1(lines):
    tree = Counter()
    all_dirs = set()
    pwd = '/'
    for line in lines:
        if line.startswith('$'):
            # command
            parts = line.strip().split()
            if parts[1] == 'ls':
                continue
            d = parts[2]
            if d == '..':
                pwd = '/'.join(pwd.split('/')[:-1])
                if not pwd:
                    pwd = '/'
            elif d.startswith('/'):
                pwd = d
            else:
                pwd = pwd.rstrip('/') + '/' + d
            print(pwd)
            all_dirs.add(pwd)
        else:
            # listing
            parts = line.strip().split()
            if parts[0] == 'dir':
                all_dirs.add(pwd.rstrip('/') + '/' + parts[1])
            else:
                size = int(parts[0])
                name = parts[1]
                tree[pwd.rstrip('/') + '/' + name] = size
                dirs = pwd.split('/')
                print(name)
                for i in range(len(dirs)):
                    d = '/'.join(dirs[0:i+1])
                    print(d)
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
    free = 70000000 - tree['']
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
    assert solve_part2(fileinput.input(TEST_FILE)) == 23352670


if __name__ == '__main__':
    lines1, lines2 = itertools.tee(fileinput.input())
    part1 = solve_part1(lines1)
    part2 = solve_part2(lines2)
    print(part1)
    print(part2)
