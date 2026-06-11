# Fluent Python: Subgenerators with yield from

# simple version
def sub_gen():
    yield 1.1
    yield 1.2

def gen():
    yield 1
    for i in sub_gen(): # sees 'i', while yield from won't.
        yield i
    yield 2

for x in gen():
    print(x)


# practical example - tree recursion
# delegating generator
def tree(cls, level=0):
    yield cls.__name__, level
    for sub_cls in cls.__subclasses__():
        yield from tree(sub_cls, level + 1) # goes directly to the client code

# client code
def display(cls):
    for cls_name, level in tree(cls):
        indent = ' ' * 4 * level
        print(f'{indent}{cls_name}')

if __name__ == '__main__':
    display(BaseException)
