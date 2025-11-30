def digitize(n): # my solution
    str_ = str(n)
    return [str_[i] for i in range(len(str_) - 1, -1, -1)]

print(digitize(2134))

def digitize2(n): # idiomatic
    return list(map(int, reversed(str(n))))

print(digitize2(2134))


# grid_traveler with memoization - time O(n*m) / space O(n+m) )
"DID IT ABSOLUTELY ALONE FOR 1.5H AFTER THE FIB DEMO !!!!! YEEEEEEEAH!"
def grid_traveler(x, y, memo={}):
    # base cases
    if x <= 1 or y <= 1: return 1 # can go only down or right, one direction blocked = 1
    if x == y == 2: return 2 # 2x2
    if x + y == 5: return 3 # 3x2 or 2x3

    # check if permutations already known
    if memo.get((x, y), False): return memo[(x, y)]
    if memo.get((y, x), False): return memo[(y, x)]
    # else - go deeper
    memo[(x, y)] = grid_traveler(x-1, y, memo) + grid_traveler(x, y-1, memo)
    print(f'Added to memo: {(x, y)} with value {memo[(x, y)]}')
    return memo[(x, y)]

# call func
print(grid_traveler(4, 4))

