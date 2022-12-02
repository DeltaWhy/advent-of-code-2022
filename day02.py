import fileinput
import itertools


def solve(lines):
    lines1, lines2 = itertools.tee(lines)
    score = 0
    # A, B, C = rock, paper, scissors
    # X, Y, Z = rock, paper, scissors
    for line in lines1:
        theirs, mine = line.strip().split(' ')
        score += {'X': 1, 'Y': 2, 'Z': 3}[mine]
        if {'A': 'X', 'B': 'Y', 'C': 'Z'}[theirs] == mine:
            # draw
            score += 3
        elif {'A': 'Y', 'B': 'Z', 'C': 'X'}[theirs] == mine:
            # win
            score += 6
    part2 = 0
    # A, B, C = rock, paper, scissors
    # X, Y, Z = lose, draw, win
    shapes = {('A', 'X'): 'C', ('B', 'X'): 'A', ('C', 'X'): 'B',
              ('A', 'Y'): 'A', ('B', 'Y'): 'B', ('C', 'Y'): 'C',
              ('A', 'Z'): 'B', ('B', 'Z'): 'C', ('C', 'Z'): 'A'}
    for line in lines2:
        theirs, mine = line.strip().split(' ')
        part2 += {'X': 0, 'Y': 3, 'Z': 6}[mine]
        shape = shapes[(theirs, mine)]
        part2 += {'A': 1, 'B': 2, 'C': 3}[shape]
    return score, part2

def test_solve():
    assert solve(fileinput.input("test02.txt")) == (15, 12)

if __name__ == '__main__':
    part1, part2 = solve(fileinput.input())
    print(part1)
    print(part2)
