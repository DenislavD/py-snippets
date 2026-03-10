# Fluent Python - mutable arguments

# can use in __init__ 
a = [1, 2]
b = list(a) # costructor creates a copy!, can also convert to list - very useful
print(id(a), id(b), b)

# __init__.__defaults__


# Advanced decorators
from functools import wraps

# decorators with parameters
def deco_factory(printit=True):
    def log_decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if printit:
                print(f'Inner start, executing f next')
                f(*args, **kwargs)
                print(f'Inner exit')
            else:
                f(*args, **kwargs)
        return inner

    return log_decorator


@deco_factory(False) # returns log_decorator with printit=True closure
def summer(a, b, double_b=1):
    """Sums 2 integers."""
    print(f'Sum of {a} and {b} * {double_b} is: {a + b * double_b}')

summer(1, 3, 2)
print(summer.__doc__, summer.__name__)


# class decorators (recommended, advanced usage)
class pickbingo():
    def __init__(self, flag='odd'):
        self.flag = flag if flag == 'odd' else 'even'

    def __call__(self, f):
        @wraps(f)
        def inner(*args, **kwargs):
            print(f'Flag: {self.flag}')
            f(*args, **kwargs) # no need to return here, since f only has a side effect (print)
            print('Exiting decorator')
        return inner

@pickbingo('odd') # creates the class with the call and then runs instance(number)
def number(n, type):
    """Returns and odd or an even number."""
    res = n if type == 'odd' and n % 2 == 1 else n + 1
    print(res)

number(3, 'odd')
print(number.__doc__, number.__name__)

