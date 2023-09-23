import os

action = input("Would you like to read a saved item, add or delete one? (type read, add or delete) ")

if action == "read":
    choice = input("Type the title of the quiz to read: ")
    with open(f"{os.getcwd()}\\Quizes\\saved_quizes.txt") as f:
        # Getting the lines and iterating over them. 'correct' indicates whether we are operating over the lines the user asked for.
        lines = f.readlines()
        correct = False
        for line in lines:
            line = line.rstrip()
            # Giving 'correct' a value, before checking if we are able ask the user the questions of the quiz they asked for.
            if "--------" in line and line.endswith(choice):
                correct = True
            elif "--------" in line and not line.endswith(choice):
                correct = False
            if correct and not "--------" in line:
                # Asking the question, then giving the answer.
                input(line[:line.index("?")] + "? ")
                print("The answer is........" + line[line.index("?") + 1:])
elif action == "add":
    with open(f"{os.getcwd()}\\Quizes\\saved_quizes.txt", "a") as f:
        # Create the new quiz with the given title, then adding questions untill the user is done doing so.
        f.write(f"------------------------------------------------------------------------------------------------------------{input('What is the title of the Quiz going to be? ')}" + "\n")
        line = input("First line in the quiz: (type 'stop' anytime to finish writing) ")
        while line != "stop":
            f.write(line + "\n")
            line = input("Next line in the quiz: ")
else:
    # Getting the lines before changing anything. The rest is similar to the actions done when reading.
    plines = []
    lines = []
    correct = False
    with open(f"{os.getcwd()}\\Quizes\\saved_quizes.txt") as f:
        plines = f.readlines()
    choice = input("Type the title of the quiz to be deleted: ")
    for line in plines:
        # Just like reading, look for lines under the title the user gave, but only append all lines except for them to the new saved_quizes.txt
        line = line.rstrip()
        if "--------" in line and line.endswith(choice):
            correct = True
        elif "--------" in line and not line.endswith(choice):
            correct = False
        if not correct:
            lines.append(line + "\n")
    with open(f"{os.getcwd()}\\Quizes\\saved_quizes.txt", "w") as f:
        f.writelines(lines)
