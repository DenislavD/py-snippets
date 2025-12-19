grid1= ["                      ",
        "   +-------+          ",
        "   |      +++---+     ",
        "X--+      +-+   X     "]

grid2= ["                    ",
        "     +--------+     ",
        "  X--+        +--+  ",
        "                 |  ",
        "                 X  ",
        "                    "]

grid3= ["X-----|----X"]

import logging
from collections import namedtuple
Coords = namedtuple('Coords', 'row, col')

log = logging.getLogger(__name__)
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.WARNING) # DEBUG INFO WARNING
log.debug('Starting..')

def line(grid): # for codewars
    return Line(grid).is_a_line

class Line:
    DIRECTIONS = { 'u': Coords(-1, 0), 'd': Coords(1, 0), 'l': Coords(0, -1), 'r': Coords(0, 1) }

    def __init__(self, grid):
        self.grid = grid
        self.rows, self.cols = len(grid), len(grid[0])
        flattened = ''.join(row for row in grid)
        self.X1 = Coords(*divmod(flattened.find('X'), self.cols))
        self.X2 = Coords(*divmod(flattened.rfind('X'), self.cols))
        log.debug(f'Rows:{self.rows}, cols:{self.cols}, X1:{self.X1}, X2:{self.X2}')
        
        self.stepped_on = []
        self.curr_pos = self.X1 # start walk from X1
        self.prev_pos = self.last_move = None
        self.reverse = False

        self.is_a_line = False
        self.start_walk()


    def get_directions(self, char, prev):
        directions = list(self.DIRECTIONS.keys())
        if char == '|' or char == '-':
            directions = [prev] # 'u'
        elif char == '+':
            directions = directions[2:] if prev in 'ud' else directions[:2]
        log.debug(f'Dirs: {directions}')
        return directions


    def look_ahead(self, directions):
        options = []
        for option in directions:
            test_pos = Coords(self.curr_pos.row + self.DIRECTIONS[option].row, 
                self.curr_pos.col + self.DIRECTIONS[option].col)
            if self.check_tile(test_pos, option):
                options.append((test_pos, option))

        log.info(f'{len(self.stepped_on)}: END LOOKAHEAD, {options}')
        if len(options) == 1: return options[0]
        

    def check_tile(self, coord, direction) -> bool:
        log.debug(f'Testing: {coord}')
        allowed_next = ('|', '+', 'X') if direction in 'ud' else ('-', '+', 'X')

        if coord.row < 0 or coord.row >= self.rows or coord.col < 0 or coord.col >= self.cols:
            log.debug(f'- Outside grid at {coord}')
            return False
        elif self.grid[coord.row][coord.col] not in allowed_next:
            log.debug(f'- Next not allowed at {coord}')
            return False
        elif coord in self.stepped_on:
            log.debug(f'- Already stepped on {coord}')
            return False
        return True


    def try_reverse(self):
        log.info('Failure, trying reverse path')
        self.stepped_on = []
        self.curr_pos = self.X2
        self.prev_pos = self.last_move = None
        self.reverse = True        


    def start_walk(self):
        while True:
            # try a step
            log.debug(f'Step: {len(self.stepped_on)}')
            directions = self.get_directions(self.grid[self.curr_pos.row][self.curr_pos.col], self.last_move)
            step = self.look_ahead(directions)
            
            if step: # prepare for next step
                self.prev_pos = self.curr_pos
                self.stepped_on.append(self.prev_pos)
                self.curr_pos, self.last_move = step

                if(self.grid[self.curr_pos.row][self.curr_pos.col] == 'X'): # end
                    self.stepped_on.append(self.curr_pos)
                    line_length = len(''.join(row for row in self.grid).replace(' ', ''))
                    if line_length == len(self.stepped_on):
                        self.is_a_line = True
                        break
                    else:
                        log.debug('Lengths are not the same')
                        if not self.reverse:
                            self.try_reverse()
                        else:
                            self.is_a_line = False
                            break             

            else: # can't go anywhere or too many options
                if not self.reverse:
                    self.try_reverse()
                else:
                    log.debug('Failure with reverse, exiting')
                    self.is_a_line = False
                    break

# tests
line1 = Line(grid1)
assert line1.is_a_line == True, 'reverse'
line2 = Line(grid2)
assert line2.is_a_line == True, 'simple'
line3 = Line(grid3)
assert line3.is_a_line == False

