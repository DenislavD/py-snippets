from dataclasses import dataclass
from typing import Union
import re

@dataclass
class Var: name: str
@dataclass
class Lambda: param: Var; body: 'Expr'
@dataclass
class App:
    fun: Union['Expr', str]; arg: 'Expr'
    def __str__(self):
        f, a = self.fun, self.arg
        f = f if isinstance(f, str) else f.name if isinstance(f, Var) else f'({f})'
        a = a if isinstance(a, str) else a.name if isinstance(a, Var) else f'({a})'
        return f + a
Expr = Var | Lambda | App


def T(var: Var, expr: Expr):
    """Recursively walk an Expression to convert it to a SKI combination"""
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


def create_expression(s) -> Expr:
    text = f'({s})' # add outer brackets to simplify loop
    result_obj = ''

    replacements = []
    while res:= re.search(r'\([^()]*\)', text):
        repl_id = str(len(replacements))
        subexpr = res.group()

        lambda_: Expr = str2lambda(subexpr[1:-1])
        replacements.append(repr(lambda_))
        text = text.replace(subexpr, repl_id) # reduce processing string

    for i, r in enumerate(replacements): # do replacements
        for ind in range(i):
            replacements[i] = replacements[i].replace(f"Var(name='{ind}')", replacements[ind])

    return eval(replacements[-1]) # last item is the full expression


def str2lambda(s) -> Expr:
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

    # create left-associative tree from flat list
    body = list(body)
    holder = Var(body.pop(0))
    while len(body) > 0:
        holder = App(holder, Var(body.pop(0)))

    if structure:
        inner.body = holder
        return structure # Lambda(s)
    return holder # App only
    

def eliminate(s):
    print(s)
    structure = create_expression(s)
    result = T(structure.param, structure.body)
    return str(result)


if __name__ == '__main__':
    import sys
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
    t9 = "λa.aaaa", None
    t10 = "'λabcde.b(a(da))(ac)(cc)'", None
    tests = [t1, t2, t3, t4, t5, t6, t7]

    if len(sys.argv) > 1:
        for s, obj in tests:
            print(f'--------- TEST {s}, expected {str(obj)}')
            structure = create_expression(s)
            res2 = T(structure.param, structure.body)
            print(s, '->', str(res2))
            print()
    else:
        s = 'λa.a(aa)a(a(aa(a(a(a(a(aa))(aaa(aaaa(aa))))a)))(aaaa)(aa)(aa(a(aa)))(aa))'

        print(f'--------- TEST {s}')
        structure = create_expression(s)
        res2 = T(structure.param, structure.body)
        print(s, '->', str(res2))
        print()

