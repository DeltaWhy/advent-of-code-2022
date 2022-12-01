import fileinput


test_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

lines = test_input.split('\n')
groups = [[]]
for line in fileinput.input():
    if not line.strip():
        groups.append([])
    else:
        groups[-1].append(line)

sums = [sum(map(int, group)) for group in groups]
print(sums)
print(max(sums))
print((list(sorted(sums))[-3:]))
print(sum(list(sorted(sums))[-3:]))
