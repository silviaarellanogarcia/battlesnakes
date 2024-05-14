from collections import deque

class DFS:
    def __init__(self, graph):
        self.graph = graph

    def calculate_paths_to_goals(self, start, goals, max_depth):
        solution_path = []
        queue = deque([(start, [start])])  # (node, path)
        first = True
        while queue:
            current_node, path = queue.popleft()
            if len(path) >= max_depth:
                solution_path.append(path)
                continue
            if not first and current_node in goals.keys():
                if goals[current_node] - len(path) - 1 < 0:
                    solution_path.append(path)
                    break
            else:
                first = False
                for neighbor in self.graph.get_neighbors(current_node):
                    if neighbor not in path:
                        new_path = path + [neighbor]
                        queue.append((neighbor, new_path))
        return solution_path

    def choose_paths_to_scape(self, start, goals, max_depth):
        paths = self.calculate_paths_to_goals(start, goals, max_depth)
        best_path = None
        best_distance = float('inf')

        print('GOT %s paths' % len(paths))
        print(paths)
        
        for path in paths:
            dist = self.graph.get_distance(start, path[-1])
            if dist < best_distance:
                best_distance = dist
                best_path = path
                
        return best_path