import random
import os

attempts = 10
mode = input("Play: Easy mode, Normal mode, or Hard mode? ").lower()

while not mode in ["easy", "normal", "hard"]:
    mode = input("Enter one of the difficulty levels above: ").lower()
if mode == "easy":
    attempts = 15
elif mode == "normal":
    attempts = 10
else:
    attempts = 5

num = random.randrange(1, 4427)
word = ""
gap = ""
exist = []
used = []
guesses = 0
index = 0
with open(f"{os.getcwd()}\\WordGame\\dictionary.txt") as d:
    word = d.readlines()[num]
    word = word.lower()
    word = word.strip()
    for i in range(len(word)):
        gap += "_"
print(f"I picked a random word from a dictionary. You are given {attempts} chances. Try to guess it!")

while guesses != attempts:
    guesses += 1
    print("------------------------------------------------------------")
    print(gap + f", guess the word with {len(word)} letters in " + str(attempts - guesses + 1) + " attempts")
    print(f"To be placed: {exist}")
    print(f"Used: {used}")
    guess = input("Type your guess: ")
    guess = guess.lower()
    while len(guess) != len(word):
        print(f"You may only type a word with {len(word)} letters")
        guess = input("Type your guess: ")
    if guess == word:
        print("Congratulations! You found the word in " + str(guesses) + " guesses!")
        break
    else:
        for letter in guess:
            if not letter in used and not letter in exist:
                used.append(letter)
            if letter in word:
                if word.count(letter) > 1:
                    if not letter in exist:
                        for i in range(word.count(letter)):
                            exist.append(letter)
                if guess[index] == word[index] and not letter in gap:
                    gap = gap[:word.index(word[index])] + letter + gap[word.index(word[index]) + 1:]
                    if letter in exist:
                        exist.remove(letter)
                else:
                    if not letter in exist and not letter in gap:
                        exist.append(letter)
            index += 1
    for letter in used:
        if letter in word:
            used.remove(letter)

    index = 0

print("------------------------------------------------------------")
print(f"The game has ended, the correct word is {word}!")