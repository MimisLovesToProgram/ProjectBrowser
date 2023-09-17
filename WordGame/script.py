import random
import os

# Setting the default attempts, asking the user for the game's difficulty, and then validating it.
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

word = ""
# 'gap' is a variable that contains both gaps, and letters of the variable 'word' at their respective places. The rest is simple.
gap = ""
exist = []
used = []
guesses = 0
index = 0
# Picking the word from the dictionary, processing it, then filling the variable 'gap' with underscores, for each letter contained in 'word'
with open(f"{os.getcwd()}\\WordGame\\dictionary.txt") as d:
    word = random.choice(d.readlines())
    word = word.lower()
    word = word.strip()
    for i in range(len(word)):
        gap += "_"
print(f"I picked a random word from a dictionary. You are given {attempts} chances. Try to guess it!")

# Keep the game running until there are no more attempts left, simply by getting guesses and continously updating 'gap', and displaying many kinds of info in each iteration.
while guesses != attempts:
    guesses += 1
    # Show the round's info (the current 'gap', the number of attempts, used letters and the ones to be placed).
    print("------------------------------------------------------------")
    print(gap + f", guess the word with {len(word)} letters in " + str(attempts - guesses + 1) + " attempts")
    print(f"To be placed: {exist}")
    print(f"Used: {used}")
    # Getting a guess, and checking if its valid.
    guess = input("Type your guess: ")
    guess = guess.lower()
    while len(guess) != len(word):
        print(f"You may only type a word with {len(word)} letters")
        guess = input("Type your guess: ")
    # Checking whether the word guessed is the actual word or not.
    if guess == word:
        print("Congratulations! You found the word in " + str(guesses) + " guesses!")
        break
    else:
        for letter in guess:
            # Adding the current letter to 'used'
            if not letter in used and not letter in exist:
                used.append(letter)
            if letter in word:
                # If the current letter is in the correct position of 'word', reveal it in 'gap'.
                if guess[index] == word[index] and not letter in gap:
                    gap = gap[:word.index(word[index])] + letter + gap[word.index(word[index]) + 1:]
                    # Since the letter has now been revealed, remove it from 'exist'.
                    if letter in exist:
                        exist.remove(letter)
                else:
                    # If it does exist in 'word' but is not in the correct place, just add it to 'exist'.
                    if not letter in exist and not letter in gap:
                        exist.append(letter)
            index += 1
    # Since letters that are added to 'used' above that are also in 'word' are not needed, they can be removed.
    for letter in used:
        if letter in word:
            used.remove(letter)
            
    index = 0

# Finally, print the correct word.
print("------------------------------------------------------------")
print(f"The game has ended, the correct word is {word}!")