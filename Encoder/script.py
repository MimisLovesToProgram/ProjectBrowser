# my_codec is a script I built in this directory, not a module from the Standard Library or Downloaded.
import my_codec
import os
import sys

# The contents of the file the user wants to interact with.
content = ""

# binary mode is still experimental, used to encrypt/decrypt binary files. Use 'repetition' to allow multiple encryptions/decryptions at once.
binary = "n"
repetition = 1

file = input("What file would you like to change? ")

# Checking if the given file exists within this directory.
while not file in os.listdir(os.getcwd() + "\\Encoder"):
    print("No such file in the Encoder's directory.")
    file = input("What file inside the Encoder's directory would you like to change? ")

funct = input("With what function? ")

# Checking if the function given is valid.
while funct != "encrypt" and funct != "decrypt":
    print("Invalid function. Valid functions are: encrypt | decrypt")
    funct = input("Enter one of the functions mentioned above: ")

# If the user enables Advanced settings, they will be asked to provide info to be stored in 'binary' and 'repetition'
advanced = input("Enable Advanced settings (y or n)? ")
if advanced != "n":
    binary = input("Are you changing a file different than just text (y or n)? ")
    repetition = int(input("How many times would you like to repeat this action? "))

# Performing the requested actions 'repetition' times, and checking how to treat the given file: as binary, or non-binary.
# Before performing the requested actions, make sure the file does not end up corrupted. If it doesn't, perform the requested action once.
for i in range(repetition):
    if binary != "n":
        with open(os.getcwd() + f"\\Encoder\\{file}", "rb") as f:
            content = f.read()
            # Checking whether the file will end up corrupted or not after performing the requested actions.
            for char in content:
                if len(my_codec.code) < my_codec.code.index(char) + repetition - i + 1 and funct == "encrypt":
                    print("Can't perform requested actions because the file would be corrupted.")
                    sys.exit(0)
                elif len(my_codec.code) < my_codec.code.index(char) - repetition + i + 1 and funct == "decrypt":
                    print("Can't perform requested actions because the file would be corrupted.")
                    sys.exit(0)
    else:
        with open(os.getcwd() + f"\\Encoder\\{file}") as f:
            content = f.read()
            # Checking whether the file will end up corrupted or not after performing the requested actions.
            for char in content:
                if len(my_codec.code) < my_codec.code.index(char) + repetition - i + 1 and funct == "encrypt":
                    print("Can't perform requested actions because the file would be corrupted.")
                    sys.exit(0)
                elif len(my_codec.code) < my_codec.code.index(char) - repetition + i + 1 and funct == "decrypt":
                    print("Can't perform requested actions because the file would be corrupted.")
                    sys.exit(0)

    # For each time the above tests pass (so that the file doesn't get corrupted), perform the requested actions.
    with open(os.path.join(os.getcwd(), "Encoder", file), "w") as f:
        try:
            if funct == "encrypt":
                f.write(my_codec.encrypt(content))
            else:
                f.write(my_codec.decrypt(content))
        except Exception as e:
            print(f"If you are seeing this, something went wrong while performing the requested actions.\nException: {e}")
            break
