import re
import pytest
from operator import add, sub, mul, truediv as div, mod
from keyword import iskeyword

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile(r"\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokens = tokenize(expression)
        if not tokens:
            return ''

        assignment = False
        if '=' in tokens:
            if list(reversed(tokens)).index('=') == len(tokens)-2:
                if isinstance(tokens[0], str) and not iskeyword(tokens[0]):
                    assignment = tokens[0]
                    del tokens[:2]
                else:
                    raise ValueError(f'Invalid assignment identifier: `{tokens[0]}`.')
            else:
                raise ValueError('Invalid assignment operator place.')

        self.format_tokens(tokens)

        # loop through arithmetic brackets
        while start := max((i for i, t in enumerate(tokens, 1) if t == '('), default=0):
            end = tokens.index(')', start)
            subexpr = tokens[start:end]
            result = self.do_math(subexpr)
            tokens[start-1:end+1] = result
        self.do_math(tokens)
        
        if len(tokens) != 1:
            raise ValueError('Invalid input.')

        if assignment:
            self.vars[assignment] = tokens[0]
        
        return tokens[0]


    def format_tokens(self, tokens):
        for i, token in enumerate(tokens):
            if '.' in token:
                tokens[i] = float(token)
            elif token.isnumeric():
                tokens[i] = int(token)
            elif token in self.vars:
                tokens[i] = self.vars[token]
            elif token not in '()=*/%+-':
                raise ValueError(f'Invalid character: `{token}`..')


    def do_math(self, items: list) -> list:
        i = 1 # first-order operations: * and /
        while i < len(items) and len(items) > 1:
            match items[i]:
                case '*': oper = mul
                case '/': oper = div
                case '%': oper = mod
                case _: oper = None

            if oper:
                items[i-1:i+2] = [ oper(items[i-1], items[i+1]) ]
            else:
                i += 1

        i = len(items) - 2 # addition and subtraction
        while i < len(items) and len(items) > 1:
            match items[i]:
                case '+': oper = add
                case '-': oper = sub
                case _: #  , assignment
                    break

            items[i-1:i+2] = [ oper(items[i-1], items[i+1]) ]
            
        return items


### Tests
interpreter = Interpreter();
    
# Basic arithmetic
assert interpreter.input("1 + (1.4 + 2)") == 4.4
assert interpreter.input("2 - 1") == 1
assert interpreter.input("2 * 3") == 6
assert interpreter.input("8 / 4") == 2
assert interpreter.input("7 % 4") == 3

# Variables
assert interpreter.input("x = 1") == 1
assert interpreter.input("x") == 1
assert interpreter.input("x + 3") == 4
with pytest.raises(ValueError):
    interpreter.input("y + 6")
with pytest.raises(ValueError):
    assert interpreter.input("x == 1") == 1
assert interpreter.input("x = 1") == 1

# Other tests
assert interpreter.input('  \t ') == ''
assert interpreter.input('iif = 8 * (3 % 2)') == 8
assert interpreter.input('iif = 8 * (3 % 2) - 1') == 7
assert interpreter.input('iif = (8 * (3 % 2) - 1)') == 7
assert interpreter.input('iif = (8 * (3 % 2) - x)') == 7
assert interpreter.input('(7 + 3) / (2 * 2 + 1)') == 2