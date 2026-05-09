import os # importering af operating system biblioteket for at kunne håndtere filer
from Environment import TicTacToeEnv # importering af vores tic tac toe environment som vi har defineret i Environment.py
from agent import QLearningAgent # importering af vores Q-learning agent som vi har defineret i agent.py
import copy # importering af copy biblioteket for at kunne lave dybe kopier af vores agent, det er nødvendigt for at kunne træne mod en klon af sig selv
import random # importering af random biblioteket for at kunne lave tilfældige valg, det er nødvendigt for at kunne træne mod en klon af sig selv og for at kunne vælge tilfældige handlinger under træningen
import time # importering af time biblioteket for at kunne udregne, hvor lang tid der er til træningen sandynligvis er færdig
import math

save_file = "AI.pkl" # filnavn for at gemme den bedste AI efter træningen

games = 50000 # antallet af spil som ai'en skal træne på. Den bedste ai gemmes efter træningen. pr. spil er der 30% chance for at AI 2 er en klon af AI 1, 
# hvilket gerne skal forhindre en statisk træning der medføre en ai der kun vinder mod en bestemt strategi.

def should_print_eta(game):

    """
    Funktion der bestemmer i hvilke intervaller ETA skal udregnes. Den udregnes i tal, der er 10'er potenser, det vil sige: 1, 10, 100, 1000 osv.
    når 10k spil eller derover er gennemført vil hvert spil tælle med i ETA, hvis det kan divideres med 10000 uden rest. fx 10k, 20k, 30k osv.
    """

    completed_games = game + 1 

    if completed_games == 1:
        return True
    
    log_value = math.log10(completed_games)
    
    if log_value.is_integer():
        return True
    
    if completed_games >= 10000 and completed_games % 10000 == 0:
        return True
    
    return False


def train_ai(games, worker_id = None, progress_queue = None): # funktion til at træne ai
    env = TicTacToeEnv() # opretter environmentet

    if os.path.exists(save_file): # tjekker om der allerede findes en gemt AI, hvis ja så indlæses den, ellers oprettes en ny AI
        agent1 = QLearningAgent.load(save_file)
        print("Agent found")

    else:
        agent1 = QLearningAgent("AI 1")
        print("No agent found. Creating new...")

    agent2 = QLearningAgent("AI 2") # opretter en anden AI som agent1 skal træne imod, denne AI starter som en ny agent

    # stats dictionary for at holde styr på hvor mange gange hver AI vinder og hvor mange gange det ender uafgjort
    stats ={
        "AI 1 Wins": 0,
        "AI 2 Wins": 0,
        "Draws": 0
    }

    init_time = time.time() # starter en timer for at kunne udregne hvor lang tid træningen tager

    # main loop for træning.
    for game in range(games):

        if should_print_eta(game):

            completed_games = game + 1

            if progress_queue is not None:
                progress_queue.put((worker_id, completed_games, time.time()))

            elif worker_id is None:
                elapsed_time = time.time() - init_time
                avg_time_per_game = elapsed_time / completed_games
                games_left = games - completed_games
                eta_seconds = int(games_left * avg_time_per_game)

                hours = eta_seconds // 3600
                minutes = (eta_seconds % 3600) // 60
                seconds = eta_seconds % 60

                if hours > 0:
                    eta_string = f"{hours}h {minutes}m {seconds}s"
                elif minutes > 0:
                    eta_string = f"{minutes}m {seconds}s"
                else:
                    eta_string = f"{seconds}s"

                print(f"single training | Game {completed_games}/{games} | ETA: {eta_string}")



        # 30% chance for at at ai spiller mod klon af sig selv
        if random.random() < 0.3:
            agent2 = copy.deepcopy(agent1)
            agent2.name = "AI 1 clone"
        else:
            agent2 = QLearningAgent("AI 2")

        obs, info = env.reset() # nulstiller environment 
        terminated = False 
        truncated = False

        # nultiller sidte træk
        last_move = {
            1: None,
            2: None
        } 

        # loop, der kæører mens spiller er i gang
        while not terminated and not truncated:
            current_player = env.player # henter spiller fra environmentet, det er enten 1 eller 2. Start spiller er tilfældig
            agent = agent1 if current_player == 1 else agent2 # vælger den rigtige agent baseret på hvilken spiller der er i gang

            old_board = obs.copy() # laver en kopi af den nuværende observation (brættet) for at kunne bruge det til læring senere
            action = agent.choose_action(obs, training=True) # agenten vælger en handling baseret på den nuværende observation (brættet) og træningstilstanden (training=True betyder at agenten vil vælge en tilfældig handling med sandsynligheden epsilon)

            obs, reward, terminated, truncated, info = env.step(action) # opdaterer environment med handling

            agent.learn(old_board, action, reward, obs, terminated) # AI lærer baseret på gammelt bræt

            last_move[current_player] = (agent, old_board, action) # gemmer sidste træk

            if terminated: # tjekker om spiller er slut
                if "Vinder" in info: # tjekker om der er en vinder
                    winner = info["Vinder"]  # henter vinderen fra info dictionary
                    loser = 2 if winner == 1 else 1 # finder taberen baseret på vinderen

                    # opdaterer stats baseret på vinderen
                    if winner == 1: 
                        stats["AI 1 Wins"] += 1
                    else:
                        stats["AI 2 Wins"] += 1
                    
                    # vi gemmer trækket for taberen så den kan blive straffet
                    loser_move = last_move[loser]

                    # tjekker om taberen har lavet et træk
                    if loser_move is not None:
                        loser_agent, loser_board, loser_action = loser_move # henter agenten, brættet og handlingen for taberen
                        loser_agent.learn(
                            loser_board, 
                            loser_action, 
                            -2, # straffer taberen med en negativ belønning for at tabe 
                            obs, 
                            True # spillet er afsluttet
                        )
                        last_move[current_player] = (agent, old_board, action)
                elif "Uafgjort" in info: # tjekker om det er uafgjort
                    stats["Draws"] += 1

                    for player in [1, 2]:
                        move = last_move[player]

                        if move is not None:
                            agent, board, action = move
                            agent.learn(
                                board,
                                action,
                                0.01,
                                obs,
                                True
                            ) # giver begge agenter en lille positiv belønning for at spille til uafgjort i stedet for at tabe

        # efter hvert spil reduceres epsilon for begge agenter, så de gradvist bliver mindre og mindre tilfældige og mere og mere fokuserede på at vælge den handling der har den højeste Q-værdi. Vi sætter en nedre grænse på 0.05 for at sikre at de stadig har en lille chance for at vælge tilfældige handlinger, hvilket kan hjælpe med at forhindre fastlåsning i suboptimale strategier.
        agent1.epsilon = max(0.05, agent1.epsilon * 0.99) 
        agent2.epsilon = max(0.05, agent2.epsilon * 0.99)

    #gemmer den bedste AI
    if stats["AI 1 Wins"] > stats["AI 2 Wins"]:
        agent1.save(save_file)
        print("AI 1 is the champion and has been saved.")
    elif stats["AI 2 Wins"] > stats["AI 1 Wins"]:
        agent2.save(save_file)
        print("AI 2 is the champion and has been saved.")

    print("Training completed!")
    print(stats)
    print("AI saved to", save_file)

def play_against_ai(): # funktion til at spille mod den trænede AI
    env = TicTacToeEnv() # opretter environmentet

    if not os.path.exists(save_file):
        print("No trained AI found. Please train the AI first.")
        return
    ai = QLearningAgent.load(save_file) # indlæser den trænede AI fra filen
    ai.epsilon = 0 # sætter epsilon til 0 for at sikre at AI'en altid vælger den handling med den højeste Q-værdi, hvilket gør den mere udfordrende at spille mod
    print("Loaded AI for playing against.")

    obs, info = env.reset()
    terminated = False
    truncated = False

    if env.player == 1: # env.player er det spillernummer ai'en har.
        print("You are O, AI is X")
    else:
        print("You are X, AI is O")
    
    print("Enter move as single index (0-8) corresponding to the board positions:")
    print("0 1 2")
    print("3 4 5")
    print("6 7 8")

    last_ai_move = None

    while not terminated and not truncated:
        env.render()

        if env.player == 1: # hvis det er AI'ens tur (spiller 1), så vælger AI'en en handling og opdaterer environmentet, ellers venter den på brugerens input
            old_board = obs.copy() # laver en kopi af den nuværende observation (brættet) for at kunne bruge det til læring senere
            action = ai.choose_action(obs, training=False) # AI'en vælger en handling baseret på den nuværende observation (brættet) og træningstilstanden (training=False betyder at AI'en ikke vil vælge tilf

            obs, reward, terminated, truncated, info = env.step(action) # opdaterer environment med AI'ens handling
            last_ai_move = (old_board, action) # gemmer AI'ens sidste træk for at kunne bruge det til læring senere, hvis det er nødvendigt

            print(f"AI chose: {action}") 
        else: # hvis det er brugerens tur, så venter den på input og opdaterer environmentet baseret på det
            valid_move = False # flag for at sikre at brugeren indtaster en gyldig handling

            while not valid_move: # loop der fortsætter indtil brugeren indtaster en gyldig handling
                try:
                    action = int(input("Your move 0-8: "))

                    if action in env.available_actions(): # tjekker om den indtastede handling er gyldig ved at sammenligne den med de tilgængelige handlinger i environmentet 
                        valid_move = True 
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a valid integer between 0 and 8.")
                
            obs, reward, terminated, truncated, info = env.step(action)
        
        if terminated: # tjekker om spillet er slut
            env.render() # viser det endelige bræt

            if "Vinder" in info: # tjekker om der er en vinder
                winner = info["Vinder"] # henter vinderen fra info dictionary
                if winner == 1:
                    print("AI wins!")

                    if last_ai_move is not None: # vi tjekker om ai'en har spillet i sidste træk. Den belønnes hvis den har vundet og straffes hvis den har tabt
                        old_board, action = last_ai_move
                        ai.learn(
                            old_board, 
                            action, 
                            1.2, # belønner AI'en med en positiv belønning for at vinde
                            obs, 
                            True
                        )
                        
                else:
                    print("You win!")

                    if last_ai_move is not None:
                        old_board, action = last_ai_move
                        ai.learn(
                            old_board, 
                            action, 
                            -2, # straffer AI'en med en negativ belønning for at tabe
                            obs, 
                            True
                        )
            elif ("Uafgjort" in info):
                print("Draw!")

                if last_ai_move is not None:
                    old_board, action = last_ai_move
                    ai.learn(old_board, action, 0.01, obs, True) # giver AI'en en lille positiv belønning for at spille til uafgjort i stedet for at tabe
    ai.save(save_file) # gemmer AI'en efter spillet, så den kan blive bedre over tid ved at lære af sine erfaringer mod menneskelige spillere
    print("AI updated and saved after playing against you.")

# giver brugeren mulighed for at vælge om de vil træne AI'en eller spille mod den, og kalder den relevante funktion baseret på deres valg

if __name__ == "__main__":
    choice = input("Do you want to train the AI or play against it? (train/play): ").strip().lower()
    if choice == "train":
        train_ai(games)
    elif choice == "play":
        play_against_ai()
    else: # håndterer ugyldige input ved at informere brugeren om at de skal indtaste 'train' eller 'play'
        print("Invalid choice. Please enter 'train' or 'play'.")