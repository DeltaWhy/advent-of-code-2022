import collections
import itertools
import operator
import math


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

def sign(n):
    return 0 if n == 0 else -1 if n < 0 else 1

class Vec2(collections.namedtuple('Vec2', ['x', 'y'])):
    @classmethod
    def direction(cls, d, count=1):
        """
        >>> Vec2.direction('R', 2)
        (2, 0)
        >>> Vec2.direction('down')
        (0, 1)
        >>> Vec2.direction(None)
        (0, 0)
        """
        if not d:
            return Vec2(0, 0)
        return {'U': Vec2(0, -1),
                'D': Vec2(0, 1),
                'L': Vec2(-1, 0),
                'R': Vec2(1, 0)}[d.upper()[0]] * count

    def __add__(self, other):
        """
        >>> Vec2(1, 2) + Vec2(3, 4)
        (4, 6)
        >>> Vec2(1, 2) + (3, 4)
        (4, 6)
        """
        return Vec2(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        """
        >>> Vec2(1, 2) - Vec2(3, 4)
        (-2, -2)
        >>> Vec2(1, 2) - (3, 4)
        (-2, -2)
        """
        return Vec2(self.x - other[0], self.y - other[1])

    def __mul__(self, other):
        """
        >>> Vec2(-1, 1) * 3
        (-3, 3)
        """
        return Vec2(self.x * other, self.y * other)

    def __bool__(self):
        """
        >>> bool(Vec2(0, 0))
        False
        >>> bool(Vec2(1, 0))
        True
        """
        return not(self.x == 0 and self.y == 0)

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __abs__(self):
        return Vec2(abs(self.x), abs(self.y))

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def mag(self):
        """
        >>> Vec2(3, 4).mag()
        5.0
        """
        return math.sqrt(self.x**2 + self.y**2)

    def manhattan(self):
        """
        >>> Vec2(3, 4).manhattan()
        7
        """
        return abs(self.x) + abs(self.y)

    def dir(self):
        """
        >>> Vec2(0, -2).dir()
        (0, -1)
        """
        return Vec2(sign(self.x), sign(self.y))

    def neighbors(self):
        return [self + d for d in [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)]]

    def cneighbors(self):
        return [self + d for d in [
            (-1, 0), (1, 0), (0, -1), (0, 1)]]
