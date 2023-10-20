import random
import time
import os

# Player 1's (computer) and Player 2's chosen number respectively.
num1 = 0
num2 = 0

# The current range of numbers player 2 can guess from. Elements in this list are going to be removed as the game progresses.
p1CurrentRange = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

attempts1 = 3
attempts2 = 3

guess = ""

condition = ""

score1 = 0
score2 = 0

round = 1

# Used to adjust Player 1's range of numbers to guess, returns the new, adjusted list of numbers Player 1 can guess.
def p1range(condition:str, range:list) -> list:
    result = []
    # If this is the first guess in the turn, just return the normal range.
    if condition == "":
        return range
    # If the number guessed is smaller than the number set by Player 2, only append numbers bigger than the current guess to result.
    if "<" in condition:
        for item in range:
            if not int(item) < int(condition[condition.index("<") + 1:]):
                result.append(item)
    # If the number guessed is bigger than the number set by player 2, only append numbers smaller than the current guess to result.
    elif ">" in condition:
        for item in range:
            if not int(item) > int(condition[condition.index(">") + 1:]):
                result.append(item)
    return result

while score1 < 5 and score2 < 5:
    num1 = str(random.randrange(1, 17))
    num2 = input("Choose a number from 1 to 16: ")

    # Checking if the number given by player 2 is within the approved boundaries.
    while not int(num2) in range(1, 17):
        num2 = input("Please choose a number from 1 to 16: ")

    print("-------------------------------------------------------------------")

    # While Player 2 still has attempts left in this round, ask them to make a guess about Player 1's number, giving them hints in case they fail to.
    while attempts2 != 0:
        attempts2 -= 1
        guess = input("Player 2: Enter your guess for Player 1's number: ")
        if guess == num1:
            print(f"You have found Player 1's number! +{attempts2 + 1} points!")
            score2 += attempts2 + 1
            break
        elif int(guess) < int(num1):
            print(f"The number {guess} is smaller than Player 1's number.")
        elif int(guess) > int(num1):
            print(f"The number {guess} is bigger than Player 1's number.")
        print("-----------------")
    if guess != num1:
        print("You did not find Player 1's number: " + num1)
    print("-------------------------------------------------------------------")

    # While Player 1 still has attempts left in this round, pick a sensible but random number for Player 2's number, giving it hints in case they fail to, and updating
    # its range of sensible numbers to pick next.
    while attempts1 != 0:
        attempts1 -= 1
        p1CurrentRange = p1range(condition, p1CurrentRange)
        guess = str(random.choice(p1CurrentRange))
        print("Player 1's guess: " + guess)
        if guess == num2:
            print(f"Player 1 has found Player 2's number! +{attempts1 + 1} points!")
            score1 += attempts1 + 1
            break
        elif int(guess) < int(num2):
            print(f"The number {guess} is smaller than Player 2's number. ({num2})")
            condition = "<" + guess
        elif int(guess) > int(num2):
            print(f"The number {guess} is bigger than Player 2's number. ({num2})")
            condition = ">" + guess
        p1CurrentRange.remove(int(guess))
        time.sleep(10)
        print("-----------------")
    if guess != num2:
        print("Player 1 did not find Player 2's number: " + num2)
    
    # Resetting most variables to start the next round.
    round += 1
    p1CurrentRange = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    condition = ""
    attempts1 = 3
    attempts2 = 3
    print("======================================")
    print("ROUND: " + str(round))
    print("Player 1's Points: " + str(score1))
    print("Player 2's Points: " + str(score2))
    print("======================================")

# After the game has ended, check who won, and write the result in the project's result file.
with open(f"{os.getcwd()}\\GuessTheNumber\\result.txt", "a") as f:
    if score1 >= 5 and score2 >= 5:
        if score1 > score2:
            print(f"Player 1 Has Won {score1}-{score2}!")
            f.write(f"Player 1 Has Won {score1}-{score2} in {round - 1} rounds!\n")
        elif score2 > score1:
            print(f"Player 2 Has Won {score2}-{score1}!")
            f.write(f"Player 2 Has Won {score2}-{score1} in {round - 1} rounds!\n")
        else:
            print(f"The game has ended in a draw {score1}-{score2}!")
            f.write(f"The game has ended in a draw {score1}-{score2} in {round - 1} rounds!\n")
    elif score1 >= 5:
        print(f"Player 1 Has Won {score1}-{score2}!")
        f.write(f"Player 1 Has Won {score1}-{score2} in {round - 1} rounds!\n")
    else:
        print(f"Player 2 Has Won {score2}-{score1}!")
        f.write(f"Player 2 Has Won {score2}-{score1} in {round - 1} rounds!\n")