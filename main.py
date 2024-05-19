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
import replit

from graph import Graph
from astar import AStar
from DFS import DFS

SNAKE_NAMES = ["Chimuelo Dev", "Chimuelo"]

save_data = replit.db

def save_info_start(data):
    game_id = data.get("game", {}).get("id", None)
    snake_names = ' | '.join(sorted([snake['name'] for snake in data['board']['snakes']]))
    games = save_data.get('games', {})
    snake_names_games = games.get(snake_names, {})
    translate = save_data.get('translate', {})
    translate[game_id] = snake_names
    snake_names_games[game_id] = {'count': len(snake_names_games)}
    games[snake_names] = snake_names_games
    save_data['games'] = games
    save_data['translate'] = translate

def deep_copy_observable_dict(src):
    if not hasattr(src, "items"):
        return src

    copy = {}
    for key, value in src.items():
        if hasattr(src, "items"):
            copy[key] = deep_copy_observable_dict(value)
        else:
            copy[key] = value
    return copy

def save_info_end(data):
    result = ' | '.join(sorted([snake['name'] for snake in data['board']['snakes']]))
    game_id = data.get("game", {}).get("id", None)
    translate = save_data.get('translate', {})
    snake_names = translate[game_id]

    games = save_data.get('games', {})
    snake_names_games = games.get(snake_names, {})
    game = snake_names_games.get(game_id, {})
    game['result'] = result
    games[snake_names] = snake_names_games
    save_data['games'] = games
    with open('data.json', 'w') as f:
        json.dump(deep_copy_observable_dict(dict(save_data)), f, indent=4)

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
    game = Graph()
    game.reset((game_state['board']['width'], game_state['board']['height']))
    print("GAME START")
    save_info_start(game_state)
    snake_names = [snake['name'] for snake in game_state['board']['snakes']]
    print('SNAKES: %s' % ', '.join(snake_names))
    

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    graph = Graph((game_state['board']['width'], game_state['board']['height']))
    if game_state['you']['id'] in graph.target_cells.keys():
        del graph.target_cells[game_state['you']['id']]
    print("GAME OVER\n")
    save_info_end(game_state)
    snake_names = [snake['name'] for snake in game_state['board']['snakes']]
    print('SNAKES REMAINING: %s' % ', '.join(snake_names))

def move(game_state: typing.Dict) -> typing.Dict:
    graph = Graph((game_state['board']['width'], game_state['board']['height']))
    astar = AStar(graph)
    dfs = DFS(graph)
    my_id = game_state['you']['id']
    my_name = game_state['you']['name']
    my_length = game_state['you']['length']

    if my_name not in SNAKE_NAMES:
        return {"move": 'up'}

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
    enemy_ways = []
    for snake in game_state['board']['snakes']:
        for num, cell in enumerate(snake['body']):
            occupied_cells[graph.convert_to_tuple(cell)] = snake['length'] - num + 1

        if snake['id'] != my_id and snake['length'] >= my_length and my_name != snake['name']:
            for future_pos in graph.get_neighbors(graph.convert_to_tuple(snake['head'])):
                if future_pos not in occupied_cells.keys():
                    occupied_cells[future_pos] = snake['length'] + 1
                    enemy_ways.append(future_pos)

        elif snake['id'] != my_id and my_name == snake['name']:
            for future_pos in graph.get_neighbors(graph.convert_to_tuple(snake['head'])):
                if future_pos not in occupied_cells.keys():
                    occupied_cells[future_pos] = snake['length'] + 1
                    friend_ways.append(future_pos)

    food_cells = set()
    for food in game_state['board']['food']:
        food_cells.add(graph.convert_to_tuple(food))

    position = graph.convert_to_tuple(game_state['you']['head'])

    start_info = graph.get_neighbor_info(position, occupied_cells, game_state['you']['length'])
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
        path = dfs.choose_paths_to_scape(position, block_closed_sides, max_depth=15)
    elif len(blocked_future) != len(start_info.keys()):
        for side in closed_sides:
            occupied_cells[side] = 10 # Think about this if some change on a*
            if side in food_cells:
                food_cells.remove(side)

        food_cells &= safe_cells

        for k, v in graph.target_cells.items():
            if k != my_id and v is not None and v in food_cells:
                food_cells.remove(v)

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
                next_move = graph.difference(future, position)
    if path is None and next_move is None:
        print('RANDOM MOVE')
        safe_moves = set(start_info.keys()) - blocked_future
        if len(safe_moves) == 0:
            all_moves = set([graph.difference(k, position) for k in start_info.keys()])
            all_one_moves = [graph.difference(k, position) for k, v in occupied_cells.items() if v == 2]
            possible_one_moves = all_moves & set(all_one_moves)
            print(all_one_moves)
            print(possible_one_moves)
            possible_moves = all_moves & set([graph.difference(v, position) for v in enemy_ways])
            print(enemy_ways)
            print(possible_moves)
            if len(possible_one_moves) > 0:
                all_moves = possible_one_moves
            if len(possible_moves) > 0:
                all_moves = possible_moves
            elif my_length > 1:
                neck = graph.convert_to_tuple(game_state['you']['body'][1])
                all_moves = all_moves - set([graph.difference(neck, position)])
            order = {graph.difference(k, position): v['n_cells'] for k, v in start_info.items()}
            next_move = max(list(all_moves), key=lambda x: order[x])
        else:
            rand_move = random.choice(list(safe_moves))
            next_move = graph.difference(rand_move, position)

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
