# dynamic 3 tabulation
def can_sum_dd(target, arr): # Time: O(m*n), space: O(m) 
	table_len = target + 1
	table = [False] * table_len
	table[0] = True # can generate a 0 target by not getting any numbers from the array

	for i, cell in enumerate(table):
		if cell:
			for num in arr:
				if  i + num <= table_len - 1:
					#print(f'Enabling: {i + num}')
					table[i + num] = True # can generate this
					if table[table_len - 1] == True:
						return True
	return table[table_len - 1]

# print(can_sum_dd(7, [5, 4, 3]))
# print(can_sum_dd(300, [7, 14]))

# how sum
def how_sum_dd(target, arr):
	table = [False] * (target + 1)
	table[0] = []

	for i, cell in enumerate(table):
		if cell is not False:
			for num in arr:
				if i + num <= target:
					table[i + num] = [*cell, num]
					if table[target] is not False:
						return table[target]
	return table[target]

# print(how_sum_dd(7, [5, 4, 3]))
# print(how_sum_dd(8, [2, 1, 4]))
# print(how_sum_dd(300, [7, 15]))


def best_sum_dd(target, arr):
	table = [False] * (target + 1)
	table[0] = []

	for i, cell in enumerate(table):
		if cell is not False:
			for num in arr:
				if i + num <= target:
					candidate = [*cell, num]
					if table[i + num] is False or len(candidate) < len(table[i + num]):
						table[i + num] = candidate # check length at each step
	return table[target]

print(best_sum_dd(7, [5, 4, 3]))
print(best_sum_dd(8, [2, 1, 4]))
print(best_sum_dd(300, [7, 14]))

