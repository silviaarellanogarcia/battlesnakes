import random

def choose_safe_random_move(game_state):
    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    # Prevent Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of head
    my_neck = game_state["you"]["body"][1]  # Coordinates of "neck"
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
    
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
    
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
    
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # Prevent the snake from moving out of the edges of the board
    if my_head["x"] == 0:  # Left edge
        is_move_safe["left"] = False
    elif my_head["x"] == board_width - 1:  # Right edge
        is_move_safe["right"] = False
    if my_head["y"] == 0:  # Bottom edge
        is_move_safe["down"] = False
    elif my_head["y"] == board_height - 1:  # Upper edge
        is_move_safe["up"] = False

    # Prevent the snake from colliding with itself
    my_body = game_state['you']['body']
    if {"x": my_head["x"] + 1, "y": my_head["y"]} in my_body:
        is_move_safe["right"] = False
    elif {"x": my_head["x"] - 1, "y": my_head["y"]} in my_body:
        is_move_safe["left"] = False
    elif {"x": my_head["x"], "y": my_head["y"] + 1} in my_body:
        is_move_safe["up"] = False
    elif {"x": my_head["x"], "y": my_head["y"] - 1} in my_body:
        is_move_safe["down"] = False

    # Prevent the snake from colliding with other snakes
    opponents = game_state['board']['snakes']
    for opponent in opponents:
        snake_body = opponent['body']
        if {"x": my_head["x"] + 1, "y": my_head["y"]} in snake_body:
            is_move_safe["right"] = False
        elif {"x": my_head["x"] - 1, "y": my_head["y"]} in snake_body:
            is_move_safe["left"] = False
        elif {"x": my_head["x"], "y": my_head["y"] + 1} in snake_body:
            is_move_safe["up"] = False
        elif {"x": my_head["x"], "y": my_head["y"] - 1} in snake_body:
            is_move_safe["down"] = False

    valid_moves = [move for move, safe in is_move_safe.items() if safe]
    if len(valid_moves) == 0:
        next_move = "up"
    else:
        next_move = random.choice(valid_moves)

    return next_move