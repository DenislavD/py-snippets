from dataclasses import dataclass
from typing import Union

@dataclass
class Var:
    name: str
    def __repr__(self): return self.name
@dataclass
class App:
    fun: Union['Expr', str]; arg: 'Expr'
    def __repr__(self):
        f, a = self.fun, self.arg
        f = f if isinstance(f, str) else f.name if isinstance(f, Var) else f'({f})'
        a = a if isinstance(a, str) else a.name if isinstance(a, Var) else f'({a})'
        return f + a
@dataclass
class Lambda:
    param: Var
    body: 'Expr'
    def __repr__(self):
        return f'L{self.param.name}.{self.body}'
Expr = Var | Lambda | App

x, y, z = Var('x'), Var('y'), Var('z')

def T(var: Var, expr: Expr):
    print(f'T({var}, {expr})')
    match expr:
        case Var() if var == expr:
            print('Rule 1')
            return 'I'
        case Var() | str():
            print('Rule 2')
            return App('K', expr)
        case Lambda(param, body):
            print(f'Compiling inner lambda, then continuing with {var}')
            compiled = T(param, body)
            return T(var, compiled)
        case App(func, arg):
            print('Rule 3')
            return App(App('S', T(var, func)), T(var, arg))


# test cases
t1 = Lambda(x, Lambda(y, App(y, x)))
t2 = Lambda(x, Lambda(y, App(x, y)))
t3 = Lambda(x, x)
t4 = Lambda(x, Lambda(y, Lambda(z, App( x, App(y, z) )))) # λxyz.x(yz)
t5 = Lambda(x, Lambda(y, Lambda(z, App( App(x, z), y )))) # λxyz.xzy
t6 = Lambda(x, Lambda(y, x))

l = t6
res = T(l.param, l.body)
print('Result:', res)
