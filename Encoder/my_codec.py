# This script is only used as a package for 'script.py'.

# This line of characters contains every character that can be encoded. The sorting determines what character will be turned to what when encrypting / decrypting
code = "aRb?cGd/Nef^gZ_h&iAj*kD#lm>Mno pQF\"q~rOs<t\tCuLPv:HwT+x!y$z}1.2]3\\4%SB5{6K|V;7@8Y9'0E\nU-X=I[,W()J`"

# Dictionaries that will have every character from 'code', and a value of their next character on the list, and the previous one respectively.
next = {}
previous = {}

# 'next' will be used for encrypting, while 'previous' for decrypting.

index = -1

# Filling the two dictionaries.
for letter in code:
    index += 1
    # You can't encrypt the last character on 'code', and can't decrypt the first one, due to indexing errors.
    if not code.endswith(letter):
        next[letter] = code[index + 1]
    if not code.startswith(letter):
        previous[letter] = code[index -1]

# Used when encrypting a string, by taking and combining the next character in 'code' for every character in 'text', then returning this combination.
def encrypt(text:str) -> str:
    result = ""
    for letter in text:
        # Always check if the current character is in 'code', or it can't by encrypted.
        if letter in code:
            if not code.endswith(letter):
                result += next[letter]
        else:
            input(f"Couldn't encrypt one of the carracters given: {letter}\nPress anything to terminate the program ")
            break
    return result

# Used when decrypting an encrypted string, by taking and combining the previous characters in 'code' for every character, then returning this combination.
def decrypt(text:str) -> str:
    result = ""
    for letter in text:
        # Just like encrypting, you can't decrypt a character that is not in 'code'.
        if letter in code:
            result += previous[letter]
        else:
            input(f"Couldn't decrypt one of the characters given: {letter}\nPress anything to terminate the program ")
            break
    return result