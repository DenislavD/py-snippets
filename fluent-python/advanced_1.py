# Fluent Python: Multiple inheritance and MRO

class Root:
    def pong(self):
        pass

class A(Root):
    def pong(self):
        super().pong() # "cooperative" method

class B(Root):
    pass

class Leaf(A, B):
    pass

print(Leaf.__mro__)
# (<class 'Leaf'>, <class 'A'>, <class 'B'>, <class 'Root'>, <class 'object'>)
"A leaf.pong() call goes to A, then to B, where it doesn't exist and doesn't reach Root."


# Mixin Classes - used to augment in combo with another child or sibling class
import collections

def _upper(key):
    try:
        return key.upper()
    except AttributeError:
        return key

# provides case-insensitive mappings by uppercasing when adding or looking up
class UpperCaseMixin:
    def __setitem__(self, key, item):
        super().__setitem__(_upper(key), item)

    def __getitem__(self, key):
        return super().__getitem__(_upper(key))

    def get(self, key, default=None):
        return super().get(_upper(key), default)

    def __contains__(self, key):
        return super().__contains__(_upper(key))

# use
class UpperDict(UpperCaseMixin, collections.UserDict):
    pass

class UpperCounter(UpperCaseMixin, collections.Counter):
    """Specialized 'Counter' that uppercases string keys"""

d = UpperDict([('a', 'letter A'), (2, 'digit two')])
print(list(d.keys()))
d['b'] = 'letter B'
print(f'{'b' in d=}')
print(d, d.get('a'), d.get('b'))

c = UpperCounter('BaNanA')
print(c, c.most_common())
