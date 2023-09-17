import time
import os
import random
import re

rec_e = 0
rec_n = 0
rec_h = 0
with open(f"{os.getcwd()}\\WordRace\\record.txt") as f:
    for line in f.readlines():
        if not f.readlines() == []:
            search = re.search(r"([0-9]+)", line)
            number = int(search.group(1))
            if "Easy" in line:
                rec_e = number
            elif "Normal" in line:
                rec_n = number
            elif "Hard" in line:
                rec_h = number
        else:
            rec_e = 0
            rec_n = 0
            rec_h = 0
            break

limit = 0
difficulty = input("Play Easy difficulty, Normal, or Hard? (Type one of these) ").lower()

while not difficulty in ["easy", "normal", "hard"]:
    difficulty = input("Type one of the difficulties mentioned above: ")

if difficulty == "easy":
    limit = 60
elif difficulty == "normal":
    limit = 40
else:
    limit = 20

words = []
with open(f"{os.getcwd()}\\WordRace\\dictionary.txt") as f:
    for word in f.readlines():
        words.append(word.rstrip())

print("Are you ready to start the game? The first letter will apear once you are. ")
input("Type anything here once you are ready to start! ")
letter = random.choice('qwertyuiopasdfghjklzxcvbnm')
print(f"----------------------------------------------------------------------------\nThe game has now started! Your letter is '{letter}'")

found = 0

start = time.time()
while time.time() - start < limit:
    word = input(f"Type a word starting with '{letter}': ")
    if word.startswith(letter) and word in words and time.time() - start < limit:
        found += 1
        print("That word is correct!\n----------------------------------------------------------------------------")
    elif time.time() - start > limit:
        print("You ran out of time while writing!\n----------------------------------------------------------------------------")
    else:
        print("This word is not correct.\n----------------------------------------------------------------------------")

print(f"========================================\nTime's up! You found {found} words!")

with open(f"{os.getcwd()}\\WordRace\\record.txt", "w") as f:
    if found > rec_e and difficulty == "easy":
        rec_e = found
    elif found > rec_n and difficulty == "normal":
        rec_n = found
    elif found > rec_h and difficulty == "hard":
        rec_h = found
    f.write(f"Easy: {rec_e}\n")
    f.write(f"Normal: {rec_n}\n")
    f.write(f"Hard: {rec_h}")