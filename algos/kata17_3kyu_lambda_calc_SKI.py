from dataclasses import dataclass
from typing import Union
import re

@dataclass
class Var: name: str
@dataclass
class App:
    fun: Union['Expr', str]; arg: 'Expr'; prefix: str = ''
    def __str__(self):
        f, a = self.fun, self.arg
        f = f if isinstance(f, str) else f.name if isinstance(f, Var) else f'({f})'
        a = a if isinstance(a, str) else a.name if isinstance(a, Var) else f'({a})'
        return self.prefix + f + a
@dataclass
class Lambda: param: Var; body: 'Expr'
Expr = Var | Lambda | App


def T(var: Var, expr: Expr):
    match expr:
        case Var() if var == expr:
            return 'I'
        case Var() | str():
            return App('K', expr)
        case Lambda(param, body):
            compiled = T(param, body)
            return T(var, compiled)
        case App(func, arg):
            return App(App('S', T(var, func)), T(var, arg))


def get_subexpressions(s) -> list:
    text = f'({s})' # add outer brackets to simplify loop
    result_obj = ''

    while res:= re.search(r'\([^()]*\)', text):
        subexpr = res.group()
        
        lambda_ = str2lambda(subexpr[1:-1])
        result_obj = repr(lambda_).replace("Var(name='*')", result_obj)
        text = text.replace(subexpr, '*') # reduce processing string

    return eval(result_obj)


def str2lambda(s):
    structure = None

    if '.' in s:
        params, body = s.split('.')
        structure = Lambda(Var(params[1]), '') # 0 is the lambda, 1 is the root
        inner = structure
        for p in params[2:]:
            inner.body = Lambda(Var(p), '')
            inner = inner.body
    else:
        body = s

    # NEED TO CREATE TREE FROM LIST
    match len(body):
        case 1: holder = Var(body)
        case 2: holder = App(Var(body[0]), Var(body[1]))
        case 3: holder = App( App(Var(body[0]), Var(body[1])), Var(body[2]) )
        case 4: holder = App( App(Var(body[0]), Var(body[1])), App(Var(body[2]), Var(body[3])) )
        case _: holder = ''

    if structure:
        inner.body = holder
        return structure # Lambda(s)
    return holder # App only
    

def eliminate(s):
    print(s)
    structure = get_subexpressions(s)
    result = T(structure.param, structure.body)
    return str(result)


# test cases
x, y, z = Var('x'), Var('y'), Var('z')

t1 = 'λx.x', Lambda(x, x)
t2 = 'λxy.xy', Lambda(x, Lambda(y, App(x, y)))
t3 = 'λxy.yx', Lambda(x, Lambda(y, App(y, x)))
t4 = 'λx.xx', Lambda(x, App(x, x)) # SII
t5 = 'λxyz.x(yz)', Lambda(x, Lambda(y, Lambda(z, App( x, App(y, z) )))) # λxyz.x(yz)
t6 = 'λxyz.xzy', Lambda(x, Lambda(y, Lambda(z, App( App(x, z), y )))) # λxyz.xzy
t7 = 'λxy.x', Lambda(x, Lambda(y, x))
t8 = "λf.(λx.f(λy.xxy))(λx.f(λy.xxy))", None
tests = [t1, t2, t3, t4, t5, t6, t7]

# for s, obj in tests:
s, obj = t4
s = 'λa.aaaa'

# res1 = T(obj.param, obj.body)
# print('Result1:', res1)

print(f'--------- TEST {s}, expected {str(obj)}')
structure = get_subexpressions(s)
res2 = T(structure.param, structure.body)
print('Result2:', str(res2))
# assert res1 == res2

