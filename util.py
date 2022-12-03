import itertools


def groups(iter, size):
    """
    >>> groups('ABCDEFGHI', 3)
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    """
    l = list(iter)
    return [l[i:i+3] for i in range(0, len(l), size)]
