from operator import attrgetter

class Tree:
    
    def __init__(self, root, left=None, right=None):
        assert root and type(root) == Node
        if left: assert type(left) == Tree and left.root < root
        if right: assert type(right) == Tree and root < right.root

        self.left = left
        self.root = root
        self.right = right

    def is_leaf(self):
        return not(self.left or self.right)
        
    def __str__(self):
        return str(self.as_list()).replace(',', '').replace('\'', '')

    def as_list(self) -> list:
        if self.is_leaf():
            return [f'{self.root.value}:{self.root.weight}']

        left = self.left.as_list() if self.left else '_'
        right = self.right.as_list() if self.right else '_'
        return [left, f'{self.root.value}:{self.root.weight}', right]

    def __eq__(self, other):
        return self.as_list() == other.as_list()

    def __ne__(self, other):
        return not self.__eq__(other)

    def cost(self, depth=1):
        """Returns the cost of a tree which root is depth deep."""
        if not self:
            return 0
        
        left_cost = self.left.cost(depth + 1) if self.left else 0
        right_cost = self.right.cost(depth + 1) if self.right else 0
        return self.root.weight * depth + left_cost + right_cost

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


cost = Tree.cost

def make_min_tree(node_list) -> Tree: # node_list is sorted in ascending order
    """
    Returns a minimal cost tree of all nodes in node_list.
    Dynamic programming: Tabulation approach with O(n^3) time and O(n^2) space complexity.
    """
    get_weight = attrgetter('weight')
    
    # initialize costs and roots tables
    n = len(node_list)
    t_costs = [[0] * (n + 1) for _ in range(n + 2)] # 1-based, first 0 row is empty/ignored
    t_roots = [[0] * n for _ in range(n)] # 0-based

    for row, node in enumerate(node_list):
        t_costs[row+1][row] = 0
        t_costs[row+1][row+1] = node.weight
    t_costs[row+2][n] = 0

    # fill in the tables
    for diagonal in range(n):
        for i in range(1, n + 1 - diagonal):
            j = diagonal + i

            min_ = float('inf')
            for mid in range(i, j + 1):
                cost = t_costs[i][mid-1] + t_costs[mid+1][j]
                if cost < min_:
                    min_ = cost
                    t_roots[i-1][j-1] = mid - 1 # record root node as 0-based
            t_costs[i][j] = min_ + sum(map(get_weight, node_list[i-1:j]))

    # construct tree, root table is 0-based
    root_index = t_roots[0][n-1]
    root_node = node_list[root_index]
    root = Tree(root_node)

    stack = [(root, 0, n-1)]
    while stack:
        tree, i, j = stack.pop()
        mid = t_roots[i][j]

        if mid < j: # build the right tree
            right_index = t_roots[mid+1][j]
            tree.right = Tree(node_list[right_index])
            stack.append((tree.right, mid + 1, j))

        if mid > i: # build the left tree
            left_index = t_roots[i][mid-1]
            tree.left = Tree(node_list[left_index])
            stack.append((tree.left, i, mid - 1))

    return root


# TESTS
node_list_0 = Node('A', 10), Node('B', 2), Node('C', 4), Node('D', 9), Node('E', 8)
node_list_1 = Node('A', 10), Node('B', 9), Node('C', 8), Node('D', 7), Node('E', 6)
node_list_2 = Node('A', 50), Node('B', 9), Node('C', 8), Node('D', 7), Node('E', 6)
node_list_3 = Node('A', 20), Node('B', 9), Node('C', 8), Node('D', 7), Node('E', 6)
node_list_4 = Node('A', 30), Node('B', 9), Node('C', 8), Node('D', 7), Node('E', 6)
node_list_5 = Node('A', 10), Node('B', 9), Node('C', 8), Node('D', 7), Node('E', 1)
node_list_LR = Node('A', 4), Node('B', 3), Node('C', 5)
node_list_RL = Node('A', 5), Node('B', 3), Node('C', 4)
nl = node_list_0, node_list_1, node_list_2, node_list_3, node_list_4, node_list_5, node_list_LR, node_list_RL
r1 = 65, 87, 138, 105, 118, 70, 21, 21

assertions = []
for nodes, result, i in zip(nl, r1, range(10)):
    tree = make_min_tree(nodes)
    assertions.append([i, ': ', tree.cost(), ' vs ', result])
    assert tree.cost() == result, f'{tree.cost()} is not equal to {result}'

for a in assertions:
    print(''.join(map(str, a)))
