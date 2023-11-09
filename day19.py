import enum
import fileinput
import itertools
import operator
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
    blueprint: Blueprint = field(repr=False)
    time_left: int = 24
    ore_bots: int = 1
    clay_bots: int = 0
    obsidian_bots: int = 0
    geode_bots: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geodes: int = 0

    def next(self, action = None):
        new_state = State(**self.__dict__)
        new_state.time_left -= 1
        new_state.ore += self.ore_bots
        new_state.clay += self.clay_bots
        new_state.obsidian += self.obsidian_bots
        new_state.geodes += self.geode_bots
        if action == Action.WAIT:
            pass
        elif action == Action.BUILD_ORE:
            new_state.ore_bots += 1
            new_state.ore -= self.blueprint.ore_ore
        elif action == Action.BUILD_CLAY:
            new_state.clay_bots += 1
            new_state.ore -= self.blueprint.clay_ore
        elif action == Action.BUILD_OBSIDIAN:
            new_state.obsidian_bots += 1
            new_state.ore -= self.blueprint.obsidian_ore
            new_state.clay -= self.blueprint.obsidian_clay
        elif action == Action.BUILD_GEODE:
            new_state.geode_bots += 1
            new_state.ore -= self.blueprint.geode_ore
            new_state.obsidian -= self.blueprint.geode_obsidian
        else:
            raise ValueError()
        return new_state

    def actions(self):
        if self.time_left == 0:
            return []
        res = [Action.WAIT]
        if self.ore >= self.blueprint.geode_ore and self.obsidian >= self.blueprint.geode_obsidian:
            # always build geode robot if possible
            return [Action.BUILD_GEODE]
        if self.ore >= self.blueprint.ore_ore:
            res.insert(0, Action.BUILD_ORE)
        if self.ore >= self.blueprint.clay_ore:
            res.insert(0, Action.BUILD_CLAY)
        if self.ore >= self.blueprint.obsidian_ore and self.clay >= self.blueprint.obsidian_clay:
            res.insert(0, Action.BUILD_OBSIDIAN)
        return res

def blueprint_value(blueprint):
    def gain(state: State, action: str):
        if action == Action.BUILD_GEODE:
            return state.time_left - 1
        else:
            return 0

    def heuristic(state: State) -> int:
        # Max possible future gain from a state: build a geode bot on every remaining turn.
        # gaussian summation
        # (time_left) + (time_left - 1) + ... + 2 + 1 ==
        return (state.time_left + 1) * state.time_left / 2

        # Better heuristic: assume we can only build geode bots starting on a future turn.
        # Assume we can build obsidian bots every turn until then.
        # At t=0 we have gained 0 obsidian, at t=1 bots_0, at t=2 (bots_0) + (bots_0+1), at t=3 (bots_0) + (bots_0+1) + (bots_0+2), ..
        # So at t=n for n > 1 we have (bots_0*n) + (n*(n-1)/2) == (bots_0*n) + (n**2/2) - (n/2)
        # == (bots_0-0.5)*n + (n**2/2)

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
        actions = state.actions()
        if not actions:
            return 0
        values = {}
        for action in actions:
            st = state.next(action)
            if realized_value(st) > best_at_time[st.time_left]:
                best_at_time[st.time_left] = realized_value(st)
            if realized_value(st) + heuristic(st) <= best_at_time[st.time_left]:
                pruned += 1
                continue
            values[action] = gain(state, action) + dfs(st)
        return max(values.values()) if values else 0

    start = State(blueprint=blueprint, time_left=24, ore=0, clay=0, obsidian=0, geodes=0, ore_bots=1, clay_bots=0, obsidian_bots=0, geode_bots=0)
    ans = dfs(start)
    print(pruned, dfs.cache_info())
    return ans

def solve_part1(data):
    res = 0
    for blueprint in data:
        value = blueprint_value(blueprint)
        print(value, blueprint)
        res += blueprint_value(blueprint) * blueprint.id
    return res

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert blueprint_value(data[0]) == 9
    assert blueprint_value(data[1]) == 12
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
