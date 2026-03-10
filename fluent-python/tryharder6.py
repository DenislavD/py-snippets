# Data Class Builders continuation

from typing import NamedTuple # function that creates a namedtuple
from dataclasses import dataclass

class DemoPlainClass:
    a: int
    b: float = 1.1
    c = 'cabbage'

DemoPlainClass.z = 'NEW' # can add class attrs during runtime
print('------------------ Plain --------------------')
print(DemoPlainClass.__annotations__, DemoPlainClass.b, DemoPlainClass.z) # DemoPlainClass.a -> AttributeError

o = DemoPlainClass()
print(f'{o.b=}, {o.c=}') # b,c = class attributes; o.a -> AttributeError
o.b, o.c, o.z = 'nice', 24, None
print(f'{DemoPlainClass.b=}, {o.b=}, {o.z=}') # can change instance attrs


class DemoNTClass(NamedTuple): # main diffs: has a (from __annot.) + creates a tuple
    a: int
    b: float = 1.1
    c = 'cabbage'

DemoNTClass.z = 'NEW'
print('------------------ NamedTuple --------------------')
print('__doc__:', DemoNTClass.__doc__, '  __annotations__:', DemoNTClass.__annotations__)
print(f'{DemoNTClass.a=}, {DemoNTClass.b=}, {DemoNTClass.c=}, {DemoNTClass.z=}')

ont = DemoNTClass(8) # max 2 args: for a, b
#ont.a = 5 # AttributeError: can't set attribute
#ont.c = 5 # AttributeError: 'DemoNTClass' object attribute 'c' is read-only
#ont.q = 5 # AttributeError: 'DemoNTClass' object has no attribute 'q' and no __dict__ for setting new attributes
print('instance:', ont, ont.c, ont.z) # can add/change attr. to the class, but not the instance (it's a tuple)


@dataclass(frozen=False, order=True)
class DemoDataClass: # main diffs: a is not a class atrr. + we can change everything
    a: int
    b: float = 1.1
    c = 'cabbage'

DemoDataClass.z = 'NEW'
print('------------------ Data Class --------------------')
print('__doc__:', DemoDataClass.__doc__, '  __annotations__:', DemoDataClass.__annotations__)
print(f'{DemoDataClass.b=}, {DemoDataClass.c=}, {DemoDataClass.z=}') # DemoDataClass.a -> AttributeError

odc = DemoDataClass(9, 2.1)
print('instance:', odc, odc.c, odc.z)

