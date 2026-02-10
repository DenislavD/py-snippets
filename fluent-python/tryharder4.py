# from Fluent Python - data structures: Mappings

from collections import defaultdict, OrderedDict
import copy

test = {1: 'Sofia', 2: 'Varna'}
d = dict(Alice=15, Johny=32, Stefi={'waitress': 'NY', 'age': 30, 'test': test})

# copy tests
d1 = d.copy()
d2 = copy.copy(d) # same as d.copy() ?
d3 = copy.deepcopy(d) # copies the obj references as new objects
test[2] = 'Burgas'
d.clear()
print(f'{d=}')
print(f'.copy():        {d1}')
print(f'copy.copy:      {d2}')
print(f'copy.deepcopy:  {d3}')

d5 = dict.fromkeys( ('a', 'b','c','d',) , False) # class method
print(f'fromkeys: {d5}')

item = d3.popitem()
print(f'popped: {item=} from {d3}')

d1.setdefault('Bob', {'a': 1}).update({'b': 2}) # default={'a': 1}
print(f'setdefault: Bob: {d1['Bob']}')

# OrderedDict
od = OrderedDict(d1.items())
od.move_to_end('Alice') # , last=False , unique to OrderedDict only
item = od.popitem(last=False)
print(f'{od}, popped: {item=}')

# defaultdict
dd = defaultdict(list)
dd |= d2 # Python 3.9+ -> in-place dict merging
dd['Bob'].append('something')
print(dd)
