# Fluent Python: Interfaces, protocols and ABCs

# subclassing an ABC
from collections import namedtuple, abc

Card = namedtuple('Karta', ['suit', 'rank'])

class FrenchDeck2(abc.MutableSequence):
    vidove = ['pika', 'kupa', 'karo', 'spatiq']
    ranks = [str(x) for x in range(2, 11)] + list('JQKA')

    def __init__(self):
        self._cards = [Card(rank, vid) for vid in self.vidove for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, index):
        return self._cards[index]

    def __setitem__(self, position, value): # we need this for shuffling
        self._cards[position] = value

    def __delitem__(self, position):
        del self._cards[position]

    def insert(self, position, value):
        self._cards.insert(position, value)

# MutableSequence has abstract methods __setitem__, __delitem__ and insert, need to implement them or..
# TypeError: Can't instantiate abstract class FrenchDeck2 without an implementation for abstract method 'insert'
# checked only at runtime
deck = FrenchDeck2()
# price: implement the abstract __delitem__ and insert
# gain concrete methods: from Sequence: __contains__, __iter__, __reversed__, index and count 
# from MutableSequence: append, reverse, extend, pop, remove and __iadd__
# can be overridden with more efficient implementations if we want


# defining and using an ABC (used only for framework building)
import abc
import random

class TombolaABC(abc.ABC):
    
    @abc.abstractmethod # - subclasses are forced to override the implementation
    def load(self, iterable):
        """Add items from an iterable"""
        print('Loading items..') # subclasses can invoke this with super().load()

    @abc.abstractmethod
    def pick(self):
        """Remove item at random, returning it
        This method should raise 'LookupError' when the instance is empty"""

    # concrete methods
    def loaded(self): 
        """Return True if there is at least 1 item, False otherwise"""
        return bool(self.inspect())

    def inspect(self):
        """Return a sorted tuple with the items currently inside"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(items)


# regular inheritance
class BingoCage(TombolaABC):

    def __init__(self, iterable):
        self._items = list(iterable)

    def load(self, iterable):
        self._items.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._items))
        except ValueError:
            raise LookupError('pick from an empty BingoCage') from None # silence the ValueError
        return self._items.pop(position)

    # we are not obliged to implement this, but we can
    def loaded(self):
        return bool(self._items)

    # we can implement additional methods at will
    def __call__(self):
        return self.pick()


bingo = BingoCage([1, 2, 3, 4, 5])
print(bingo.inspect())
print(bingo(), bingo(), bingo(), bingo(), bingo())
#print(bingo.pick()) # LookupError: pick from an empty BingoCage


# virtual subclassing (goose typing)
# Warning: Not checked at import/compile time, will just get an error at runtime
@TombolaABC.register
class TomboList(list):
    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend

    def loaded(self): # can't do like load, becase list doesn't have __bool__ method
        return bool(self)

    def inspect(self):
        return tuple(self)

# alternatively TombolaABC.register(TomboList)
print(issubclass(TomboList, TombolaABC))

tl = TomboList('abcde')
print(tl.inspect(), '->', tl.pick())

# see also __subclasshook__ in ABC for structural typing automatic checking