# Fluent Python: Context Managers

import sys
from contextlib import contextmanager

class LookingGlass:
    def __enter__(self): # only argument
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'REVERSED..' # can be anything

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True # tells the interpreter that the exception was handled

with (
    LookingGlass() as return_val,
    # more than 1 Context Managers can be listed in 3.10+ 
):
    print('Hello there?')
    print(return_val)


# shortcut with @contextmanager + generator function
@contextmanager
def underscored():
    original_write = sys.stdout.write

    def underscore_write(text):
        original_write('_'.join(text))

    sys.stdout.write = underscore_write
    try: # if an exception is raised in the with block, it will be re-raised here => try
        yield # can yield something as well if needed
    except Exception as exc:
        print('Error:', exc.args[:20], '..')

    sys.stdout.write = original_write # exit (restore)

with underscored():
    print('What now huh??')
    undefined
print('Stop this! Is it normal again?')
print()

# Fun fact: @contextmanager-decorated functions work as decorators too!

@underscored() # needs to have the parentheses
def say_something(text):
    print(text)

say_something('OH, come on..')
