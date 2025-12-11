# dynamic 4 tabulation
# Time: O(m * n * m) - last m is for the list split, Space: O(m)
# this is polynomial, not exponential, so okay-ish
def can_construct_dd(target, words):
	t_len = len(target)
	table = [False] * (t_len + 1)
	table[0] = True # skateboard

	for i, cell in enumerate(table):
		if cell is not False:
			for part in words:
				if target[i:].startswith(part):
					table[i + len(part)] = True
					if table[t_len]:
						return True
	return False

print(can_construct_dd('skateboard', ['bo', 'rd', 'ate', 't', 'ska', 'sk', 'boar'])) # False
print(can_construct_dd('abcdef', ['ab', 'abc', 'cd', 'def', 'abcd'])) # True
print(can_construct_dd('enterapotentpot', ['a', 'p', 'ent', 'enter', 'ot', 'o', 't'])) # True
print(can_construct_dd('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef', [
	'e',
	'ee',
	'eee',
	'eeee',
	'eeeee',
	'eeeeee',
	])) # False

