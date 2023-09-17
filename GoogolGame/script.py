import random
import os

# Get an amount of numbers to be generated, then generate that many random numbers, with the highest one possible being 99,999.
numbers = int(input("How many hidden numbers should be generated? "))
hidden = [format(random.randrange(1, 10**5), ',') for i in range(numbers)]
opened = []
counter = 0

print("The game has now started! When you feel you are done, type anything other than yes.")
user_input = input("Are you ready to see your first number? ")

while user_input.lower() == "yes" and counter + 1 <= len(hidden):
    # Display the current number, how many numbers have been seen, then add the current number to 'opened', print the list, and keep things going.
    print(f"===================================================\nYour number is: {hidden[counter]}. {counter + 1}/{numbers} numbers opened.")

    opened.append(hidden[counter])
    print(f"Opened: {sorted(opened, reverse=True)}")
    counter += 1
    user_input = input("Would you like to continue? ")

# After the game has ended, print the results, and write them at the project's log.
with open(f"{os.getcwd()}\\GoogolGame\\GameLog.log", "a") as f:
    if max(hidden) == hidden[counter - 1]:
        print("------------------------------------------------\nCongrats! You have found the greatest number among the other hidden ones!")
        f.write(f"The player has won, having found the greatest number among {hidden}!\n")
    else:
        print(f"------------------------------------------------\nUnfortunately, you have not picked the greatest number, {max(hidden)}.")
        f.write(f"The player has lost, having picked {hidden[counter - 1]} instead of the greatest number in {hidden}.\n")