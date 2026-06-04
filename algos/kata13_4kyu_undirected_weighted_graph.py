from bisect import insort

AdjacencyList = list[list[str | list[tuple[str, int]]]]
Dictionary = dict[str, list[tuple[str, int]]]
Matrix = list[list[int]]

class Graph:
    def __init__(self, order: int):
        # the *order* of a graph is its number of vertices (nodes)
        self.order = order
        self.A = 'A'
        self.matrix = [[0] * self.order for _ in range(self.order)] # empty matrix

    def list_2_graph(self, lst: AdjacencyList) -> Dictionary:
        return {key: value for key, value in lst}
    
    def graph_2_list(self, dictionary: Dictionary) -> AdjacencyList:
        return [[key, value] for key, value in sorted(dictionary.items())]

    def mat_2_list(self, matrix: Matrix) -> AdjacencyList:
        return [[self.A + str(i), [(self.A + str(j), w) for j, w in enumerate(row) if w]] 
                                                        for i, row in enumerate(matrix)]

    def adjmat_2_graph(self, matrix: Matrix) -> Dictionary:
        return {self.A + str(i): [(self.A + str(j), w) for j, w in enumerate(row) if w]
                                                        for i, row in enumerate(matrix)}

    def list_2_mat(self, lst: AdjacencyList) -> Matrix:
        for row, elements in lst:
            rowno = int(row[1:])
            for elem, weight in elements: # ('A5', 2)
                colno = int(elem[1:])
                self.matrix[rowno][colno] = weight
        return self.matrix

    def graph_2_mat(self, dictionary: Dictionary) -> Matrix:
        for row, elements in sorted(dictionary.items()):
            rowno = int(row[1:])
            for elem, weight in elements: # ('A5', 2)
                colno = int(elem[1:])
                self.matrix[rowno][colno] = weight
        return self.matrix

    def find_all_paths(self, dict_: Dictionary, start: str, end: str) -> list[str]:
        if start == end:
            return [end]

        result = []
        working_dict = dict(dict_) # copy
        if start in working_dict:
            for key, _ in sorted(working_dict.pop(start)):
                sequences = self.find_all_paths(working_dict, key, end)
                for seq in sequences:
                    insort(result, '-'.join([start, seq]), key=len)

        return result


# test conversions
dict_ = {'A4': [('A1', 5), ('A2', 7), ('A3', 9)], 'A1': [('A0', 2), ('A2', 3), ('A3', 8), ('A4', 5)], 'A2': [('A1', 3), ('A4', 7)], 'A0': [('A1', 2), ('A3', 6)], 'A3': [('A0', 6), ('A1', 8), ('A4', 9)]}
mat = [[0, 2, 0, 6, 0], [2, 0, 3, 8, 5], [0, 3, 0, 0, 7], [6, 8, 0, 0, 9], [0, 5, 7, 9, 0]]
list_ = [
    ['A0', [('A1', 2), ('A3', 6)]], 
    ['A1', [('A0', 2), ('A2', 3), ('A3', 8), ('A4', 5)]], 
    ['A2', [('A1', 3), ('A4', 7)]],
    ['A3', [('A0', 6), ('A1', 8), ('A4', 9)]],
    ['A4', [('A1', 5), ('A2', 7), ('A3', 9)]], 
]

graph = Graph(5)

assert graph.list_2_graph(list_) == dict_
assert graph.graph_2_list(dict_) == list_

assert graph.mat_2_list(mat) == list_
assert graph.adjmat_2_graph(mat) == dict_

assert graph.list_2_mat(list_) == mat
assert graph.graph_2_mat(dict_) == mat

# test paths
dict_ = {
  'A0': [('A3', 1), ('A4', 1)],
  'A1': [('A0', 1), ('A2', 1), ('A3', 1), ('A5', 1)],
  'A2': [('A1', 1), ('A2', 1), ('A3', 1), ('A4', 1)],
  'A3': [('A0', 1), ('A2', 1)],
  'A4': [('A1', 1), ('A2', 1), ('A3', 1), ('A5', 1)],
}
paths = graph.find_all_paths(dict_, 'A1', 'A3')
assert paths == ['A1-A3', 'A1-A0-A3', 'A1-A2-A3', 'A1-A0-A4-A3', 'A1-A2-A4-A3', 'A1-A0-A4-A2-A3']