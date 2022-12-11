from dataclasses import dataclass
import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque
from util import *
from functools import reduce


TEST_FILE = "test11.txt"


@dataclass
class Monkey:
    index: int
    inventory: deque[int]
    operation: str
    operand: int
    test: int
    next_true: int
    next_false: int
    inspected: int = 0
    def operate(self, part2 = False, lcm = None):
        for i in range(len(self.inventory)):
            self.inspected += 1
            n = self.inventory[i]
            if self.operation == '+':
                n += self.operand
            elif self.operation == '*':
                n *= self.operand
            elif self.operation == '**':
                n = n ** self.operand
            else:
                raise ValueError(self.operation)
            if part2:
                self.inventory[i] = n % lcm
            elif lcm:
                self.inventory[i] = int(n/3) % lcm
            else:
                self.inventory[i] = int(n/3)

    def next(self):
        while self.inventory:
            n = self.inventory.popleft()
            if n % self.test == 0:
                yield (n, self.next_true)
            else:
                yield (n, self.next_false)

def parse(lines):
    groups = isplit(lines)
    monkeys = []
    for group in groups:
        index = int(group[0].split()[1].partition(':')[0])
        inventory = deque([int(x) for x in group[1].partition(': ')[2].split(', ')])
        if '+ old' in group[2]:
            operation = '*'
            operand = 2
        elif '* old' in group[2]:
            operation = '**'
            operand = 2
        elif '+' in group[2]:
            operation = '+'
            operand = int(group[2].strip().split()[-1])
        elif '*' in group[2]:
            operation = '*'
            operand = int(group[2].strip().split()[-1])
        else:
            raise ValueError(group[2])
        test = int(group[3].strip().split()[-1])
        next_true = int(group[4].strip().split()[-1])
        next_false = int(group[5].strip().split()[-1])
        monkeys.append(Monkey(index, inventory, operation, operand, test, next_true, next_false))

    return monkeys

def test_parse():
    res = parse(fileinput.input(TEST_FILE))

def solve_part1(monkeys):
    import math
    lcm = math.lcm(*([m.test for m in monkeys] + [m.operand for m in monkeys if m.operation == '*']))
    # print(lcm)
    for round in range(20):
        for monkey in monkeys:
            monkey.operate(False, lcm)
            for item, next in monkey.next():
                monkeys[next].inventory.append(item)
    # print(monkeys)
    top = list(sorted(monkeys, key=lambda x: x.inspected, reverse=True))
    return top[0].inspected * top[1].inspected

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 10605

def solve_part2(monkeys):
    import math
    lcm = math.lcm(*([m.test for m in monkeys] + [m.operand for m in monkeys if m.operation == '*']))
    # print(lcm)
    for round in range(10000):
        for monkey in monkeys:
            monkey.operate(True, lcm)
            for item, next in monkey.next():
                monkeys[next].inventory.append(item)
    # print(monkeys)
    top = list(sorted(monkeys, key=lambda x: x.inspected, reverse=True))
    return top[0].inspected * top[1].inspected

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 2713310158


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
