from bisect import * # assumes ASCENDING order!

list_ = [0, 1, 4, 5, 7, 26]
list_rev = [17, 8, 1]
new_value = 3.5

insertion_point = bisect_left(list_, new_value) # O(log n) search (binary)
list_.insert(insertion_point, new_value)
print(f'New list1: {list_}')

# same as: bisect.insort_left(a, x, lo=0, hi=len(a), *, key=None)
insort_left(list_, new_value)
print(f'New list2: {list_}')

insort_left(list_rev, new_value, key=lambda x: -x) # for descending order
print(f'New list_rev: {list_rev}')

# task: use bisect to implement a custom priority list
from functools import cache
from operator import itemgetter
iterable = (('roger', 'young', 30), ('angela', 'jones', 28), ('bill', 'smith', 22), ('david', 'thomas', 32))

key_func = itemgetter(2)
print([x[2] for x in iterable])
print(sorted(key_func(x) for x in iterable))

by_age = sorted(iterable, key=key_func)
insort(by_age, ('asvaldi', 'kamey', 18), key=key_func) # loops array elements through key_func each time
print(by_age)


@cache
def key_func_cached(item):
	print(f'getting value for {item}')
	return item[2]

insort(by_age, ('azvaldi', 'rebit', 19), key=key_func_cached)
insort(by_age, ('azvaldi', 'lemur', 10), key=key_func_cached)
print(by_age)