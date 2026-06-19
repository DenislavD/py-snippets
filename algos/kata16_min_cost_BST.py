import heapq
from collections import namedtuple, deque
Weighted = namedtuple('Weighted', ('weight', 'priority', 'value'))

class Tree:
    
    def __init__(self, root, left=None, right=None, parent=None):
        assert root and type(root) == Node
        if left: assert type(left) == Tree and left.root < root
        if right: assert type(right) == Tree and root < right.root
        if parent: assert type(parent) == Tree

        self.left = left
        self.root = root
        self.right = right
        self.parent = parent

    def is_leaf(self):
        return not(self.left or self.right)
        
    def __str__(self):
        return str(self.as_list()).replace(',', '').replace('\'', '')

    def as_list(self) -> list:
        if self.is_leaf():
            return [f'{self.root.value}:{self.root.weight}'] # [self.root.value]

        left = self.left.as_list() if self.left else '_'
        right = self.right.as_list() if self.right else '_'
        return [left, f'{self.root.value}:{self.root.weight}', right]

    def __eq__(self, other):
        return self.as_list() == other.as_list()

    def __ne__(self, other):
        return not self.__eq__(other)

    def insert(self, node):
        # find correct parent node
        current = self
        while current:
            if current.root > node and current.left:
                current = current.left
            elif current.root < node and current.right:
                current = current.right
            else:
                break

        # insert
        if current.root > node:
            current.left = Tree(node, parent=current)
        else:
            current.right = Tree(node, parent=current)

    def cost(self, depth=1):
        """Returns the cost of a tree which root is depth deep."""
        if not self:
            return 0
        
        left_cost = self.left.cost(depth + 1) if self.left else 0
        right_cost = self.right.cost(depth + 1) if self.right else 0
        return self.root.weight * depth + left_cost + right_cost

    # using L and R instead of self?!
    def rot_left(L) -> 'Tree':
        # print(f'Rotating {L.root.value} left')
        P = L.parent
        R = L.right
        L.right = R.left
        if R.left:
            R.left.parent = L
        R.left = L
        L.parent = R
        R.parent = P
        # update parent down link
        if P.left and P.left == L:
            P.left = R
        else:
            P.right = R
        return R

    def rot_right(R) -> 'Tree':
        # print(f'Rotating {R.root.value} right')
        P = R.parent
        L = R.left
        R.left = L.right
        if L.right:
            L.right.parent = R
        L.right = R
        R.parent = L
        L.parent = P
        # update parent down link
        if P.left and P.left == R:
            P.left = L
        else:
            P.right = L
        return L

    def inorder(self) -> ['Tree']:
        if not self: return []

        items = []
        if self.left: items += self.left.inorder()

        items += [self] # current item (starting)

        if self.right: items += self.right.inorder()
        return items

    def inlevelorder(self) -> ['Tree']:
        items = []
        queue = deque([self])
        while queue:
            if curr := queue.popleft():
                items += [curr]
                queue.extend([curr.left, curr.right])
        return items

    @classmethod
    def create_weighted(cls, list_):
        # create inverted min heap by weight and priority closer to the middle
        mid = len(list_) // 2
        heap = [Weighted(-item.weight, abs(mid-i), item.value) for i, item in enumerate(list_)]
        heapq.heapify(heap)

        holder = cls(Node('', -1)) # wrapper to always have parent, min value ''
        while True:
            try:
                popped = heapq.heappop(heap)
            except IndexError:
                break

            node = Node(popped.value, -popped.weight)
            holder.insert(node)

        return holder, holder.right

class Node: 

    def __init__(self, value, weight=1):
        self.value = value
        self.weight = weight

    def __str__(self):
        return '%s:%d' % (self.value, self.weight)   
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __eq__(self, other):
        return self.value == other.value 

    def __ne__(self, other):
        return self.value != other.value 


def compare_rotations(item, holder, i):
    curr_cost = holder.right.cost() # add last_action?
    swaps_cnt = 0

    #try left rotation
    if item.right:
        rotated = item.rot_left()
        new_cost = holder.right.cost()
        # print(f'{curr_cost=} vs {new_cost=}')
        if new_cost < curr_cost:
            curr_cost = new_cost
            swaps_cnt += 1
            print(f'-> LEFT ROTATION for {i}')
        else:
            # print('Reverting left rot..')
            rotated.rot_right()
        # print(f'Current tree: {holder.right}')

    #try right rotation
    if item.left:
        rotated = item.rot_right()
        new_cost = holder.right.cost()
        # print(f'{curr_cost=} vs {new_cost=}')
        if new_cost < curr_cost:
            curr_cost = new_cost
            swaps_cnt += 1
            print(f'-> RIGHT ROTATION for {i}')
        else:
            # print('Reverting right rot..')
            rotated.rot_left()
        # print(f'Current tree: {holder.right}')

    #try left-right rotation
    if item.right and item.parent is not holder and item.parent.left is item:
        rr = item.parent
        rotated_l = item.rot_left()
        rotated_r = rr.rot_right()
        new_cost = holder.right.cost()
        if new_cost < curr_cost:
            curr_cost = new_cost
            swaps_cnt += 2
            print(f'-> LEFT-RIGHT ROTATION for {i}')
        else:
            #print('Reverting left-right rot..')
            rotated_r.rot_left()
            rotated_l.rot_right()
        # print(f'Current tree: {holder.right}')

    #try right-left rotation
    if item.left and item.parent is not holder and item.parent.right is item:
        rl = item.parent
        rotated_r = item.rot_right()
        rotated_l = rl.rot_left()
        new_cost = holder.right.cost()
        if new_cost < curr_cost:
            curr_cost = new_cost
            swaps_cnt += 2
            print(f'-> RIGHT-LEFT ROTATION for {i}')
        else:
            #print('Reverting right-left rot..')
            rotated_l.rot_right()
            rotated_r.rot_left()
        # print(f'Current tree: {holder.right}')

    return swaps_cnt


def make_min_tree(node_list) -> Tree: # node_list is sorted in ascending order
    """Returns a minimal cost tree of all nodes in node_list."""

    holder, tree = Tree.create_weighted(node_list)
    print('Initial:', holder.right, holder.right.cost())

    i = swaps_cnt = 0
    items = tree.inorder() # list(reversed(tree.inorder()))
    # items.reverse()
    while i < len(items):
        # print('Current item:', id(items[i]), 'i:', i)
        curr_cnt = compare_rotations(items[i], holder, i)
        if curr_cnt:
            # print(f'Reset rotations on {i=}')
            i = 0
        else:
            i = i + 1 # reset rotations if swap
        swaps_cnt += curr_cnt

    print(holder.right, '--->', holder.right.cost(), 'Swaps:', swaps_cnt)
    return holder.right

cost = Tree.cost


# TESTS
node_list_0 = Node('A', 10), Node('B', 2), Node('C', 4), Node('D', 9), Node('E', 8)
node_list_1 = Node('A', 10), Node('B', 9), Node('C', 8), Node('D', 7), Node('E', 6)
node_list_2 = Node('A', 50), Node('B', 9), Node('C', 8), Node('D', 7), Node('E', 6)
node_list_3 = Node('A', 20), Node('B', 9), Node('C', 8), Node('D', 7), Node('E', 6)
node_list_4 = Node('A', 30), Node('B', 9), Node('C', 8), Node('D', 7), Node('E', 6)
node_list_5 = Node('A', 10), Node('B', 9), Node('C', 8), Node('D', 7), Node('E', 1)
nl = node_list_0, node_list_1, node_list_2, node_list_3, node_list_4, node_list_5
r1 = 65, 87, 138, 105, 118, 70

assertions = []
for nodes, result, i in zip(nl, r1, range(10)):
    tree = make_min_tree(nodes)
    assertions.append([i, ': ', tree.cost(), ' vs ', result])
    assert tree.cost() == result, f'{tree.cost()} is not equal to {result}'

for a in assertions:
    print(''.join(map(str, a)))
