import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque, namedtuple
from dataclasses import dataclass
from functools import reduce
from util import *


TEST_FILE = "test16.txt"


@dataclass
class Valve:
    id: str
    rate: int
    neighbors: list[str]

def parse(lines):
    # return [line.strip() for line in lines]
    valves = {}
    for line in lines:
        row = line.strip().split()
        id = row[1]
        rate = numbers(row[4])[0]
        neighbors = line.strip().partition('to valve')[2].replace('s ', '').replace(' ', '', -1).split(',')
        valves[id] = Valve(id, rate, neighbors)
    return valves

def test_parse():
    res = parse(fileinput.input(TEST_FILE))
    print(res)

State = namedtuple('State', ['time', 'pos', 'opened'])

def solve_part1(valves):
    max_value: dict[State, int] = {}
    best_action: dict[State, str] = {}
    def next_state(state: State, action: str):
        if action == 'open':
            return State(state.time + 1, state.pos, tuple(sorted([state.pos]+list(state.opened))))
        return State(state.time + 1, action, state.opened)

    all_open = tuple(sorted((x.id for x in valves.values() if x.rate != 0)))

    def next_actions(state: State):
        if state.opened == all_open:
            return []
        elif state.pos in state.opened:
            return valves[state.pos].neighbors
        elif valves[state.pos].rate == 0:
            return valves[state.pos].neighbors
        else:
            return ['open'] + valves[state.pos].neighbors

    def gain(state: State, action: str):
        if action == 'open':
            return valves[state.pos].rate * (30 - state.time - 1)
        else:
            return 0

    def dfs(state):
        #print(state)
        if state in max_value:
            return max_value[state]
        if state.time >= 30:
            max_value[state] = 0
            return 0
        actions = next_actions(state)
        if not actions:
            max_value[state] = 0
            return 0
        values = {}
        for action in actions:
            st = next_state(state, action)
            values[action] = gain(state, action) + dfs(st)
            #print(state, action, gain(state, action), values[action])
        best_action[state], max_value[state] = max(values.items(), key=lambda x: x[1])
        return max_value[state]

    dfs(State(0, 'AA', tuple()))
    # print(max_value)
    # retrace path
    st = State(0, 'AA', tuple())
    while st.time <= 30:
        if st not in best_action:
            break
        print(st, best_action.get(st))
        st = next_state(st, best_action.get(st))

    return max(max_value.values())

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 1651

def solve_part2(data):
    for line in data:
        pass

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == None


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
