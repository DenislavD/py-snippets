from collections import Counter
from itertools import permutations, chain
from copy import deepcopy

# the solution uses size*size matrix with sets of the possible values for each element
# the elements are referenced by pointers and modified in-place throughout the code
class CityBuilder:
    
    def __init__(self, clues):
        self.SIZE = len(clues) // 4
        self.INITIAL_OPTIONS = set(i for i in range(1, self.SIZE + 1)) # {1, 2, 3, 4..}
        self._ALL_PERMUTATIONS = list(permutations(self.INITIAL_OPTIONS))

        self.rows = [[self.INITIAL_OPTIONS.copy() for _ in range(self.SIZE)] 
                                                    for _ in range(self.SIZE)]
        self.cols = [[row[col] for row in self.rows] for col in range(self.SIZE)]
        self.clues = self.format_clues(clues)
        self._prev = []
        self._guess = dict(el=None, options=None, checkpoint=[])

    def run(self):
        while not self.check_win_condition():
            if self.rows != self._prev:
                self._prev = deepcopy(self.rows)
                
                for clue in self.clues:
                    self.process_clues(clue)
                self.promote_single_options()
                self.apply_rowcol_constraints()
                
            else: # no solution, need to guess
                if not self._guess['options']: # start new guess at longest unknown
                    guess = max(chain(*self.rows), key=len)
                    self._guess.update(el=guess, options=list(guess), checkpoint=deepcopy(self.rows))
                candidate = self._guess['options'].pop()
                self._guess['el'].add(candidate)
                self._guess['el'].intersection_update({candidate})
        
        return self.format_result()

    def format_clues(self, clues):
        formatted_clues = []
        for ind, clue in enumerate(clues):
            if clue > 0:
                match divmod(ind, self.SIZE):
                    case 0, col: rowcol = self.cols[col]
                    case 1, row: rowcol = self.rows[row][::-1]
                    case 2, col: rowcol = self.cols[self.SIZE-1-col][::-1]
                    case 3, row: rowcol = self.rows[self.SIZE-1-row]
                formatted_clues.append([clue, rowcol, None])
        return formatted_clues

    def process_clues(self, clue):
        visible_must, rowcol, combos = clue
        valid = []
        combos = combos or self._ALL_PERMUTATIONS # can be 5000, 4 in checks for each
        for combo in combos:
            flag = False
            for value, allowed in zip(combo, rowcol):
                if value not in allowed:
                    flag = True
                    break
            if flag: continue

            visible_cnt = 1
            for i in range(1, len(combo)):
                if combo[i] > max(combo[0:i]):
                    visible_cnt += 1
            if visible_cnt == visible_must:
                valid.append(combo)
        
        clue[2] = valid
        [rc.intersection_update(o) for o, rc in zip(zip(*valid), rowcol)] # adjust

    def apply_rowcol_constraints(self):
        for row in self.rows:
            for col, el in enumerate(row):
                if len(el) == 1:
                    [r.discard(*el) for r in row if len(r) != 1]
                    [c.discard(*el) for c in self.cols[col] if len(c) != 1]

    def promote_single_options(self):
        for rowcol in self.rows + self.cols:
            c = Counter(chain.from_iterable(rowcol)).most_common()
            for single, cnt in c[::-1]:
                if cnt == 1: # only 1 possible cell for a value
                    for el in rowcol:
                        if len(el) > 1 and single in el:
                            el.intersection_update({single})
                elif cnt > 1:
                    break

    def check_win_condition(self):
        flat = list(chain(*chain(*self.rows)))
        if len(flat) <= self.SIZE ** 2: # final stage
            sums_rows = [sum(chain(*r)) for r in self.rows]
            sums_cols = [sum(chain(*c)) for c in self.cols]
            if sums_rows == sums_cols:
                return True # solution found
            self.reset_to_checkpoint()
        return False

    def reset_to_checkpoint(self):
        self._prev = None
        self.rows = self._guess['checkpoint']
        self.cols = [[row[col] for row in self.rows] for col in range(self.SIZE)]
        self._guess.update(el=max(chain(*self.rows), key=len)) # re-instate link to _guess

    def format_result(self):
        return list(list(el.pop() for el in row) for row in self.rows)

    
def solve_puzzle(clues):
    builder = CityBuilder(clues)
    return builder.run()

clues = [0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0] # SIZE = 4
print(solve_puzzle(clues))

clues = (0,0,0,2,2,0, 0,0,0,6,3,0, 0,4,0,0,0,0, 4,4,0,3,0,0) # SIZE = 6
print(solve_puzzle(clues))

clues = [7,0,0,0,2,2,3, 0,0,3,0,0,0,0, 3,0,3,0,0,5,0, 0,0,0,0,5,0,4] # SIZE = 7, medium
print(solve_puzzle(clues))

clues = [0,2,3,0,2,0,0, 5,0,4,5,0,4,0, 0,4,2,0,0,0,6, 5,2,2,2,2,4,1] # SIZE = 7, very hard
print(solve_puzzle(clues)) # 0,0,0,0,0,0,0

clues = [0,2,3,0,2,0,0, 5,0,4,5,0,4,0, 0,4,2,0,0,0,6, 0,0,0,0,0,0,0] # SIZE = 7, _very_hard_
print(solve_puzzle(clues))

clues = [0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4, 7, 0, 0, 0, 2, 2, 3]
print(solve_puzzle(clues))

# medved - needs guessing
clues = [3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3]
print(solve_puzzle(clues)) 