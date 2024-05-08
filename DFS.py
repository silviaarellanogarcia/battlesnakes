from collections import deque

class DFS:
    def __init__(self, graph):
        self.graph = graph

    def calculate_paths_to_goals(self, start, goals):
        paths_to_goals = {goal: [] for goal in goals}
        queue = deque([(start, [start])])  # (node, path)
        first = True
        while queue:
            current_node, path = queue.popleft()
            if not first and current_node in goals.keys():
                if len(path) > len(paths_to_goals[current_node]):
                    paths_to_goals[current_node] = path
            else:
                first = False
                for neighbor in self.graph.get_neighbors(current_node):
                    if neighbor not in path:
                        new_path = path + [neighbor]
                        queue.append((neighbor, new_path))
        return paths_to_goals

    def choose_paths_to_scape(self, start, goals):
        paths_to_goals = self.calculate_paths_to_goals(start, goals)
        best_path = None
        best_score = -float('inf')
        best_goal = -1
        
        
        for goal, steps in goals.items():
            path = paths_to_goals[goal]
            score = len(path) - steps
            print(f"GOAL: {goal}, len: {len(path)}, steps: {steps}, score: {score}")
            if score > best_score:
                best_path = path
                best_score = score
                best_goal = goal
        print(f"Best GOAL: {best_goal}, score: {best_score}")
        return best_path