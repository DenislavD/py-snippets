from heapq import *
from dataclasses import dataclass, field # allows us to customize how individual attributes behave in a dataclass
from typing import Any
from itertools import count

@dataclass(order=True)
class PrioritizedItem:
	priority: int
	counter: int # tie-breaker, without it = random order for equal elements
	item: Any=field(compare=False) # without the type annotation, compare=False doesn't even work

counter = count() # iterator
heap = []
heappush(heap, PrioritizedItem(12, next(counter), 'D'))
heappush(heap, PrioritizedItem(12, next(counter), 'C'))
heappush(heap, PrioritizedItem(12, next(counter), 'B'))
heappush(heap, PrioritizedItem(12, next(counter), 'A'))
heappush(heap, PrioritizedItem(2, next(counter), 'E'))

print('Heap:', heap) # not sorted here, pops "sort" it.
while heap:
	#print(*map(lambda x: x.item, heap))
	print(heappop(heap).item, end=' -> \n')


# merge
result = list(merge([1, 3, 5], [2, 4]))
# Result: [1, 2, 3, 4, 5]
"merge maintains a min-heap of (value, sequence_index, item_index) tuples,"
"always pulling the smallest value from the 'front' of each sequence."
# (compares their front items with each other)


# Median Maintenance problem
class RunningMedian:
	def __init__(self, seq=None): # allow sorted list instantiation, avoid mutable default argument [] !
		self.heap_lower = []
		self.heap_upper = []
		
		if seq:
			for num in seq:
				self.add(num)

	def add(self, num):
		# push to one of the heaps
		if self.heap_lower and num < -self.heap_lower[0]:
			heappush(self.heap_lower, -num)
		else:
			heappush(self.heap_upper, num)
		# rebalance if needed
		if len(self.heap_lower) > len(self.heap_upper):
			item = heappop(self.heap_lower)
			heappush(self.heap_upper, -item)
		elif len(self.heap_upper) > len(self.heap_lower) + 1:
			item = heappop(self.heap_upper)
			heappush(self.heap_lower, -item)

	def get_median(self):
		if not self.heap_upper:
			raise ValueError('Add some numbers to the sequence first.')
		
		if len(self.heap_lower) == len(self.heap_upper):
			median = (-self.heap_lower[0] + self.heap_upper[0]) / 2
		else:
			median = self.heap_upper[0]
		return float(median)

	def __repr__(self):
		return f'Lower: {self.heap_lower}, Upper: {self.heap_upper}, Median: {self.get_median()}'


t = RunningMedian([1, 2, 3, 4, 5, 60])
assert t.get_median() == 3.5, 'Median should be 3.5'

tracker = RunningMedian()
tracker.add(5)
assert tracker.get_median() == 5.0
tracker.add(15)
assert tracker.get_median() == 10.0
tracker.add(1)
assert tracker.get_median() == 5.0
tracker.add(3)
assert tracker.get_median() == 4.0
tracker.add(10)
assert tracker.get_median() == 5.0
tracker.add(8)
assert tracker.get_median() == 6.5
print(tracker)
