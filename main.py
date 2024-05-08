# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import json

from graph import Graph
from astar import AStar

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "silviaarellanogarcia, casassarnau",  # Your Battlesnake Username
        "color": "#f5429b",  # Choose color
        "head": "silly",  # Choose head
        "tail": "present",  # Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    Graph((game_state['board']['width'], game_state['board']['height']))
    print("GAME START")
    

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:
    graph = Graph((game_state['board']['width'], game_state['board']['height']))
    astar = AStar(graph)

    move_set = {
      (1, 0): "right", 
      (-1, 0): "left", 
      (0, 1): "up", 
      (0, -1): "down"
    }
    

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    occupied_cells = set()
    for snake in game_state['board']['snakes']:
        for cell in snake['body']:
            occupied_cells.add((cell['x'], cell['y']))

    food_cells = set()
    for food in game_state['board']['food']:
        food_cells.add((food['x'], food['y']))

    position = graph.convert_to_tuple(game_state['you']['head'])
    
    astar_path = astar.astar(
        position, food_cells, occupied_cells, len(game_state['you']['body']))

    print('POS: %s' % str(position))
    print('OCC: %s' % str(occupied_cells))
    print('FOOD: %s' % str(food_cells))
    print('PATH: %s' % str(astar_path))

    astar_path = None
    if astar_path is None:
        print("RANDOM")
        is_move_safe = {
              "up": True, 
              "down": True, 
              "left": True, 
              "right": True
            }

        # We've included code to prevent your Battlesnake from moving backwards
        my_head = game_state["you"]["body"][0]  # Coordinates of your head
        my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
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

        if my_head["x"] == 0:  # Left edge
            is_move_safe["left"] = False
        elif my_head["x"] == board_width - 1:  # Right edge
            is_move_safe["right"] = False
        if my_head["y"] == 0:  # Bottom edge
            is_move_safe["down"] = False
        elif my_head["y"] == board_height - 1:  # Upper edge
            is_move_safe["up"] = False

        my_body = game_state['you']['body']
        print(my_body)
        if {"x": my_head["x"] + 1, "y": my_head["y"]} in my_body:
            is_move_safe["right"] = False
        elif {"x": my_head["x"] - 1, "y": my_head["y"]} in my_body:
            is_move_safe["left"] = False
        elif {"x": my_head["x"], "y": my_head["y"] + 1} in my_body:
            is_move_safe["up"] = False
        elif {"x": my_head["x"], "y": my_head["y"] - 1} in my_body:
            is_move_safe["down"] = False

        
        
        valid_moves = [move for move, safe in is_move_safe.items() if safe]
        next_move = random.choice(valid_moves)
        
    else:
        next_move = graph.difference(astar_path[1], position)
        next_move = move_set[next_move]

    

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
