# with help from https://www.youtube.com/watch?v=5rb0vvJ7NCY

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


Blueprint = namedtuple('Blueprint', ['ore_ore', 'clay_ore', 'obsidian_ore', 'obsidian_clay', 'geode_ore', 'geode_obsidian'])

def parse(lines):
    res = []
    for line in lines:
        data = numbers(line)[1:]
        res.append(Blueprint(*data))
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))
    print(res)

WAIT = 0
BUILD_ORE = 1
BUILD_CLAY = 2
BUILD_OBSIDIAN = 3
BUILD_GEODE = 4

@dataclass(unsafe_hash=True)
class State:
    ore_bots: int = 1
    clay_bots: int = 0
    obsidian_bots: int = 0
    geode_bots: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geodes: int = 0

def gain(state: State, action: str, time_left: int):
    if action == BUILD_GEODE:
        return time_left - 1
    else:
        return 0

def heuristic(state: State, time_left: int) -> int:
    # Max possible future gain from a state: build a geode bot on every remaining turn.
    # gaussian summation
    # (time_left) + (time_left - 1) + ... + 2 + 1 ==
    return (time_left + 1) * time_left / 2

def realized_value(state: State, time_left: int) -> int:
    return state.geodes + time_left * state.geode_bots

def next_actions(blueprint: Blueprint, state: State, skip_ore: bool, skip_clay: bool, skip_obsidian: bool, skip_geode: bool):
    res = []
    if state.ore >= blueprint.ore_ore and not skip_ore:
        # don't build ore bots if we have enough to build the most expensive bot every turn
        if state.ore_bots < max(blueprint.ore_ore, blueprint.clay_ore, blueprint.obsidian_ore, blueprint.geode_ore):
            res.insert(0, BUILD_ORE)
    if state.ore >= blueprint.clay_ore and not skip_clay:
        # don't build clay bots if we have enough to build an obsidian bot every turn
        if state.clay_bots < blueprint.obsidian_clay:
            res.insert(0, BUILD_CLAY)
    if state.ore >= blueprint.obsidian_ore and state.clay >= blueprint.obsidian_clay and not skip_obsidian:
        # don't build obsidian bots if we have enough to build a geode bot every turn
        if state.obsidian_bots < blueprint.geode_obsidian:
            res.insert(0, BUILD_OBSIDIAN)
    if state.ore >= blueprint.geode_ore and state.obsidian >= blueprint.geode_obsidian and not skip_geode:
        res.insert(0, BUILD_GEODE)
    return res

def next(blueprint: Blueprint, state: State, action: int) -> State:
    ore = state.ore + state.ore_bots
    clay = state.clay + state.clay_bots
    obsidian = state.obsidian + state.obsidian_bots
    geodes = state.geodes + state.geode_bots
    if action == WAIT:
        return State(state.ore_bots, state.clay_bots, state.obsidian_bots, state.geode_bots, ore, clay, obsidian, geodes)
    elif action == BUILD_ORE:
        return State(state.ore_bots + 1, state.clay_bots, state.obsidian_bots, state.geode_bots, ore - blueprint.ore_ore, clay, obsidian, geodes)
    elif action == BUILD_CLAY:
        return State(state.ore_bots, state.clay_bots + 1, state.obsidian_bots, state.geode_bots, ore - blueprint.clay_ore, clay, obsidian, geodes)
    elif action == BUILD_OBSIDIAN:
        return State(state.ore_bots, state.clay_bots, state.obsidian_bots + 1, state.geode_bots, ore - blueprint.obsidian_ore, clay - blueprint.obsidian_clay, obsidian, geodes)
    elif action == BUILD_GEODE:
        return State(state.ore_bots, state.clay_bots, state.obsidian_bots, state.geode_bots + 1, ore - blueprint.geode_ore, clay, obsidian - blueprint.geode_obsidian, geodes)
    else:
        raise ValueError()

pruned = 0

best_at_time = defaultdict(lambda: 0)

dfs_cache: dict[State, tuple[int, int]] = {}

def dfs(blueprint: Blueprint, state: State, time_left: int, skip_ore: bool = False, skip_clay: bool = False, skip_obsidian: bool = False, skip_geode: bool = False):
    if state in dfs_cache:
        time_left2, value = dfs_cache[state]
        if time_left2 >= time_left:
            return value
    global pruned
    if time_left <= 0:
        return 0
    actions = next_actions(blueprint, state, skip_ore, skip_clay, skip_obsidian, skip_geode)
    best_value = 0
    for action in actions:
        st = next(blueprint, state, action)
        for t in range(time_left):
            if realized_value(st, time_left - 1) > best_at_time[t]:
                best_at_time[t] = realized_value(st, time_left - 1)
        if realized_value(st, time_left - 1) + heuristic(st, time_left - 1) <= best_at_time[time_left - 1]:
            pruned += 1
            continue
        value = gain(state, action, time_left) + dfs(blueprint, st, time_left - 1)
        if value > best_value:
            best_value = value
    # wait action
    st = next(blueprint, state, WAIT)
    for t in range(time_left):
        if realized_value(st, time_left - 1) > best_at_time[t]:
            best_at_time[t] = realized_value(st, time_left - 1)
    if realized_value(st, time_left - 1) + heuristic(st, time_left - 1) <= best_at_time[time_left - 1]:
        pruned += 1
    else:
        value = dfs(blueprint, st, time_left - 1, BUILD_ORE in actions, BUILD_CLAY in actions, BUILD_OBSIDIAN in actions, BUILD_GEODE in actions)
        if value > best_value:
            best_value = value

    dfs_cache[state] = (time_left, best_value)
    return best_value

def blueprint_value(blueprint, max_time = 24):
    global pruned
    pruned = 0
    best_at_time.clear()
    dfs_cache.clear()

    start = State(ore=0, clay=0, obsidian=0, geodes=0, ore_bots=1, clay_bots=0, obsidian_bots=0, geode_bots=0)
    ans = dfs(blueprint, start, max_time)
    print(pruned, len(dfs_cache))
    return ans

@pytest.mark.skip()
def test_blueprint_value():
    data = parse(fileinput.input(TEST_FILE))
    assert blueprint_value(data[0]) == 9
    assert blueprint_value(data[1]) == 12

@pytest.mark.skip()
def test_blueprint_value2():
    data = parse(fileinput.input(TEST_FILE))
    assert blueprint_value(data[0], 32) == 56
    assert blueprint_value(data[1], 32) == 62

def solve_part1(data):
    res = 0
    for i, blueprint in with_index(data):
        value = blueprint_value(blueprint)
        print(value, blueprint)
        res += value * (i + 1)
    return res

#@pytest.mark.skip()
def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert solve_part1(data) == 33

def solve_part2(data):
    res = 1
    for blueprint in data[0:3]:
        value = blueprint_value(blueprint, 32)
        print(value, blueprint)
        res *= value
    return res


if __name__ == '__main__':
    lines = list(fileinput.input())
    data = parse(lines)
    part1 = solve_part1(data)
    print(part1)
    data = parse(lines)
    part2 = solve_part2(data)
    print(part1)
    print(part2)
