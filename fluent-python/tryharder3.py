# from Fluent Python - data structures

a, b, *rest = range(5)
print('With tail*:', a, b, *rest)

a, *body, c, d = range(5)
print('With body*:', a, *body, c, d)

*head, c, d = range(5)
print('With head*:', *head, c, d)

# in console you can do: a, b on one line

metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
]

print(f'{"Western hemisphere":20} | {"latitude":>9} | {"longitude":>9}')
for record in metro_areas:
    match record:
        case [str(name), _, _, (float(lat), float(lon)) as coord] if lon <= 0: # CHECKS types, x convert
            print(f'{name:20} | {lat:9.4f} | {lon:9.4f}')
            print(coord)


# slices as objects
headers = 'Number', 'Description', 'Values (USD)'
first_line = '123', 'Nails', '153.22'
text = '{:15}{:15}{:15}\n{:15}{:15}{:15}'.format(*headers, *first_line)

NUMBER = slice(0, 15)
DESCRIPTION = slice(15, 30)
VALUE = slice(30, 45)

for line in text.split('\n'):
    print(line[NUMBER], line[DESCRIPTION], line[VALUE])

# flat sequences (str, bytes, array.array) and memoryviews
from array import array
arr = array('d', [9.46, 13.02, 5, 0]) # one object in C with the same type of items in it
print(arr)

octets = array('B', range(6)) # array of 6 bytes
m1 = memoryview(octets)
print(m1.tolist())
m2 = m1.cast('B', [2, 3]) # can also use NumPy for this in an easier way
print(m2.tolist(), m2.itemsize)
