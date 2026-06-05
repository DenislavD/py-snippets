# 2 kyu - Evaluate mathematical expression
import re
from operator import add, sub, mul, truediv as div

sample = '(86+--1455.0-73)' # '(--24.0+-68.0/-12235.0)' 
cases = (
    ('1 + 1', 2),
    ('2 ++ ((8/16.0) + 3)', 5.5),
    ('3 -(-1)', 4),
    ('2 + -2', 0),
    ('10- 2- -5', 13),
    ('(((10)))', 10),
    ('3 * 5', 15),
    ('-7 * -(6 / 3)', 14)
)

def calc(text):
    text = re.sub(r'\s', '', text) # remove whitespace
    text = f'({text})' # add outer brackets to simplify loop

    while res:= re.search(r'\([^()]*\)', text): # innermost bracket content
        subexpr = res.group()
        items = format_items(subexpr[1:-1])
        result = do_math(items)
        text = text.replace(subexpr, str(*result)) # 

    return float(text)

def format_items(text):
    items = re.split(r'([\d.]+)', text) # split by digits into list

    i = 0
    while i < len(items):
        if items[i].count('-') + items[i].count('+') >= 2:
            items[i] = reduce_operators(items[i])

        try:
            items[i] = float(items[i])
        except ValueError:
            pass

        match items[i]:
            case '':
                del items[i]
            case '+' if i == 0:
                del items[i]
            case '-' if i == 0:
                items[0:2] = [''.join(items[0:2])]
            case '*+':
                items[i] = '*'
            case '/+':
                items[i] = '/'
            case '*-':
                items[i] = '*'
                items[i+1] = '-' + items[i+1]
            case '/-':
                items[i] = '/'
                items[i+1] = '-' + items[i+1]
            case _:
                i += 1

    return items

def reduce_operators(item):
    sign = '+' if item.count('-') % 2 == 0 else '-'
    item = item.replace('+', '').replace('-', '')
    return item + sign

def do_math(items: list):
    i = 1 # first-order operations: * and /
    while i < len(items) and len(items) > 1:
        match items[i]:
            case '*': oper = mul
            case '/': oper = div
            case _: oper = None

        if oper:
            items[i-1:i+2] = [ oper(items[i-1], items[i+1]) ]
        else:
            i += 1

    i = 1 # addition and subtraction
    while i < len(items) and len(items) > 1:
        match items[i]:
            case '+': oper = add
            case '-': oper = sub

        items[i-1:i+2] = [ oper(items[i-1], items[i+1]) ]

    return items

calc(sample)

for expr, result in cases:
    assert calc(expr) == result
print('Tests passed.')