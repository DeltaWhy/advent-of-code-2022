import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque, namedtuple
from dataclasses import dataclass
from functools import reduce, cache
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

    @cache
    def dfs(state):
        #print(state)
        if state.time >= 30:
            return 0
        actions = next_actions(state)
        if not actions:
            return 0
        values = {}
        for action in actions:
            st = next_state(state, action)
            values[action] = gain(state, action) + dfs(st)
            #print(state, action, gain(state, action), values[action])
        best_action[state], ans = max(values.items(), key=lambda x: x[1])
        return ans

    ans = dfs(State(0, 'AA', tuple()))
    # retrace path
    st = State(0, 'AA', tuple())
    while st.time <= 30:
        if st not in best_action:
            break
        print(st, best_action.get(st))
        st = next_state(st, best_action.get(st))
    return ans

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 1651

State2 = namedtuple('State2', ['time', 'pos1', 'pos2', 'opened'])

def solve_part2(valves):
    best_action: dict[State, str] = {}
    def next_state(state: State2, actions: tuple[str, str]):
        opened = list(state.opened)
        pos1, pos2 = state.pos1, state.pos2
        if actions[0] == 'open':
            opened.append(pos1)
        elif actions[0]:
            pos1 = actions[0]
        if actions[1] == 'open':
            opened.append(pos2)
        elif actions[1]:
            pos2 = actions[1]
        opened = tuple(sorted(opened))
        if pos1 > pos2:
            pos1, pos2 = pos2, pos1
        return State2(state.time + 1, pos1, pos2, opened)

    all_open = tuple(sorted((x.id for x in valves.values() if x.rate != 0)))

    def next_actions(state: State):
        if state.opened == all_open:
            return []
        if state.pos1 in state.opened or valves[state.pos1].rate == 0:
            actions1 = valves[state.pos1].neighbors
        else:
            actions1 = ['open'] + valves[state.pos1].neighbors
        if state.pos2 in state.opened or valves[state.pos2].rate == 0:
            actions2 = valves[state.pos2].neighbors
        else:
            actions2 = ['open'] + valves[state.pos2].neighbors
        return list(itertools.product(actions1, actions2))

    def gain(state: State, actions: tuple[str, str]):
        res = 0
        if state.pos1 == state.pos2 and 'open' in actions:
            return valves[state.pos1].rate * (26 - state.time - 1)
        if actions[0] == 'open':
            res += valves[state.pos1].rate * (26 - state.time - 1)
        if actions[1] == 'open':
            res += valves[state.pos2].rate * (26 - state.time - 1)
        return res

    @cache
    def dfs(state):
        #print(state)
        if state.time >= 26:
            return 0
        actions = next_actions(state)
        if not actions:
            return 0
        values = {}
        for action in actions:
            st = next_state(state, action)
            values[action] = gain(state, action) + dfs(st)
            print(state, action, gain(state, action), values[action])
        best_action[state], ans = max(values.items(), key=lambda x: x[1])
        return ans

    ans = dfs(State2(0, 'AA', 'AA', tuple()))
    # retrace path
    st = State2(0, 'AA', 'AA', tuple())
    while st.time <= 26:
        if st not in best_action:
            break
        print(st, best_action.get(st))
        st = next_state(st, best_action.get(st))
    return ans

def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part2(data) == 1707


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
