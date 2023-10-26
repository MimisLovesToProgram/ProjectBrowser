import random
import os

# The length of the passwords to be generated, the current password generated and a list of words to be filled from a dictionary, respectively.
plen = 13
password = ""
words = []

num = int(input("How many passwords do you want? "))

# Adding all words from the dictionary to the list 'words'.
with open(os.path.join(os.getcwd(), "PasswordGenerator", "dictionary.txt")) as d:
    words = d.readlines()

for i in range(num):
    # Creating the passwords based on a pattern, thus using a loop till the password length has been surpassed or reached.
    while len(password) < plen:
        pattern = ""
        pattern += random.choice(".?!_-")
        pattern += random.choice(words).rstrip()
        for i in range(2):
            pattern += random.choice("1234567890")
        password += pattern

    # Write the generated password in PassLog.log, but only from start to the length limit.
    with open(os.path.join(os.getcwd(), "PasswordGenerator", "result.txt"), "a") as l:
        l.write(password[:plen] + "\n")

    password = ""
