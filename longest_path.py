def dfs(graph, current_node, end_node, visited, path, longest_path):
    visited.add(current_node)
    if current_node == end_node:
            longest_path = max(longest_path, path, key=len)
    for neighbor in graph.get_neighbors(current_node):
            if neighbor not in visited:
                    new_path = path + [neighbor]
                    longest_path = graph.dfs(neighbor, end_node, visited, new_path, longest_path)
    return longest_path

def longest_path_without_repetition(graph, start_node, end_node, occupied_cells):
    visited = set()
    longest_path = []
    cell_freed_longest_path = 0
    path = [start_node]

    for cell in occupied_cells.keys():
        aspiring_longest_path = graph.dfs(start_node, end_node, visited, path, longest_path)
        if len(aspiring_longest_path) - occupied_cells[graph.convert_to_tuple(cell)] > len(longest_path) - cell_freed_longest_path:
            longest_path = aspiring_longest_path
            cell_freed_longest_path = occupied_cells[graph.convert_to_tuple(cell)]

    return longest_path