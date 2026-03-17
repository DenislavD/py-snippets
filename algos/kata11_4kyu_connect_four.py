# connect four - who won https://www.codewars.com/kata/56882731514ec3ec3d000009
def who_is_winner(pieces_position_list):
    rows, cols = 7, 6 # transposed for easier token placing
    grid = [['-'] * cols for _ in range(rows)]
    turns = [('ABCDEFG'.index(t[0]), t[2]) for t in pieces_position_list]
    
    def get_diagonals_indexes(rows, cols) -> list[int]:
        diags = [ [[0, 0], ], ]
        for _ in range(rows + cols - 2): # total # of diagonals
            current = []
            for r, c in diags[-1]:
                if c + 1 < cols:
                    current.append([r, c + 1])
            if r + 1 < rows:
                current.append([r + 1, c])
            diags.append(current)
        return [diag for diag in diags if len(diag) >= 4]
    diags = get_diagonals_indexes(rows, cols)

    def check_win_condition(plr):
        check_right_diags = [''.join(grid[r][c] for r,c in diag) for diag in diags if len(diag) >= 4]
        check_left_diags = [''.join(grid[r][cols-1-c] for r,c in diag) for diag in diags if len(diag) >= 4]
        check_cols = [''.join(row[i] for row in grid) for i in range(cols)]
        check_rows = [''.join(row) for row in grid]

        vectors = check_right_diags + check_left_diags + check_cols + check_rows
        for vector in vectors:
            if plr * 4 in vector:
                return 'Yellow' if plr == 'Y' else 'Red'

    # play
    for col, plr in turns:
        grid[col][ grid[col].index('-') ] = plr # place token
        if result := check_win_condition(plr):
            return result

    return 'Draw'

assert who_is_winner(["A_Red","B_Yellow","A_Red","B_Yellow","A_Red","B_Yellow","G_Red","B_Yellow"]) == 'Yellow'
assert who_is_winner([ 
"C_Yellow", "E_Red", "G_Yellow", "B_Red", "D_Yellow", "B_Red", "B_Yellow", "G_Red", "C_Yellow", "C_Red",
"D_Yellow", "F_Red", "E_Yellow", "A_Red", "A_Yellow", "G_Red", "A_Yellow", "F_Red", "F_Yellow", "D_Red", 
"B_Yellow", "E_Red", "D_Yellow", "A_Red", "G_Yellow", "D_Red", "D_Yellow", "C_Red"
]) == 'Yellow'
assert who_is_winner(["A_Red", "B_Yellow", "A_Red", "E_Yellow", "F_Red", "G_Yellow", "A_Red", "G_Yellow"
    ]) == 'Draw'
