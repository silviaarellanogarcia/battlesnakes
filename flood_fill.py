def flood_fill(board, start_x, start_y, visited):
    '''
    Algorithm to compute  the connected areas of the board. Start
    '''

    if start_x < 0 or start_x >= len(board) or start_y < 0 or start_y >= len(board[0]):
        return
    if board[start_x][start_y] != 'empty' or visited[start_x][start_y]:
        return

    # Mark the current cell as visited
    visited[start_x][start_y] = True

    # Recursively call flood_fill for adjacent cells
    flood_fill(board, start_x + 1, start_y, visited)
    flood_fill(board, start_x - 1, start_y, visited)
    flood_fill(board, start_x, start_y + 1, visited)
    flood_fill(board, start_x, start_y - 1, visited)


def get_territory(board, occ):
    """
    Determine the territories controlled by the snake using flood fill algorithm.
    """
    visited = [[False for _ in range(len(board[0]))] for _ in range(len(board))]
    territories = []

    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 'empty' and not visited[x][y]:
                territory = []
                flood_fill(board, x, y, visited)
                for i in range(len(board)):
                    for j in range(len(board[0])):
                        if visited[i][j]:
                            territory.append((i, j))
                territories.append(territory)

    return territories