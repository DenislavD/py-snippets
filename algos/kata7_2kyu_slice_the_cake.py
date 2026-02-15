# Task: Cut a rectangular cake in equal pieces, so each has one raisin in it.
def cut(cake):
    # Time complexity: Assume n=raisins, m=shapes, k=cake area.
    #   Create arrays/views, count raisins, get shapes, helper funcs O(k) each,
    #   Main logic: worst case O(m^n), best case O(m*n). Final: O(m^n + k)
    # Space complexity: New bytearrays, output O(k) each, table O(n*k),
    #   Deadends worst case O(m^n), cuts O(n). Final: O(m^n + n*k)

    # calculate all n rectangular divisors of area
    def get_shapes(x, y, parts=1) -> list:
        shapes = []
        area = (x * y) // parts
        for i in range(1, area + 1):
            whole, decimals = divmod(area, i)
            if all([decimals == 0, i <= x, whole <= y]):
                shapes.append((i, whole))
        return shapes
    
    # check if cake can be cut in this shape with 1 raisin in it
    def check_cut(cake_view, form_view, start, shape) -> int:
        start_row, start_col = start
        end_row, end_col = start_row + shape[0], start_col + shape[1]
        if end_row > rows or end_col > cols:
            return -1

        result = 0
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                result += cake_view[row, col] + form_view[row, col]
        return result

    # reflect the cut in the form
    def make_cut(cake_form, start, shape):
        start_row, start_col = start
        end_row, end_col = start_row + shape[0], start_col + shape[1]

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                cake_form[col + row * cols] = 1

    # find next starting piece
    def get_next_start(cake_form):
        start = cake_form.find(0)
        if start == -1: return False
        return divmod(start, cols)

    # return cake cuts in requested output format
    def return_cuts(table, shapes: list):
        start = 0, 0
        output = [''] * len(shapes)
        for i, shape in enumerate(shapes):
            start_row, start_col = start
            end_row, end_col = start_row + shape[0], start_col + shape[1]
            
            for row in range(start_row, end_row):
                for col in range(start_col, end_col):
                    output[i] += 'o' if view[row, col] else '.'
                output[i] += '\n'
            start = get_next_start(table[i + 1]) # re-use saved form steps
        return output
    
    # initialize vars
    rows = len(cake.split())
    cols = len(cake.split()[0])
    cake_barr = bytearray(1 if bite == 'o' else 0 for bite in cake.replace('\n', ''))
    view = memoryview(cake_barr).cast('B', shape=[rows, cols])
    raisins = cake.count('o')
    shapes = get_shapes(rows, cols, raisins) # already sorted
    
    # main solution pathway
    table = [[]] * (raisins + 1) # holds the current step's cake_barr form
    table[0] = bytearray(len(cake_barr)) # initialize with full cake
    deadends = []
    cuts = []

    while len(cuts) < raisins:
        dead = True
        cake_form_current = table[len(cuts)]
        view_form = memoryview(cake_form_current).cast('B', shape=[rows, cols])

        start = get_next_start(cake_form_current)
        # print(start, )
        for shape in shapes:
            # print(f'Check_cut {cuts=} with {shape}: {check_cut(view, view_form, start, shape)}')
            candidate = [*cuts, shape]
            if candidate not in deadends and check_cut(view, view_form, start, shape) == 1:
                next_form = cake_form_current.copy()
                make_cut(next_form, start, shape)
                cuts.append(shape)
                table[len(cuts)] = next_form
                dead = False
                # print(f'Cut {shape}, {cuts=}')
                break # move forward
            else:
                # print('DEAD', candidate)
                deadends.append(candidate)

        if dead:
            deadends.append(cuts.copy())
            # print(f'{deadends=}')
            if [] in deadends:
                return [] # no solution
            cuts.pop() # go 1 step back
    
    output = return_cuts(table, cuts)
    output = [row.strip() for row in output]
    return output

# test suite
# c = '''
# ................
# .....o..........
# ................
# ...............o
# ................
# ................
# ................
# .....o..o.....o.
# ................
# ................
# ...o............
# ................
# ................
# ...............o
# ................
# .o..............
# '''.strip() # test 4 hard
# # c = '''
# # .o.o....
# # ........
# # ....o...
# # ........
# # .....o..
# # ........
# # '''.strip() # test 2 medium
# # c = '''
# # ........
# # ..o.....
# # ...o....
# # ........
# # '''.strip() # test 1

# from pprint import pprint
# pprint(cut(c), width=20)

