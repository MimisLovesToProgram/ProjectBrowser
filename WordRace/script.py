import time
import os
import random
import re

# Getting the player's records from record.txt
rec_e = 0
rec_n = 0
rec_h = 0
with open(f"{os.getcwd()}\\WordRace\\result.txt") as f:
    for line in f.readlines():
        # If the user wants to reset the high scores, and they empty the result file, we need this if-else.
        if not f.readlines() == []:
            # Using regex to get the record for each difficulty if the result file has not been emptied.
            search = re.search(r"([0-9]+)", line)
            number = int(search.group(1))
            if "Easy" in line:
                rec_e = number
            elif "Normal" in line:
                rec_n = number
            elif "Hard" in line:
                rec_h = number
        else:
            # Resetting the high scores if the user has emptied the result file.
            rec_e = 0
            rec_n = 0
            rec_h = 0
            break

limit = 0
difficulty = input("Play Easy difficulty, Normal, or Hard? (Type one of these) ").lower()

# Checking if the difficulty given above is valid or not.
while not difficulty in ["easy", "normal", "hard"]:
    difficulty = input("Type one of the difficulties mentioned above: ")

# Setting a time limit for the difficulty given.
if difficulty == "easy":
    limit = 60
elif difficulty == "normal":
    limit = 40
else:
    limit = 20

# Getting the words from dictionary.txt and putting the on a list, after having been stripped.
words = []
with open(f"{os.getcwd()}\\WordRace\\dictionary.txt") as f:
    for word in f.readlines():
        words.append(word.rstrip())

# Preparing to start the game, and picking the starting letter of the words to be given.
print("Are you ready to start the game? The first letter will apear once you are. ")
input("Type anything here once you are ready to start! ")
letter = random.choice('qwertyuiopasdfghjklzxcvbnm')
print(f"----------------------------------------------------------------------------\nThe game has now started! Your letter is '{letter}'")

found = 0

# Setting a simple timer.
start = time.time()
while time.time() - start < limit:
    # Getting a word from the user, and checking if it is valid and written within the time limit.
    word = input(f"Type a word starting with '{letter}': ")
    if word.startswith(letter) and word in words and time.time() - start < limit:
        found += 1
        print("That word is correct!\n----------------------------------------------------------------------------")
    # Don't count the word if the user finished writing after the time was out.
    elif time.time() - start > limit:
        print("You ran out of time while writing!\n----------------------------------------------------------------------------")
    else:
        print("This word is not correct.\n----------------------------------------------------------------------------")

print(f"========================================\nTime's up! You found {found} words!")

# Checking whether the user has made a new high score, and if yes, modifying the respective high score variable.
with open(f"{os.getcwd()}\\WordRace\\result.txt", "w") as f:
    if found > rec_e and difficulty == "easy":
        rec_e = found
    elif found > rec_n and difficulty == "normal":
        rec_n = found
    elif found > rec_h and difficulty == "hard":
        rec_h = found
    # Finally, write the records to the result file.
    f.write(f"Easy: {rec_e}\n")
    f.write(f"Normal: {rec_n}\n")
    f.write(f"Hard: {rec_h}")