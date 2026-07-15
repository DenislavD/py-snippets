# Descriptors I

# Simple workings
def triple(a):
    return f'Result is {a * 3}'
    # NB: every user-defined function has __get__

print('Regular call:', triple(1)) # -> 3, __get__ not called here, not in a class
# Simulating class behavior:
print('__get__ call 1:', triple.__get__('string')) # -> <bound method triple of 'string'>
triple.__get__('string')() # -> 'stringstringstring'

def get_override(self):
    print('__get__ overridden!')
    return f'Arg: {self}'
triple.__get__ = get_override

print('__get__ call 2:', triple.__get__('string')) # -> Arg: string, not callable


# Class workings
class Adder:
    # class attribute Adder.add is user function with auto __get__ , 
    def add(self, num): # so it's a non-data descriptor
        return num + 1

print(Adder.add) # <function Adder.add at 0x..>
inst = Adder()
bound = inst.add # <bound method Adder.add of <__main__.Adder object at 0x..>
# How ?
# add is an attribute on class Adder, which has __get__
# so on . access it gets called with the instance: Adder.add.__get__(inst)
# -> returns a wrapped function add(inst)
res = bound(2) # == add(inst, 2)
# How ?
# bound.__call__(*args):
#    return bound.__func__(bound.__self__, *args)
print(bound, res)
