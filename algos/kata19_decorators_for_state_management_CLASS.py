from time import time, sleep
from collections import defaultdict
from itertools import pairwise

""" How does it work?
instrument is a class decorator implementing the descriptor protocol.

If a function is decorated:
Decoration time: One instrument object is created
Call time: The instrument object's __call__ is invoked

If a method is decorated:
Decoration time: One instrument object is created
Call time:
Each time the decorated attribute on the user class is accessed with . notation,
it finds the descriptor instrument object saved in the class' __dict__ and
executes it's __get__ : userobj.deco_method => instrument.__get__(self, obj, cls),
which returns a NEW instance of the instrument decorator with the instance of the
user class passed in. Then when it is called: userobj.deco_method() ,
the __call__ method is invoked as usual, but now with the correct inst assigned.
"""

class instrument: # Descriptor (non-data)
    call_cnt = defaultdict(int)
    call_times = defaultdict(list)    

    def __init__(self, func, inst=None):
        self.func = func
        self.inst = inst
        self.key = str(func) + str(inst)

    def __call__(self, *args, **kwargs):
        instrument.call_cnt[self.key] += 1
        instrument.call_times[self.key] += [time()]
        if self.inst:
            return self.func(self.inst, *args, **kwargs)
        else:
            return self.func(*args, **kwargs)

    def __get__(self, obj, cls):
        return type(self)(self.func, obj) # make new instrument instance with inst == user cls obj

    def invocation_count(self):
        return instrument.call_cnt[self.key]

    def last_invocation_time(self):
        if len(instrument.call_times[self.key]) == 0:
            return None
        return instrument.call_times[self.key][-1]

    def avg_delay(self):
        if len(instrument.call_times[self.key]) < 2:
            return None
        sum_ = sum(b - a for a, b in pairwise(instrument.call_times[self.key]))
        return round(sum_  / (len(instrument.call_times[self.key]) - 1), 2)

    def reset_stats(self):
        instrument.call_cnt[self.key] = 0
        instrument.call_times[self.key] = []


@instrument
def test():
    print('running test')

test()
sleep(2)
test()
# test.reset_stats()
print('test', test.invocation_count(), test.last_invocation_time(), test.avg_delay())


# class test
class ClassTest():
    def __init__(self):
        ...

    @instrument
    def sayhi(self):
        print('running ClassTest.sayhi')

    def sayso(self):
        print('self.id:', id(self))


c_test = ClassTest()
c_test2 = ClassTest()

c_test.sayhi()
# sleep(1)
# c_test.sayhi()
# c_test.sayhi()
# c_test2.sayhi()
# c_test2.sayhi()
print('c_test:', c_test.sayhi.invocation_count(), \
    c_test.sayhi.last_invocation_time(), c_test.sayhi.avg_delay())

print('c_test2:', c_test2.sayhi.invocation_count(), \
    c_test2.sayhi.last_invocation_time(), c_test2.sayhi.avg_delay())
