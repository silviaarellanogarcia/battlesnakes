from singleton import SingletonMeta

class Graph(metaclass=SingletonMeta):
    def __init__(self, size):
        self.size = size
        self.graph = {}
        self.build_graph()
        self.target_cells = {}

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

    @staticmethod
    def sum(n1, n2):
        dx = n1[0] + n2[0]        
        dy = n1[1] + n2[1]
        return (dx, dy)

    def flood_fill(self, start_node, blocked, max_steps=None):
        visited = set()
        blocking = {}
        to_explore = [(start_node, 0)]  # Tuple: (node, steps)
        while to_explore:
            current_node, steps = to_explore.pop()
            visited.add(current_node)
            if max_steps is not None and steps >= max_steps:  # Stop exploration if reached max steps
                continue
            for neighbor in self.get_neighbors(current_node):
                if neighbor not in visited:
                    block_score = blocked.get(neighbor, None)
                    if block_score is None:
                        to_explore.append((neighbor, steps + 1))
                    else:
                        blocking[neighbor] = block_score
        return visited, blocking

    def get_neighbor_info(self, node, blocked):
        neighbor_info = {}
        for neighbor in self.get_neighbors(node):
            if neighbor not in blocked:
                connected = []
                available_cells = None
                blocking_cells = None
                for neighbor2 in list(neighbor_info.keys()):
                    if neighbor in neighbor_info[neighbor2]['cells']:
                        connected.append(neighbor2)
                        neighbor_info[neighbor2]['connected'].append(neighbor)
                        available_cells = neighbor_info[neighbor2]['cells']
                        blocking_cells = neighbor_info[neighbor2]['block']

                if available_cells is None:
                    available_cells, blocking_cells = self.flood_fill(neighbor, blocked)
                neighbor_info[neighbor] = {
                    'cells': available_cells,
                    'block': blocking_cells,
                    'n_cells': len(available_cells),
                    'connected': connected
                }
        return neighbor_info