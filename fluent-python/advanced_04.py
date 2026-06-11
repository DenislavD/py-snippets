# Fluent Python: Iterators

# emulating an iterator in for loop
s = 'ABC'
it = iter(s)
while True:
    try:
        print(next(it))
    except StopIteration:
        del it
        break


# classic iterator example
import re
import reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self): # fulfills the Iterable protocol
        return SentenceIterator(self.words)

class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self): # alternatively can be gained by subclassing abc.Iterator
        return self


# with generator function (generator factory which returns a generator object)
# No SentenceIterator needed
class SentenceGen(Sentence):
    def __iter__(self): # override __iter__
        for word in self.words:
            yield word
        # OR: yield from self.words


if __name__ == '__main__':
    sentence = Sentence('I am cool.')
    for i, word in enumerate(sentence, 1):
        print(i, ':', word, end='; ')    

    print() # clear line
    sentence_gen = SentenceGen('You are great!')
    for i, word in enumerate(sentence_gen, 1):
        print(i, ':', word, end='; ')
