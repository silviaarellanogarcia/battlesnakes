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
from DFS import DFS
from utils import choose_safe_random_move

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
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
    #print(json.dumps(game_state))
    

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    graph = Graph((game_state['board']['width'], game_state['board']['height']))
    if game_state['you']['id'] in graph.target_cells.keys():
        del graph.target_cells[game_state['you']['id']]
    print("GAME OVER\n")

def move(game_state: typing.Dict) -> typing.Dict:
    graph = Graph((game_state['board']['width'], game_state['board']['height']))
    astar = AStar(graph)
    dfs = DFS(graph)
    my_id = game_state['you']['id']
    my_name = game_state['you']['name']
    my_length = game_state['you']['length']

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

    occupied_cells = {}
    friend_ways = []
    for snake in game_state['board']['snakes']:
        for num, cell in enumerate(snake['body']):
            occupied_cells[graph.convert_to_tuple(cell)] = snake['length'] - num + 1

        if snake['id'] != my_id and snake['length'] >= my_length:
            for move in move_set.keys():
                future_pos = graph.sum(graph.convert_to_tuple(snake['head']), move)
                if future_pos not in occupied_cells.keys():
                    occupied_cells[future_pos] = snake['length'] + 1

        if snake['id'] != my_id and my_name == snake['name']:
            for move in move_set.keys():
                future_pos = graph.sum(graph.convert_to_tuple(snake['head']), move)
                if future_pos not in occupied_cells.keys():
                    occupied_cells[future_pos] = snake['length'] + 1
                    friend_ways.append(future_pos)

    food_cells = set()
    for food in game_state['board']['food']:
        food_cells.add(graph.convert_to_tuple(food))

    position = graph.convert_to_tuple(game_state['you']['head'])

    start_info = graph.get_neighbor_info(position, occupied_cells)
    closed_sides = []
    block_closed_sides = {}
    safe_cells = set()
    blocked_future = set()
    for side, info in start_info.items():
        if info['n_cells'] <= my_length + 2:
            if info['n_cells'] == 0:
                blocked_future.add(side)
            closed_sides.append(side)
            block_closed_sides.update(info['block'])
        else:
            safe_cells |= info['cells']

    path = None
    if len(closed_sides) >= len(start_info.keys()) and len(blocked_future) != len(start_info.keys()):
        print('DFS')
        path = dfs.choose_paths_to_scape(position, block_closed_sides, max_depth=15)
    elif len(blocked_future) != len(start_info.keys()):
        for side in closed_sides:
            occupied_cells[side] = 10 # Think about this if some change on a*
            food_cells = food_cells - start_info[side]['cells']

        for k, v in graph.target_cells.items():
            if k != my_id and v is not None and v in food_cells:
                food_cells.remove(v)

        for food in list(food_cells):
            if food in occupied_cells.keys():
                food_cells.remove(food)

        if len(food_cells) == 0:
            for _ in range(3):
                food_cells.add(random.choice(list(safe_cells)))

        path = astar.astar(
           position, food_cells, occupied_cells, len(game_state['you']['body']))
    
    if path is not None:
        graph.target_cells[my_id] = path[-1]
    else:
        graph.target_cells[my_id] = None
        
    #print('POS: %s' % str(position))
    #print('OCC: %s' % str(occupied_cells))
    #print('FOOD: %s' % str(food_cells))
    #print('PATH: %s' % str(astar_path))
    next_move = None
    if len(blocked_future) == len(start_info.keys()):
        for future in graph.get_neighbors(position):
            if future in friend_ways:
                next_move = move_set[graph.difference(future, position)]
    if path is None and next_move is None:
        print("RANDOM")
        next_move = choose_safe_random_move(game_state)
        
    elif next_move is None:
        next_move = graph.difference(path[1], position)
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
