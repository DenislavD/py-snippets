# Fluent Python: Advanced Type Hints

# Overloaded signatures
# print(help(sum)) # sum(iterable, /, start=0) ..

import functools, operator
from collections.abc import Iterable
from typing import overload, Union, TypeVar
T = TypeVar('T') 
S = TypeVar('S')

@overload
def sum(it: Iterable[T]) -> Union[T, int]: ...
@overload
def sum(it: Iterable[T], /, start: S) -> Union[T, S]: ...

def sum(it, /, start=0): # no hints needed here
    return functools.reduce(operator.add, it, start)


# TypedDict
from typing import TypedDict, TYPE_CHECKING

class Fruit(TypedDict): # exists only for type checkers, no runtime effect. Use Data class builders.
    inventory_cnt: int
    name: str
    tastes: list[str]

pear = Fruit(color='red') # works
print(pear)

if TYPE_CHECKING:
    reveal_type(pear['tastes']) # debugging facility provided by MyPy

"Functions like json.loads return Any, so TypedDict can't be used to check statically."
"=> Need runtime validation."


# type casting
from typing import cast

cast(tuple, [1, 2, 3]) # used to silence type checkers
def incompatible_type_def(): # type: ignore
    ...


# runtime annotations
from typing import get_type_hints
from inspect import get_annotations

print(Fruit.__annotations__) # resolved classes here
print(get_type_hints(Fruit))
print(get_annotations(Fruit))
