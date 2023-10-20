import re
import os

strength = 0
password = input("Enter a password to check its strength: ")

# Creating a generator to iterate over words in dictionary.txt efficiently.
def words():
    with open(f"{os.getcwd()}\\PasswordStrengthChecker\\dictionary.txt") as f:
        for word in f.readlines():
            yield word

# Adjusting the variable 'strength' according to what is contained in the password.
for i in range(len(password)):
    strength += 5

for i in range(len(re.findall(r"[!'#$%&()*+,-\\/^@<>[]{}=_|.`?]", password))):
    strength += 14

for i in range(len(re.findall(r"[A-Z]", password))):
    strength += 8

for i in range(len(re.findall(r"[0-9]", password))):
    strength += 8

for word in words():
    if word.lower().strip() in password.lower():
        strength -= 10

if password.isnumeric():
    strength -= 50

if password.isalpha():
    strength -= 30

# Fixing the value if it has gone beyond the possible limits.
if strength > 100:
    strength = 100
elif strength < 0:
    strength = 0

print(f"{strength}% Strength")
