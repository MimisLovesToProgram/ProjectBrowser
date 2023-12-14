import sys
import re
import cProfile
from functools import lru_cache

# Since the user may select a high depth (not recommended though), we shall set the recursion limit to a very long integer.
sys.setrecursionlimit(2147483647)

# A class representing one of the 9 TicTacToes on the UTTT board.
class TicTacToe:
    # Self-explanatory variables, with dominance being the number of Xs and Os played on the TicTacToe.
    local_position = {1: " ", 2: " ", 3: " ",
                      4: " ", 5: " ", 6: " ",
                      7: " ", 8: " ", 9: " "}
    finished = False
    winner = ""
    dominance = {"X": 0, "O": 0}

    def __init__(self, local_position, finished, winner, dominance):
        self.local_position = local_position
        self.finished = finished
        self.winner = winner
        self.dominance = dominance

# The game's position, consisted of 9 TicTacToe objects, with the basic / starting arguments.
position = [TicTacToe({1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}, False, "", {"X": 0, "O": 0}),
            TicTacToe({1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}, False, "", {"X": 0, "O": 0}),
            TicTacToe({1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}, False, "", {"X": 0, "O": 0}),
            TicTacToe({1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}, False, "", {"X": 0, "O": 0}),
            TicTacToe({1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}, False, "", {"X": 0, "O": 0}),
            TicTacToe({1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}, False, "", {"X": 0, "O": 0}),
            TicTacToe({1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}, False, "", {"X": 0, "O": 0}),
            TicTacToe({1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}, False, "", {"X": 0, "O": 0}),
            TicTacToe({1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}, False, "", {"X": 0, "O": 0})]

# A function to find all legal moves for a TicTacToe board (provided by the Our_TicTacToe parameter), and the game's position (in case the former's TicTacToe is finished).
def find_legal_moves(Our_TicTacToe:int, position:list) -> list:
    if not Our_TicTacToe == 0 and not position[Our_TicTacToe - 1].finished:
        # If the given TicTacToe (given from Our_TicTacToe and 'position') is not finished, -= 1 Our_TicTacToe so that it matches 'position's indexes, and return a list of moves if the move's target square is empty.
        Our_TicTacToe -= 1
        TicTacToeToPlay = position[Our_TicTacToe]
        return [(Our_TicTacToe, square) for square in TicTacToeToPlay.local_position if TicTacToeToPlay.local_position[square] == " "]
    else:
        # If the given TicTacToe is finished, return a list 'legal_moves', containing all moves whose target square is empty, for each TicTacToe on the board.
        legal_moves = []
        for ind, Tic_Tac_Toe in enumerate(position):
            if not position[ind].finished:
                legal_moves.extend([(ind, square) for square in Tic_Tac_Toe.local_position if Tic_Tac_Toe.local_position[square] == " "])
        return legal_moves

# Tuples of Tic Tac Toe square indexes, representing all finished Tic Tac Toe's patterns.
finish_combinations = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]

# A funtion to check whether the game is over or not, given the board's position.
def game_finished(position:list) -> bool:
    # Returning True if one of the finish combinations is present on the board, otherwise returning False. (using the - 1s to match 'position's indexes)
    for combination in finish_combinations:
        if position[combination[0] - 1].winner == "O" and position[combination[1] - 1].winner == "O" and position[combination[2] - 1].winner == "O":
            return True
        if position[combination[0] - 1].winner == "X" and position[combination[1] - 1].winner == "X" and position[combination[2] - 1].winner == "X":
            return True
    return False

# A function to check if a TicTacToe is finished, given its local_position attribute.
def TTT_finished(local_position:dict) -> bool:
    # Like the game_finished function above, but without the - 1s, since local_position's keys range from 1 to 9.
    for combination in finish_combinations:
        if (local_position[combination[0]] == "O" and local_position[combination[1]] == "O" and local_position[combination[2]] == "O") or (local_position[combination[0]] == "X" and local_position[combination[1]] == "X" and local_position[combination[2]] == "X"):
            return True
    return False

# A function to check whether a TicTacToe can be taken by one player, given the TicTacToe's local_position attribute, and also returning the square a player can play in to take it.
def Threatens_takes(local_position:dict) -> list:
    for combination in finish_combinations:
        if (local_position[combination[0]] == "O" and local_position[combination[1]] == "O"):
            return [True, combination[2]]
        if (local_position[combination[1]] == "O" and local_position[combination[2]] == "O"):
            return [True, combination[0]]
        if (local_position[combination[0]] == "O" and local_position[combination[2]] == "O"):
            return [True, combination[1]]
        if (local_position[combination[0]] == "X" and local_position[combination[1]] == "X"):
            return [True, combination[2]]
        if (local_position[combination[1]] == "X" and local_position[combination[2]] == "X"):
            return [True, combination[0]]
        if (local_position[combination[0]] == "X" and local_position[combination[2]] == "X"):
            return [True, combination[1]]
    return [False]

# A function to combine a move with a position, returning a new list representing the new position.
def combine_move_and_position(player:str, move:tuple, position:list) -> list:
    if move != ():
        new_pos = [TicTacToe(dict(ttt.local_position), ttt.finished, ttt.winner, dict(ttt.dominance)) for ttt in position]
        if player == "X":
            new_pos[move[0]].local_position[move[1]] = "X"
            new_pos[move[0]].dominance["X"] = new_pos[move[0]].dominance.get("X", 0) + 1
        else:
            new_pos[move[0]].local_position[move[1]] = "O"
            new_pos[move[0]].dominance["O"] = new_pos[move[0]].dominance.get("O", 0) + 1

        if TTT_finished(new_pos[move[0]].local_position):
            new_pos[move[0]].finished = True
            new_pos[move[0]].winner = player

        return new_pos
    return position

# A dictionary consisted of moves and their advantages for one turn, then cleared.
global_move_advantage = {}

# The function to pick a move for the computer to play, caching its results, and returning a move chosen after thorough checks.
@lru_cache(None)
def find_move(starting_player:str, player:str, last_move:tuple, starting_move:tuple, position:tuple, local_depth:int) -> tuple:
    legal_moves = []
    not_player = "O" if player == "X" else "X"

    # Getting all legal moves to loop through afterwards.
    combined_move = combine_move_and_position(player, last_move, position)
    if last_move == () or position[last_move[1] - 1].finished:
        legal_moves = find_legal_moves(0, combined_move)
    else:
        legal_moves = find_legal_moves(last_move[1], combined_move)

    # If there are no moves, return an empty tuple, thus ending the game (If this is the first call).
    if legal_moves == []:
        return ()

    # Treating the legal moves differently if they are the starting moves, and if they are moves being calculated to change the starting moves' advantages.
    if depth == local_depth:
        for move in legal_moves:
            if move[1] == 5:
                global_move_advantage[move] = -2000

            combined_move = combine_move_and_position(player, move, position)
            taking_threat = Threatens_takes(position[move[0]].local_position)

            # Checking all the important stuff for move picking, changing the move's advantage accordingly, and searching the game tree.
            if TTT_finished(combined_move[move[0]].local_position):
                global_move_advantage[move] = global_move_advantage.get(move, 0) + 250000
            if position[move[1] - 1].finished:
                global_move_advantage[move] = global_move_advantage.get(move, 0) - 250000
            if taking_threat[0]:
                global_move_advantage[move] = global_move_advantage.get(move, 0) + 1000
                if position[taking_threat[1] - 1].dominance[player] <= position[taking_threat[1] - 1].dominance[not_player]:
                    global_move_advantage[move] = global_move_advantage.get(move, 0) - 1500
            if position[move[1] - 1].dominance[player] <= position[move[1] - 1].dominance[not_player]:
                global_move_advantage[move] = global_move_advantage.get(move, 0) - 1000

            if player == starting_player and game_finished(combined_move):
                return move
            else:
                if local_depth - 1 != 0:
                    find_move(starting_player, not_player, move, move, tuple(combined_move), local_depth - 1)
    else:
        for move in legal_moves:
            if move[1] == 5:
                if starting_player == player:
                    global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) - 5
                else:
                    global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) + 5

            combined_move = combine_move_and_position(player, move, position)
            taking_threat = Threatens_takes(position[move[0]].local_position)

            # Evaluate the move differently if the player is the starting one or not. Similarly to the code above, change the !starting! move's advantage according to the move being checked.
            if player == starting_player:
                if TTT_finished(combined_move[move[0]].local_position):
                    global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) + 250 * moves_played
                if position[move[1] - 1].finished:
                    global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) - 300
                if taking_threat[0]:
                    global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) + 20
                    if position[taking_threat[1] - 1].dominance[player] <= position[taking_threat[1] - 1].dominance[not_player]:
                        global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) - 35
                if position[move[1] - 1].dominance[starting_player] <= position[move[1] - 1].dominance[not_player]:
                    global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) - 500
            else:
                if TTT_finished(combined_move[move[0]].local_position):
                    global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) - 250 * moves_played
                if position[move[1] - 1].finished:
                    global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) + 300
                if taking_threat[0]:
                    global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) - 20
                    if position[taking_threat[1] - 1].dominance[player] <= position[taking_threat[1] - 1].dominance[not_player]:
                        global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) + 35
                if position[move[1] - 1].dominance[starting_player] <= position[move[1] - 1].dominance[not_player]:
                    global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) + 500

            # ..Then checking whether the game is finished or not like above, and searching the game tree deeper
            if player != starting_player and game_finished(combined_move):
                global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) - 85000
            elif player == starting_player and game_finished(combined_move):
                global_move_advantage[starting_move] = global_move_advantage.get(starting_move, 0) + 4000
            else:
                if local_depth - 1 != 0:
                    find_move(starting_player, not_player, move, starting_move, tuple(combined_move), local_depth - 1)

    if not global_move_advantage:
        return legal_moves[0]
    max_advantage = max(global_move_advantage.values(), default=0)
    return {value: key for key, value in global_move_advantage.items()}[max_advantage]

# A function to print the board's position
def print_board(position:list) -> None:
    print()
    for row in range(1, 4):
        # Getting the Tic Tac Toes we will be working on with this "formula".
        current_TTTs = position[row * 3 - 3 : row * 3]
        TicTacToe1, TicTacToe2, TicTacToe3 = current_TTTs
        for col in range(1, 4):
            # Getting the squares of each Tic Tac Toe in our row.
            items_to_print1 = list(TicTacToe1.local_position.values())[col * 3 - 3 : col * 3]
            items_to_print2 = list(TicTacToe2.local_position.values())[col * 3 - 3 : col * 3]
            items_to_print3 = list(TicTacToe3.local_position.values())[col * 3 - 3 : col * 3]

            # Printing the items in this format.
            print(f"[ {' | '.join(items_to_print1)} ] [ {' | '.join(items_to_print2)} ] [ {' | '.join(items_to_print3)} ]")
        print()

global_move_advantage = {}
last_move = (0, 0)
depth = input("Enter the number of future moves the computer should calculate: ")
while not depth.isnumeric():
    depth = input("Please enter the number of future moves the computer should calculate: ")
depth = int(depth)

# Starting value of 1 due to the multiplications to be done in find_move().
moves_played = 1

user_player = input("Pick 'X' or 'O' for you to play with: ")
while not user_player in ["X", "O"]:
    user_player = input("Please pick 'X' or 'O' for you to play with: ")

computer_player = "X" if user_player == "O" else "O"
print("So, Let's start the game!")

# The main game loop.
while not game_finished(position):
    if user_player == "X":
        print_board(position)

        # Ending the game if there are no legal moves.
        if find_legal_moves(last_move[1], position) == []:
            break

        # Getting the user's move.
        raw_move = input("Enter the Tic Tac Toe's index, and one of its squares' indexes, separated by a space: ")
        move = raw_move.split()
        while move == [] or not re.match(r"^[0-9] [0-9]$", raw_move) or not (int(move[0]) - 1, int(move[1])) in find_legal_moves(last_move[1], position):
            raw_move = input("Please enter a valid move: ")
            move = raw_move.split()

        # Converting the user's move into a move we can correctly process, and updating the position.
        move = (int(move[0]) - 1, int(move[1]))
        position[move[0]].local_position[move[1]] = user_player

        # If the move played by the user finished a Tic Tac Toe, update it's stats.
        if TTT_finished(position[move[0]].local_position):
            position[move[0]].finished = True
            position[move[0]].winner = user_player

        # Get the computer's move.
        pc_move = find_move(computer_player, computer_player, move, (), tuple([TicTacToe(dict(ttt.local_position), ttt.finished, ttt.winner, dict(ttt.dominance)) for ttt in position]), depth)
        if pc_move == ():
            break

        print(global_move_advantage)
        # Resetting the dict and updating the necessary stuff (position, last_move)
        global_move_advantage = {}
        position[pc_move[0]].local_position[pc_move[1]] = computer_player
        last_move = pc_move
        print(f"Last move played: ({last_move[0] + 1}, {last_move[1]})", end="")

        # Again, checking if the computer's move finished a Tic Tac Toe, and changing its stats.
        if TTT_finished(position[pc_move[0]].local_position):
            position[pc_move[0]].finished = True
            position[pc_move[0]].winner = computer_player

    else:
        # Same things as above, but the computer plays first (the condition below is just a fixed move for the start).
        if last_move == (0, 0):
            pc_move = (4, 3)
        else:
            pc_move = find_move(computer_player, computer_player, last_move, (), tuple([TicTacToe(dict(ttt.local_position), ttt.finished, ttt.winner, dict(ttt.dominance)) for ttt in position]), depth)

        # find_move() returns () when the computer has no legal moves, thus ending the game here.
        if pc_move == ():
            break

        print(global_move_advantage)
        global_move_advantage = {}
        position[pc_move[0]].local_position[pc_move[1]] = computer_player

        print(f"Last move played: ({pc_move[0] + 1}, {pc_move[1]})")
        print_board(position)

        if TTT_finished(position[pc_move[0]].local_position):
            position[pc_move[0]].finished = True
            position[pc_move[0]].winner = computer_player

        if find_legal_moves(pc_move[1], position) == []:
            break

        raw_move = input("Enter the Tic Tac Toe's index, and one of its squares' indexes, separated by a space: ")
        move = raw_move.split()
        while move == [] or not re.match(r"^[0-9] [0-9]$", raw_move) or not (int(move[0]) - 1, int(move[1])) in find_legal_moves(pc_move[1], position):
            raw_move = input("Please enter a valid move: ")
            move = raw_move.split()
        move = (int(move[0]) - 1, int(move[1]))
        last_move = move
        position[move[0]].local_position[move[1]] = user_player

        if TTT_finished(position[move[0]].local_position):
            position[move[0]].finished = True
            position[move[0]].winner = user_player
    moves_played += .1

print("\rGame Over!                                 ")