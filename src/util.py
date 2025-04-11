from src.maze import create_maze
from src.explorer import Explorer

def run_explorer(width, height, game_type, visualize = False):

    maze = create_maze(width, height, game_type)
    explorer = Explorer(maze, visualize=visualize)
    time_taken, moves = explorer.solve()
    results = {
        "width": width,
        "height": height,
        "maze_type": game_type,
        "time_taken": time_taken,
        "moves": len(moves)
    }
    return results