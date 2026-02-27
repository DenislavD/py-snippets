from time import perf_counter

def combos(n: int) -> list[list[int]]:
    # Dynamic programming: Tabulation
    # Time complexity: O(2^n) appends in main loop, 
    # O(n * 2^n) remove duplicates => final O(n * 2^n)
    # Space complexity: O(2^n * n) new subarrays
    table = [[] for _ in range(n + 1)]
    table[0] = [[0]]
    table[1] = [[1]]

    for i in range(2, n + 1):
        for entry in table[i - 1]:
            # append 1 to each seq
            table[i].append([*entry, 1])
            # add one to the last number in each seq
            modified = sorted(entry[:-1] + [entry[-1] + 1], reverse=True)
            table[i].append(modified)

        # remove duplicates
        table[i] = list(map(list, set(map(tuple, table[i]))))

    return table[n]

n = 30 # can't go > 60 :/
t1 = perf_counter()
res = combos(n)
t2 = perf_counter()
print(f'{len(res)} combos for {n} in {round(t2 - t1, 2)}s')

