# coding: cp1251
# from Fluent Python - binary data operations - чак

import locale
print(f'Locale preferred (default for text files): {locale.getpreferredencoding()}')

with open('encodings_test.txt', 'r', encoding='cp1251') as file:
    row = file.readline()
    print('Correct:', row)

with open('encodings_test.txt', 'r', encoding='cp1252') as file:
    row = file.readline()
    print('Silent garbage symbols (gremlins):', row)

with open('encodings_test.txt', 'r', encoding='utf-8') as file:
    try:
        row = file.readline()
    except UnicodeDecodeError as exc:
        print('UTF-8 error recognition:', exc)

print('continue here..')


# Data Class Builders
from typing import NamedTuple # function that creates a namedtuple
from collections import namedtuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
    x: int = 1.1

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        ew = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{ew}, X: {self.x}'

NT = Coordinate(46.328056, -24.246775434)
Coord = namedtuple('Coord', 'lat lon name', defaults=['Sofia']) # defaults start from the rightmost
nt = Coord(33.3, 22.2)
print(f'{NT=}, {nt=}')

print(Coordinate.__mro__) # class supers?
print('tuple: ', issubclass(Coordinate, tuple))
# NamedTuple/namedtuple check in Python 3.13
print('Annotations: NamedTuple:', hasattr(NT, '__annotations__'), 'namedtuple:', hasattr(nt, '__annotations__'))
