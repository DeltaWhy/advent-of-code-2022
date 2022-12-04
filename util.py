import itertools
import operator


def with_index(iterable):
    """
    >>> list(with_index('ABC'))
    [(0, 'A'), (1, 'B'), (2, 'C')]
    """
    return zip(itertools.count(), iterable)

def groups(iterable, size):
    """
    >>> list(groups('ABCDEFGHI', 3))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    >>> list(groups('ABCDEFG', 3))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]
    """
    it = iter(iterable)
    while (l := list(itertools.islice(it, size))):
           yield l

def lmap(f, iterable):
    """
    >>> lmap(lambda x: x*2, range(3))
    [0, 2, 4]
    """
    return list(map(f, iterable))

def isplit(iterable, key_or_func=None):
    """
    >>> list(isplit(['a', 'b', 'c', '', 'd', 'e', 'f', '']))
    [['a', 'b', 'c'], ['d', 'e', 'f']]
    """
    it = iter(iterable)
    if key_or_func is None:
        key_or_func = operator.not_
    f = key_or_func if callable(key_or_func) else lambda x: x == key_or_func
    while (l := list(itertools.takewhile(lambda x: not f(x), it))):
        yield l
