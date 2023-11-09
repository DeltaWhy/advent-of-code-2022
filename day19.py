import enum
import fileinput
import itertools
import operator
import pytest
from collections import Counter, defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from functools import reduce, cache
from util import *


TEST_FILE = "test19.txt"


Blueprint = namedtuple('Blueprint', ['id', 'ore_ore', 'clay_ore', 'obsidian_ore', 'obsidian_clay', 'geode_ore', 'geode_obsidian'])

def parse(lines):
    res = []
    for line in lines:
        data = numbers(line)
        res.append(Blueprint(*data))
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))
    print(res)

class Action(enum.Enum):
    WAIT = enum.auto()
    BUILD_ORE = enum.auto()
    BUILD_CLAY = enum.auto()
    BUILD_OBSIDIAN = enum.auto()
    BUILD_GEODE = enum.auto()

@dataclass(unsafe_hash=True)
class State:
    time_left: int = 24
    ore_bots: int = 1
    clay_bots: int = 0
    obsidian_bots: int = 0
    geode_bots: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geodes: int = 0

def blueprint_value(blueprint, max_time = 24):
    def next_actions(state: State):
        if state.time_left == 0:
            return []
        res = [Action.WAIT]
        if state.ore >= blueprint.geode_ore and state.obsidian >= blueprint.geode_obsidian:
            # always build geode robot if possible
            return [Action.BUILD_GEODE]
        if state.ore >= blueprint.ore_ore:
            res.insert(0, Action.BUILD_ORE)
        if state.ore >= blueprint.clay_ore:
            res.insert(0, Action.BUILD_CLAY)
        if state.ore >= blueprint.obsidian_ore and state.clay >= blueprint.obsidian_clay:
            res.insert(0, Action.BUILD_OBSIDIAN)
        return res

    def next(state: State, action: Action) -> State:
        time_left = state.time_left - 1
        ore = state.ore + state.ore_bots
        clay = state.clay + state.clay_bots
        obsidian = state.obsidian + state.obsidian_bots
        geodes = state.geodes + state.geode_bots
        if action == Action.WAIT:
            return State(time_left, state.ore_bots, state.clay_bots, state.obsidian_bots, state.geode_bots, ore, clay, obsidian, geodes)
        elif action == Action.BUILD_ORE:
            return State(time_left, state.ore_bots + 1, state.clay_bots, state.obsidian_bots, state.geode_bots, ore - blueprint.ore_ore, clay, obsidian, geodes)
        elif action == Action.BUILD_CLAY:
            return State(time_left, state.ore_bots, state.clay_bots + 1, state.obsidian_bots, state.geode_bots, ore - blueprint.clay_ore, clay, obsidian, geodes)
        elif action == Action.BUILD_OBSIDIAN:
            return State(time_left, state.ore_bots, state.clay_bots, state.obsidian_bots + 1, state.geode_bots, ore - blueprint.obsidian_ore, clay - blueprint.obsidian_clay, obsidian, geodes)
        elif action == Action.BUILD_GEODE:
            return State(time_left, state.ore_bots, state.clay_bots, state.obsidian_bots, state.geode_bots + 1, ore - blueprint.geode_ore, clay, obsidian - blueprint.geode_obsidian, geodes)
        else:
            raise ValueError()

    def gain(state: State, action: str):
        if action == Action.BUILD_GEODE:
            return state.time_left - 1
        else:
            return 0

    def heuristic(state: State) -> int:
        # Max possible future gain from a state: build a geode bot on every remaining turn.
        # gaussian summation
        # (time_left) + (time_left - 1) + ... + 2 + 1 ==
        #return (state.time_left + 1) * state.time_left / 2

        # Better heuristic: assume we can only build geode bots starting on a future turn.
        # Assume we can build obsidian bots every turn until then.
        # At turn n we will have less than (obsidian) + (obsidian_bots * n) + n**2
        while state.obsidian_bots == 0 and state.clay < blueprint.obsidian_clay:
            state = next(state, Action.BUILD_CLAY)
        while state.obsidian < blueprint.geode_obsidian:
            state = next(state, Action.BUILD_OBSIDIAN)
        return (state.time_left + 1) * state.time_left / 2

    def realized_value(state: State) -> int:
        return state.geodes + state.time_left * state.geode_bots

    pruned = 0

    best_at_time = defaultdict(lambda: 0)

    @cache
    def dfs(state):
        nonlocal pruned
        #print(pruned, dfs.cache_info())
        if state.time_left <= 0:
            return 0
        actions = next_actions(state)
        if not actions:
            return 0
        actions = list(sorted(actions, key=lambda a: gain(state, a), reverse=True))
        values = {}
        for action in actions:
            st = next(state, action)
            if realized_value(st) > best_at_time[st.time_left]:
                best_at_time[st.time_left] = realized_value(st)
            if realized_value(st) + heuristic(st) <= best_at_time[st.time_left]:
                pruned += 1
                continue
            values[action] = gain(state, action) + dfs(st)
        return max(values.values()) if values else 0

    start = State(time_left=max_time, ore=0, clay=0, obsidian=0, geodes=0, ore_bots=1, clay_bots=0, obsidian_bots=0, geode_bots=0)
    ans = dfs(start)
    print(pruned, dfs.cache_info())
    return ans

#@pytest.mark.skip()
def test_blueprint_value():
    data = parse(fileinput.input(TEST_FILE))
    assert blueprint_value(data[0]) == 9
    assert blueprint_value(data[1]) == 12

@pytest.mark.skip()
def test_blueprint_value2():
    data = parse(fileinput.input(TEST_FILE))
    assert blueprint_value(data[0], 28) == 56
    #assert blueprint_value(data[1], 32) == 62

def solve_part1(data):
    res = 0
    for blueprint in data:
        value = blueprint_value(blueprint)
        print(value, blueprint)
        res += blueprint_value(blueprint) * blueprint.id
    return res

@pytest.mark.skip()
def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 33

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
