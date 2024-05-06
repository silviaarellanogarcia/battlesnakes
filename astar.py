import heapq

class AStar:
    def __init__(self, graph):
        self.graph = graph

    def heuristic(self, node, goals):
        # Manhattan distance heuristic
        min_value = float('inf')
        for goal in goals:
            min_value = min(self.graph.get_distance(node, goal), min_value)
        
        return min_value

    def astar(self, start, goals, occupied_cells):
        open_set = [(0, start)]  # Priority queue of (f_score, node)
        came_from = {}  # Parent pointers
        g_score = {node: float('inf') for node in self.graph.graph}
        g_score[start] = 0
        f_score = {node: float('inf') for node in self.graph.graph}
        f_score[start] = self.heuristic(start, goals)
        visited = set()

        while open_set:
            current_f, current = heapq.heappop(open_set)
            if current in goals:
                path = self.reconstruct_path(came_from, current)
                return path

            if current in visited:
                continue
            visited.add(current)

            for neighbor in self.graph.get_neighbors(current):
                if neighbor in occupied_cells:
                    continue
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goals)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No path found

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
