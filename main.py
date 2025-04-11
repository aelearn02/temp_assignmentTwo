from src.functions import save_csv, dispatch_tasks, get_result, dispatch_game, await_result,display_top_five_results_from_csv
from mpi4py import MPI
import datetime, os

# algorithms
# "right-hand"
# "astar"
# "dijkstra"
def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    hostname = MPI.Get_processor_name()

    if(rank != 0):
        game_id = dispatch_game(
            width = 50,
            height = 50,
            maze_type = "static",
            algorithm = "dfs"
        )

        comm.send(game_id, dest = 0)

    else:
        results = []
        results_dir = "./results"
        os.makedirs(results_dir, exist_ok=True)
        save_results_to_file_path = os.path.join(results_dir, "maze_runner.csv")

        # For all machines, get the id and result
        for i in range(size - 1):
            
            game_id = comm.recv(source=MPI.ANY_SOURCE)
            game_result = await_result(game_id)
            print("Current Game Result is: ", game_result)
            results.append(game_result)


        # Save Results to a csv file
        rows = [
            "total_time",
            "num_moves",
            "backtrack_count",
            "width",
            "height",
            "type",
            "algorithm",
            "date"
        ]
        for time_taken, num_moves, backtrack_count, algorithm in results:
            data = [
                f"{time_taken:4f}",
                num_moves,
                backtrack_count,
                50,
                50,
                "static",
                algorithm,
                datetime.datetime.now()
            ]
            save_csv(save_results_to_file_path, data, rows)

        # Display best result so far from all instances of running the program onto the console, not necessarily from this run.
        display_top_five_results_from_csv("./results/maze_runner.csv")


    
if __name__ == "__main__":
    main()

        
    