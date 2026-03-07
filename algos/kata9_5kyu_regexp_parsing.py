import re
from random import randint

def roll(desc, verbose=False):
    def roll_dice(times, side):
        times = int(times) or 1
        return [randint(1, int(side)) for _ in range(int(times))]

    if not desc or not isinstance(desc, str): return False

    desc = re.sub(r'\s', '', desc) # remove whitespace
    if matchez := re.search(r'(^\d*d\d*)(.*)', desc):
        groups = matchez.groups()
        print(f'{groups=}') # ~ ('2d6', '+3')

        mods_list = re.split(r'(\+?-?\d+)', groups[1]) # ['', '+3', '', '-1', '']
        print(f'{groups}, res: {[int(n) for n in mods_list if n]}')
        try:
            print(f'{groups}, res: {[int(n) for n in mods_list if n]}')
            modifier = sum(int(n) for n in mods_list if n)
        except Exception as e:
            return False

        print(groups[0].split('d'))
        dice_result = roll_dice(*groups[0].split('d'))
        print(f'{dice_result=}')

        if verbose:
            return {'dice': dice_result, 'modifier': modifier}
        else:
            return sum(dice_result) + modifier

    return False


desc = '10d12 +9 +10' # '2d6+3-1 ' # ' 3d7  + 3 -1 ' '2d6++4' 'abc 2d6+3'
res = roll(desc, True)
print(f'{res=}')


