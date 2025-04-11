from celery import Celery
# Game Related Imports
from src.maze import create_maze
from src.explorer import Explorer

broker = "pyamqp://guest@localhost//"
backend = "redis://localhost:6379/0"

app = Celery("tasks", broker = broker, backend = backend)


@app.task
def TaskQueue(message):
    print(f"Processing: {message}")
    return f"Processed: {message}"  # Result stored in Redis

@app.task
def run_game(width, height, maze_type, algorithm):
    print(f"Running Game...")
    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, algorithm)
    time_taken, moves, backtrack_count, algorithm = explorer.solve()
    return time_taken, len(moves), backtrack_count, algorithm
