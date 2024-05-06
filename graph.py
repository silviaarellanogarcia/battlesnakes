from singleton import SingletonMeta

class Graph(metaclass=SingletonMeta):
    def __init__(self, size):
        self.size = size
        self.graph = {}
        self.build_graph()

    def build_graph(self):
        rows, cols = self.size
        for i in range(rows):
            for j in range(cols):
                node = (i, j)
                neighbors = []
                # Move Up
                if i > 0:
                    neighbors.append((i - 1, j))
                # Move Down
                if i < rows - 1:
                    neighbors.append((i + 1, j))
                # Move Left
                if j > 0:
                    neighbors.append((i, j - 1))
                # Move Right
                if j < cols - 1:
                    neighbors.append((i, j + 1))
                self.graph[node] = neighbors
              
    def get_neighbors(self, node):
        return self.graph.get(node, [])

    @staticmethod
    def get_distance(node1, node2):
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    @staticmethod
    def convert_to_tuple(node):
        return (node['x'], node['y'])

    @staticmethod
    def difference(n1, n2):
        dx = n1[0] - n2[0]        
        dy = n1[1] - n2[1]
        return (dx, dy)
