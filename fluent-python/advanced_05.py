# Fluent Python: Generators and generator expressions

# Iterator: General term for any object that implements a __next__ method
# Generator: An iterator built by the Python compiler (yield instead of __next__ )

# generators
def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end.')

print(gen_AB) # generator function (factory)
print(gen_AB()) # generator object, implementing the Iterator interface
for i in gen_AB():
    print(i)
print('eager:', '-' * 50)

# executes the whole generator function and saves the yields
res_eager = [x*3 for x in gen_AB()]
for i in res_eager:
    print('-->', i)

# goes chunk by chunk
print('lazy:', '-' * 50)
res_lazy = (x*3 for x in gen_AB())
for i in res_lazy:
    print('-->', i)



# advanced_4 example reworked lazily
from advanced_4 import SentenceGen, RE_WORD

class SentenceGenLazy(SentenceGen):
    def __init__(self, text):
        self.text = text
        # no need of a words list

    def __iter__(self):
        for match in RE_WORD.finditer(self.text): # lazy .findall()
            yield match.group()
        # OR with generator expression
        # return (match.group() for match in RE_WORD.finditer(self.text))

sentence_gen_lazy = SentenceGenLazy('We are incredible.')
for i, word in enumerate(sentence_gen_lazy, 1):
    print(i, ':', word, end='; ')



# Arithmetic Progression generator function
def aritprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index

print()
g = aritprog_gen(3, 0.5, 10)
for item in g:
    print(item, end='; ')

