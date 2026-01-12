# from Fluent Python - data structures
from collections import namedtuple
from random import randint, choice

Card = namedtuple('Karta', ['suit', 'rank'])

class FrenchDeck:
    vidove = ['pika', 'kupa', 'karo', 'spatiq']
    ranks = [str(x) for x in range(2, 11)] + list('JQKA')

    def __init__(self):
        self._cards = [Card(rank, vid) for vid in self.vidove for rank in self.ranks]

    def __repr__(self):
        return f'Cards from {self._cards[0]} to {self._cards[-1]}'

    def __getitem__(self, index):
        return self._cards[index]

    def __len__(self):
        return len(self._cards)

    def pick_random(self):
        number = randint(0, 51)
        return self[number]

deck = FrenchDeck()

print(len(deck), 'cards', end='; ')
print(f'Random: {deck.pick_random()} or {choice(deck)}')

# __getitem__ => slice-able, iterable
for card in reversed(deck[:5]):
    print(card)

assert Card('Q', 'kupa') in deck

# Flat sequences - str, bytes, array.array
from array import array
arr = array('d', [9.46, 13.02, 5]) # one object in C with the same type of items in it
print(arr)

# Generator expressions - () instead of [] in list comprehensions
for tshirt in ((size, color) for size in ['S', 'M', 'L'] for color in ['black', 'white']):
    print(tshirt) # yields res

