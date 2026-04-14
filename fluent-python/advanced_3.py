from __future__ import annotations # postponed evaluation (as strings)
# this will be deprecated later, since 3.14 introduced a more elegant solution (lazy eval.)

from typing import get_type_hints, TypedDict
from inspect import get_annotations # 3.14+ : from annotationlib

class Fruit(TypedDict):
    inventory_cnt: int
    name: str
    tastes: list[str]

print(Fruit.__annotations__)
print(get_type_hints(Fruit))
print(get_annotations(Fruit))


# Generic classes
import random
from collections.abc import Iterable
from typing import TypeVar, Generic

from tryharder9 import TombolaABC

T = TypeVar('T')

class TomboListTyped(TombolaABC, Generic[T], list):
    def __init__(self, items: Iterable[T]) -> None:
        super().__init__(items)

    def pick(self) -> T:
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend

    def loaded(self): # can't do like load, becase list doesn't have __bool__ method
        return bool(self)

    def inspect(self) -> tuple[T, ...]:
        return tuple(self)

# generic class instantiation
tl = TomboListTyped[str]('abcde') # useful when type checking statically
print(tl.inspect(), '->', tl.pick())

"Legend: "
TomboListTyped[T]   # generic type
TomboListTyped[str] # parametrized type
T                   # formal type parameter
str                 # actual type parameter

print('\nVariance: invariant (this type ONLY), covariant (children), contravariant (parents)')
