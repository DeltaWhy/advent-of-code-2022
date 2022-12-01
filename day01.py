import fileinput


def solve(lines):
    groups = [[]]
    for line in lines:
        if not line.strip():
            groups.append([])
        else:
            groups[-1].append(line)

    sums = [sum(map(int, group)) for group in groups]
    return (max(sums), sum(list(sorted(sums))[-3:]))

def test_solve():
    assert solve(fileinput.input("test01.txt")) == (24000, 45000)

if __name__ == '__main__':
    part1, part2 = solve(fileinput.input())
    print(part1)
    print(part2)
