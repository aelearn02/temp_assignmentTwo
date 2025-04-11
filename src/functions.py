import pandas as pd
import os, csv
from celery.result import AsyncResult
from src.tasks import TaskQueue, app, run_game
from celery.result import AsyncResult


def display_top_five_results_from_csv(path):
    
    df = pd.read_csv(path)
    df = df.sort_values(["num_moves", "total_time"], ascending=[True, True]).reset_index(drop=True)
    print("\n\n*** Top 5 Best Results (Sorted by Fastest Time and Lowest Moves Required)***")
    print(df[["total_time","num_moves","backtrack_count","algorithm"]].head())
    print("***************")

def save_csv(path, data, rows):
    file_exists = os.path.isfile(path)

    with open(path, mode="a", newline="") as distributed_file:
        writer = csv.writer(distributed_file)
        
        if not file_exists:
            writer.writerow(rows)
        
        writer.writerow(data)

def dispatch_tasks(message):
    async_result = TaskQueue.delay(message) 
    return async_result.id #save id

def get_result(task_id):
    result = AsyncResult(id = task_id,app = app) #https://docs.celeryq.dev/en/stable/reference/celery.result.html
    if result.ready():
        return result.get()
    return None

#run game in parallel. Same as dispatch_tasks function
def dispatch_game(width, height, maze_type, algorithm = "right-hand"):
    print("Dispatching Game")
    async_result = run_game.delay(width, height, maze_type, algorithm) 
    return async_result.id
    
def await_result(id):
    while(True):
        result = get_result(id)
        if(result != None):
            break
    return result