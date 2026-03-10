# Fluent Python - Classes and protocols

from array import array
import math

# A proper Pythonic class implementing object protocols (dunder methods)
class Vector2d:
    __match_args__ = ('x', 'y')

    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
    
    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __str__(self):
        return str(tuple(self)) # uses __iter__

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self)) # uses abs

    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    @classmethod # alternative constructor
    def frombytes(cls, octets):
        typecode = chr(octets[0]) # like 'd'
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)


# tests
v1 = Vector2d(3, 4)
assert v1.x, v1.y == (3.0, 4.0)
x, y = v1
assert x, y == (3.0, 4.0)
assert repr(v1) == 'Vector2d(3.0, 4.0)'
assert eval(repr(v1)) == v1 # v1.copy

octets = bytes(v1)
assert octets == b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'
assert abs(v1) == 5.0
assert bool(v1), bool(Vector2d(0.0, 0.0)) == (True, False)

v1_clone = Vector2d.frombytes(bytes(v1)) # typecode memv.tolist(): 'd [3.0, 4.0]'
assert v1_clone == v1

assert Vector2d(1.0, 0.0).angle() == 0.0
assert Vector2d(0, 0).angle() == 0.0

assert format(Vector2d(1, 1), '0.5fp') == '<1.41421, 0.78540>' # custom format
try:
    v1.x = 5
    print(f'ASSIGNMENT: {v1.x=}')
except AttributeError: # property 'x' of 'Vector2d' object has no setter
    pass

v2 = Vector2d(3.1, 4.2)
assert len({v1, v2}) == 2

print('All assertions passed.')