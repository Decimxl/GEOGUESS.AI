from multiprocessing import Pool, cpu_count, Manager
import shutil

from Environment import TicTacToeEnv
from agent import QLearningAgent
import main_training as main

import time

Final_save_file = "AI.pkl" # filnavn for at gemme den bedste AI efter træningen

games_per_worker = 1000000 # antal spil hver tråd skal træne på
Tournament_games = 5000 # antal spil i turneringen for at finde den bedste AI blandt trådene
Workers = max(1, cpu_count() - 2) # vi bruger alle cpu kerner minus 2, så computeren stadig kan bruges til andre ting under træningen

def train_agent(args):

    worker_id, progress_queue = args

    worker_save_file = f"worker_{worker_id}.pkl" # filnavn for at gemme AI'en trænet i denne tråd

    main.save_file = worker_save_file
    main.train_ai(games_per_worker, worker_id, progress_queue=progress_queue)

    return worker_save_file

def test_ai_vs_ai(file_1, file_2, games=Tournament_games):
    env = TicTacToeEnv()

    ai1 = QLearningAgent.load(file_1)
    ai2 = QLearningAgent.load(file_2)

    ai1.epsilon = 0 # ingen exploration under turneringen
    ai2.epsilon = 0 # ingen exploration under turneringen

    score1 = 0
    score2 = 0
    draws = 0

    for i in range(games):
        obs, info = env.reset()
        terminated = False
        truncated = False

        while not terminated and not truncated:
            current_player = env.player

            agent = ai1 if current_player == 1 else ai2
            action = agent.choose_action(obs, training=False)
            obs, reward, terminated, truncated, info = env.step(action)
        if "Vinder" in info:
            if info["Vinder"] == 1:
                score1 += 1
            elif info["Vinder"] == 2:
                score2 += 1
        elif "Uafgjort" in info:
            draws += 1
    return score1, score2, draws

def choose_best_ai(files):
    best_file = files[0]
    best_score = -100000000000000
    for file in files:
        total_score = 0

        for opponent_file in files:
            if file == opponent_file:
                continue
            wins, losses, draws = test_ai_vs_ai(
                file, 
                opponent_file,
                Tournament_games
                )
            
            total_score += wins
            total_score -= losses
            total_score += draws * 0.1

        print(f"{file} score: {total_score}")

        if total_score > best_score:
            best_score = total_score
            best_file = file
    return best_file

if __name__ == "__main__":
    print("CPU count:", cpu_count())
    print("Workers:", Workers)

    print(f"Starting training with {Workers} workers, each training on {games_per_worker} games...")

    manager = Manager()
    progress_queue = manager.Queue()
    init_time = time.time()

    with Pool(Workers) as pool:
        async_result = pool.map_async(
            train_agent,
            [(worker_id, progress_queue) for worker_id in range(Workers)]
        )
        worker_progress = {
            worker_id: 0
            for worker_id in range(Workers)
        }
        while not async_result.ready():
            while not progress_queue.empty():
                worker_id, completed_games, report_time = progress_queue.get()

                worker_progress[worker_id] = completed_games

                total_completed_games = sum(worker_progress.values())
                total_games = games_per_worker * Workers

                elapsed = time.time() - init_time

                if total_completed_games >0:
                    games_per_second = total_completed_games / elapsed
                    games_left = total_games - total_completed_games
                    eta_seconds = int(games_left / games_per_second)

                    hours = eta_seconds // 3600
                    minutes = (eta_seconds % 3600) //60
                    seconds = eta_seconds % 60

                    if hours > 0:
                        eta_string = f"{hours}h {minutes}m {seconds}s"
                    elif minutes > 0:
                        eta_string = f"{minutes}m {seconds}s"
                    else:
                        eta_string = f"{seconds}s"

                    print(
                        f"Total progress: {total_completed_games}/{total_games} | ETA: {eta_string}",
                        end="\r"
                    )
            time.sleep(0.1)
        files = async_result.get()
                                        
    print()
    print("all workers finished training, starting tournament to find best AI...")
    best_file = choose_best_ai(files)

    shutil.copy(best_file, Final_save_file)

    print(f"Best AI found at {best_file}")
    print(f"saved at {Final_save_file}")
