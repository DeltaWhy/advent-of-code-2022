import collections
from dataclasses import dataclass
from functools import reduce
import itertools
import operator
import math
import re


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
        key_or_func = lambda x: hasattr(x, 'strip') and not x.strip()
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

def product(iterable, key=None):
    if key:
        return reduce(lambda acc, x: acc * key(x), iterable, 1)
    else:
        return reduce(lambda acc, x: acc * x, iterable)

def numbers(s: str) -> list[int]:
    """
    >>> numbers('for i in 1 to 10')
    [1, 10]
    >>> numbers('1, 2, 3')
    [1, 2, 3]
    >>> numbers('-1 items from 2 - 3')
    [-1, 2, 3]
    >>> numbers('-1 items from 2-3')
    [-1, 2, 3]
    >>> numbers('[-1, 2, 3, 100, -99]')
    [-1, 2, 3, 100, -99]
    """
    pattern = re.compile(r'''(?x)(?:(?: # without capturing,
        (?<=[^0-9])|^) # look-behind for a non-digit or start of string
        -)? # followed by minus, all optional
        \b[0-9]+\b # finally, a series of digits''')
    return [int(match) for match in re.findall(pattern, s)]

class Rect(collections.namedtuple('Rect', ['x1', 'y1', 'x2', 'y2'])):
    def __new__(cls, *args, **kwargs):
        """
        >>> Rect(1, 2, 3, 4)
        Rect((1, 2), (3, 4))
        >>> Rect((1, 2), (3, 4))
        Rect((1, 2), (3, 4))
        >>> Rect(Vec2(1, 2), (3, 4))
        Rect((1, 2), (3, 4))
        >>> Rect(1, 2, w=3, h=4)
        Rect((1, 2), (3, 5))
        >>> Rect((1, 2), w=3, h=4)
        Rect((1, 2), (3, 5))
        """
        if len(args) == 4:
            self = super().__new__(cls, *args)
        elif len(args) == 2 and not kwargs:
            self = super().__new__(cls, args[0][0], args[0][1], args[1][0], args[1][1])
        elif len(args) == 2 and 'h' in kwargs and 'w' in kwargs:
            self = super().__new__(cls, args[0], args[1], args[0] + kwargs['w'] - 1, args[1] + kwargs['h'] - 1)
        elif len(args) == 1 and 'h' in kwargs and 'w' in kwargs:
            self = super().__new__(cls, args[0][0], args[0][1], args[0][0] + kwargs['w'] - 1, args[0][1] + kwargs['h'] - 1)
        assert self.x1 <= self.x2 and self.y1 <= self.y2
        return self

    @property
    def w(self):
        return self.x2 - self.x1 + 1

    @property
    def h(self):
        return self.y2 - self.y1 + 1

    @property
    def p1(self):
        return Vec2(self.x1, self.y1)

    @property
    def p2(self):
        return Vec2(self.x2, self.y2)

    def __repr__(self):
        return f'Rect(({self.x1}, {self.y1}), ({self.x2}, {self.y2}))'

    def __contains__(self, other):
        """
        >>> Rect(1, 1, 2, 2) in Rect(0, 0, 3, 3)
        True
        >>> Rect(1, 1, 3, 3) in Rect(0, 0, 2, 2)
        False
        >>> (0, 0) in Rect(-1, -1, 1, 1)
        True
        >>> (1, 2) in Rect(-1, -1, 1, 1)
        False
        """
        if isinstance(other, Rect):
            return other.p1 in self and other.p2 in self
        elif isinstance(other, Vec2) or len(other) == 2:
            return self.x1 <= other[0] <= self.x2 and self.y1 <= other[1] <= self.y2
        else:
            raise ValueError(other)

    def coords(self):
        for y in range(self.y1, self.y2 + 1):
            for x in range(self.x1, self.x2 + 1):
                yield Vec2(x, y)

class Grid(list):
    def __init__(self, iterable):
        """
        >>> Grid(range(4))
        Grid[[0], [1], [2], [3]]
        >>> Grid([range(3), range(3, 6)])
        Grid[[0, 1, 2], [3, 4, 5]]
        >>> Grid(groups(range(10), 3)).pprint()
        Grid[[0 1 2]
             [3 4 5]
             [6 7 8]
             [9]]
        """
        super().__init__(((list(x) if isinstance(x, collections.abc.Iterable) else [x]) for x in iterable))

    def __getitem__(self, index):
        """
        >>> g = Grid([[1, 2], [3, 4]])
        >>> g[(0, 1)]
        3
        >>> g[0]
        [1, 2]
        >>> g[1:]
        Grid[[3, 4]]
        >>> Grid(['abc', 'def', 'ghi'])[Rect((1, 1), (2, 2))]
        Grid[['e', 'f'], ['h', 'i']]
        """
        if isinstance(index, int):
            return super().__getitem__(index)
        elif isinstance(index, slice):
            return Grid(super().__getitem__(index))
        elif isinstance(index, Rect):
            return Grid((row[index.x1:index.x2+1] for row in self[index.y1:index.y2+1]))
        else:
            return super().__getitem__(index[1])[index[0]]

    def __setitem__(self, index, value):
        """
        >>> g = Grid([[1, 2], [3, 4]])
        >>> g[(0, 1)] = 'x'
        >>> g[(0, 1)]
        'x'
        """
        if isinstance(index, int):
            return super().__setitem__(index, value)
        elif isinstance(index, slice):
            return Grid(super().__setitem__(index, value))
        else:
            return super().__getitem__(index[1]).__setitem__(index[0], value)

    def __repr__(self):
        """
        >>> Grid([[1, 2], [3, 4]])
        Grid[[1, 2], [3, 4]]
        """
        return f'Grid{super().__repr__()}'

    def pprint(self, indent=0):
        """
        >>> g = Grid([[1, 2], [3, 4]])
        >>> g.pprint()
        Grid[[1 2]
             [3 4]]
        >>> g.pprint(indent=2)
          Grid[[1 2]
               [3 4]]
        >>> Grid([[100, 2], [3, 4]]).pprint()
        Grid[[100   2]
             [  3   4]]
        >>> Grid(['abc', 'def']).pprint()
        Grid[[a b c]
             [d e f]]
        """
        max_len = 0
        for row in self:
            for item in row:
                l = len(f'{item}')
                max_len = max(max_len, l)
        fmt = '{:' + str(max_len) + '}'
        print(' '*indent, end='')
        print('Grid[[', end='')
        print(' '.join((fmt.format(item) for item in self[0])), end=']')
        for row in self[1:]:
            print('\n' + ' ' * (indent + 5), end='')
            print('[' + ' '.join((fmt.format(item) for item in row)), end=']')
        print(']')

    def coords(self):
        for y in range(len(self)):
            for x in range(len(self[y])):
                yield Vec2(x, y)

    def items(self):
        for y in range(len(self)):
            for x in range(len(self[y])):
                yield (Vec2(x, y), self[y][x])

    def compact(self):
        """
        >>> print(Grid.of('x', 3, 3).compact())
        xxx
        xxx
        xxx
        >>> print(Grid.of(True, 3, 3).compact())
        TTT
        TTT
        TTT
        >>> print(Grid.of(10, 3, 3).compact())
        101010
        101010
        101010
        >>> print(Grid.of(Vec2(0,0), 2, 2).compact())
        (0, 0)(0, 0)
        (0, 0)(0, 0)
        """
        return '\n'.join((''.join(((str(item)[0] if isinstance(item, bool) else str(item)) for item in row)) for row in self))

    @classmethod
    def of_size(cls, w, h):
        return cls.of(None, w, h)

    @classmethod
    def of(cls, item, w, h):
        """
        >>> Grid.of(0, 2, 2)
        Grid[[0, 0], [0, 0]]
        """
        return cls([[item] * w] * h)

    def rect(self):
        return Rect(0, 0, w=len(self[0]), h=len(self))
