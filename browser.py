import os
import time
import sys

projects = {}
projectind = 0

# Loading the projects from this directory to the 'projects' dictionary.
for project in os.listdir():
    if os.path.isdir(project) and not project.startswith("."):
        projectind += 1
        projects[str(projectind)] = project

print("Hello there! Here are the projects available for you to browse: (Type 'help' for the Browser Guide)\n")

# A function to print a string word-by-word.
def slow_print(text:str) -> None:
    words = text.split(" ")
    for word in words:
        if "\n" in word:
            print(word, end=' ')
        else:
            print(word, end=' ')
            sys.stdout.flush()
            time.sleep(0.05)

# Prints all available projects.
def show() -> None:
    for index, name in projects.items():
        print(f"{index}: {name}")

show()

# If provided a string argument, it will print out the contents of the 'README.md' file of the index's equivalent project.
# If not, it will print out the contents of the 'README.md' file on this folder, explaining how the browser works.
def help(*args:str) -> None:
    if not args == ():
        # If an index is given, print its project's README.md
        index = args[0]
        with open(f"{os.getcwd()}\\{projects[index]}\\README.md") as f:
            slow_print(f"""\n{f.read()}""")
    else:
        # If not, read the browser's folder README.md
        with open(f"{os.getcwd()}\\README.md") as f:
            slow_print(f"""\n{f.read()}""")

# Clears the terminal's screen, and shows all the projects available.
def clear() -> None:
    os.system("cls")
    show()

# Runs the index's equivalent project's script.py
def run(index:str) -> None:
    os.system("cls")
    os.system(f"python {projects[index]}\\script.py")

# Prints the contents of the file where the results of the index's project are stored.
def results(index:str) -> None:
    if "result.txt" in os.listdir(f"{os.getcwd()}\\{projects[index]}"):
        # If the project has a result file, print its content.    
        with open(f"{os.getcwd()}\\{projects[index]}\\result.txt") as f:
            print(f"\n{f.read()}")
    else:
        print("This project has no result file!")

# Empties the index's project's result file.
def empty(index:str) -> None:
    if "result.txt" in os.listdir(f"{os.getcwd()}\\{projects[index]}"):
        # Again, we look for the result file in the project, if there is one, and if yes, emptying it.
        with open(f"{os.getcwd()}\\{projects[index]}\\result.txt", "w") as f:
            print(f"Emptied the result file of project {projects[index]}")
    else:
        print("This project does not have a result file!")

while True:
    # Typing a command, then running the command's respective function. If any, passing parameters given by splitting the command.
    command = input("\nType a command: ")
    if "exit" in command:
        exit()
    # Needed in case the user does anything wrong, so that the program does not end. Also giving an exception to know what to tell the developer.
    try:
        if "help" in command:
            if command.split(" ") == ["help"]:
                help()
            else:
                help(command.split(" ")[1])
        elif "run" in command:
            run(command.split(" ")[1])
        elif "results" in command:
            results(command.split(" ")[1])
        elif "clear" in command:
            clear()
        elif "show" in command:
            show()
        elif "empty" in command:
            empty(command.split(" ")[1])
        else:
            print(f"{command}: No such command. Try running 'help' to check how the browser works!")
    except Exception as e:

        slow_print(f"""\nOops! Something went wrong. You should perhaps try to check how what you tried to do works, by typing 'help', and the project's index.
Also, was there a logical mistake in your last command?
The following exception occured: {e}\n""")