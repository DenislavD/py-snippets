from itertools import accumulate, repeat, batched, compress, groupby
import operator

# function for factorial of n
def factorial_seq(n):
	result = accumulate(range(1, n + 1), operator.mul)
	for x in result:
		print(x)
factorial_seq(5)

# loan of 500 with 1% interest and 12 payments of 40
# The function should accept two arguments, an accumulated total and a value from the iterable.
def get_pmnts(balance, pmt): 
	#print('Bal:', balance, 'Payment:', pmt)
	return round(balance * 1.01, 0) - pmt

res = accumulate(repeat(40, 12), get_pmnts, initial=500)
print(list(res))


# batched: last batch may be shorter
flattened_data = ['Kori', 25, 'Pernik', 'Lemur', 55, 'Kamchatka', 'Alendi', 38, 'Sofia', '??',]
for batch in batched(flattened_data, 3, strict=False):
	if len(batch) == 3: # could also do try/except
		name, age, city = batch # unpacking
		print(f'{name} lives in {city} at {age}')


# compress
data = ['Alexy', 'Pecko', 'Jodi', 'Kori', 'Raly', ]
selectors = ['Y', '', 'Y', '', 'Y']

res = compress(data, selectors)
print('Filtered:', list(res))

res2 = filter(lambda x: x[1] == 'Y', zip(data, selectors))
print('Filtered2:', list(res2))

# groupby
groups = []
for key, group in groupby(data, len): # returns iterators itself
	groups.append((key, *group)) # *group also works
print(groups)
