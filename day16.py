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

def shortest_paths(valves):
    dist = defaultdict(lambda: float('inf'))
    for v1 in valves:
        dist[(v1, v1)] = 0
        for v2 in valves[v1].neighbors:
            dist[(v1, v2)] = 1
            dist[(v2, v1)] = 1
    for v3 in valves:
        for v2 in valves:
            for v1 in valves:
                if dist[(v1, v2)] > dist[(v1, v3)] + dist[(v3, v2)]:
                    dist[(v1, v2)] = dist[(v1, v3)] + dist[(v3, v2)]
                    dist[(v2, v1)] = dist[(v1, v2)]
    return dist

def solve_part2(valves):
    distances = shortest_paths(valves)
    best_action: dict[State, str] = {}
    def next_state(state: State, action: str):
        return State(state.time + 1 + distances[(state.pos, action)], action, tuple(sorted([action]+list(state.opened))))

    all_open = tuple(sorted((x.id for x in valves.values() if x.rate != 0)))

    def next_actions(state: State):
        if state.opened == all_open:
            return []
        else:
            return [x for x in valves if x not in state.opened and valves[x].rate != 0]

    def gain(state: State, action: str, max_time: int = 26):
        next_time = state.time + 1 + distances[(state.pos, action)]
        if next_time > max_time:
            return 0
        return valves[action].rate * (max_time - next_time)

    @cache
    def heuristic(state, max_time: int = 26):
        """The max possible score for a state would be opening one valve each turn."""
        remaining_set = set(all_open) - set(state.opened)
        remaining = {valve: valves[valve].rate for valve in remaining_set}
        to_visit = list(sorted(remaining.items(), key=lambda x: x[1], reverse=True))
        res = 0
        time = state.time
        for _, rate in to_visit:
            time += 1
            if time <= max_time:
                res += rate * (max_time - time)
        return res

    @cache
    def dfs(state):
        #print(state)
        actions = next_actions(state)
        if not actions:
            return 0
        values = {}
        for action in actions:
            st = next_state(state, action)
            if st.time > 26:
                continue
            # it's actually slower with pruning
            #if values and gain(state, action) + heuristic(st) < max(values.values()):
            #    # prune
            #    continue
            values[action] = gain(state, action) + dfs(st)
            #print(state, action, gain(state, action), values[action])
        if not values:
            return 0
        best_action[state], ans = max(values.items(), key=lambda x: x[1])
        return ans

    n_combos = 2**len(all_open)
    from itertools import chain, combinations

    def powerset(iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    n_visited = 0
    best_score = 0
    for elf_set in powerset(all_open):
        elephant_set = set(all_open) - set(elf_set)
        elf_score = dfs(State(0, 'AA', tuple(sorted(elephant_set))))
        elephant_score = dfs(State(0, 'AA', tuple(sorted(elf_set))))
        n_visited += 1
        if elf_score + elephant_score > best_score:
            best_score = elf_score + elephant_score
        print(f'Visited {n_visited}/{n_combos}\tcurrent {elf_score + elephant_score}\tbest {best_score}')

    return best_score


def test_solve_part2():
    data = parse(fileinput.input(TEST_FILE))
    print(shortest_paths(data))
    assert solve_part2(data) == 1707


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    print(part1)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
