import fileinput
import itertools
import operator
from collections import Counter, defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from functools import reduce, cache
from util import *


TEST_FILE = "test19.txt"


@dataclass(frozen=True)
class Cost:
    ore: int
    clay: int = 0
    obsidian: int = 0

@dataclass(frozen=True)
class Blueprint:
    id: int
    ore: Cost
    clay: Cost
    obsidian: Cost
    geode: Cost

def parse(lines):
    res = []
    for line in lines:
        data = numbers(line)
        res.append(Blueprint(id=data[0],
                             ore=Cost(data[1]),
                             clay=Cost(data[2]),
                             obsidian=Cost(ore=data[3], clay=data[4]),
                             geode=Cost(ore=data[5], obsidian=data[6])))
    return res

def test_parse():
    res = parse(fileinput.input(TEST_FILE))
    print(res)

@dataclass(unsafe_hash=True)
class State:
    blueprint: Blueprint = field(repr=False)
    time: int = 0
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
        new_state.time += 1
        new_state.ore += self.ore_bots
        new_state.clay += self.clay_bots
        new_state.obsidian += self.obsidian_bots
        new_state.geodes += self.geode_bots
        if action is None:
            pass
        elif action == 'ore_bot':
            new_state.ore_bots += 1
            new_state.ore -= self.blueprint.ore.ore
        elif action == 'clay_bot':
            new_state.clay_bots += 1
            new_state.ore -= self.blueprint.clay.ore
        elif action == 'obsidian_bot':
            new_state.obsidian_bots += 1
            new_state.ore -= self.blueprint.obsidian.ore
            new_state.clay -= self.blueprint.obsidian.clay
        elif action == 'geode_bot':
            new_state.geode_bots += 1
            new_state.ore -= self.blueprint.geode.ore
            new_state.obsidian -= self.blueprint.geode.obsidian
        else:
            raise ValueError()
        return new_state

    def actions(self):
        if self.time >= 24:
            return []
        res = [None]
        if self.ore >= self.blueprint.ore.ore:
            res.insert(0, 'ore_bot')
        if self.ore >= self.blueprint.clay.ore:
            res.insert(0, 'clay_bot')
        if self.ore >= self.blueprint.obsidian.ore and self.clay >= self.blueprint.obsidian.clay:
            res.insert(0, 'obsidian_bot')
        #if self.ore >= self.blueprint.geode.ore and self.obsidian >= self.blueprint.geode.obsidian:
        #    res.insert(0, 'geode_bot')
        if self.ore >= self.blueprint.geode.ore and self.obsidian >= self.blueprint.geode.obsidian:
            return ['geode_bot']
        #if self.ore >= self.blueprint.obsidian.ore and self.clay >= self.blueprint.obsidian.clay:
        #    return ['obsidian_bot']
        #if self.ore >= self.blueprint.clay.ore:
        #    return ['clay_bot']
        #if self.ore >= self.blueprint.ore.ore:
        #    return ['ore_bot']
        return res

def blueprint_value(blueprint):
    best_value_at_time = defaultdict(lambda: 0)
    best_action: dict[State, str] = {}

    def gain(state: State, action: str):
        if action == 'geode_bot':
            return (24 - state.time - 1)
        else:
            return 0

    @cache
    def dfs(state):
        #print(state)
        if state.time > 24:
            return 0
        actions = state.actions()
        if not actions:
            return 0
        values = {}
        for action in actions:
            st = state.next(action)
            # prune states that are definitely worse than optimal
            for i in range(st.time + 1):
                if st.geodes < best_value_at_time[i]:
                    continue
            if st.geodes > best_value_at_time[st.time]:
                best_value_at_time[st.time] = st.geodes
                print(best_value_at_time)
            values[action] = gain(state, action) + dfs(st)
            #print(state, action, gain(state, action), values[action])
        best_action[state], ans = max(values.items(), key=lambda x: x[1])
        #import pdb; pdb.set_trace()
        return ans

    start = State(blueprint=blueprint, time=0, ore=0, clay=0, obsidian=0, geodes=0, ore_bots=1, clay_bots=0, obsidian_bots=0, geode_bots=0)
    #import pdb; pdb.set_trace()
    ans = dfs(start)
    # retrace path
    st = start
    while st.time <= 24:
        if st not in best_action:
            break
        print(st, best_action.get(st))
        st = st.next(best_action.get(st))
    return ans

def solve_part1(data):
    for line in data:
        pass

def test_solve_part1():
    data = parse(fileinput.input(TEST_FILE))
    assert blueprint_value(data[0]) == 9
    assert solve_part1(data) == None

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
