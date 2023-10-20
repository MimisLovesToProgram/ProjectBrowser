import requests
from bs4 import BeautifulSoup
import random
import os
import datetime

# Show the user the result file, for convenience.
with open(f"{os.getcwd()}\\Self-Improver\\result.txt") as f:
    print("Here are the contents of the project's result file, for convenience and informative purposes:\n")
    print(f.read() + "\n")

# Try to get quotes to show the user if they want to.
quotes_available = True
try:
    # Setting up BeautifulSoup, getting all the quotes from the HTML, and putting them as text on a list.
    response = requests.get(f"https://www.goodreads.com/quotes?page={random.randrange(1, 100)}")
    soup = BeautifulSoup(response.text, "html.parser")

    html_quotes = soup.find_all(class_="quoteText")
    quotes = [element.get_text() for element in html_quotes]
except Exception as exception:
    # Informing the user that they can not currently get quotes, and changing 'quotes_available' to False.
    quotes_available = False
    print(f"Unfortunately, the quotes site could not be reached. Error: {exception}")

action = input("Would you like to: 1) Set a new goal (or restart an existing one), 2) Update your current progress (or/and add notes), or 3) See some quotes? ")
if action == "1":
    # The previous lines, and the lines to be written.
    prevlines = []
    lines = []
    title = input("Give a title for your new goal (or for an existing one to be restarted): ")
    with open(f"{os.getcwd()}\\Self-Improver\\result.txt") as f:
        prevlines = f.readlines()

    # If there is not a goal with this title, create one in the following format.
    if not f"------------------------------------------------------------->{title}\n" in prevlines:
        with open(f"{os.getcwd()}\\Self-Improver\\result.txt", "a") as f:
            goal = input(f"What is {title}'s goal (in minutes)? ")
            f.write(f"------------------------------------------------------------->{title}\n")
            f.write(f"Goal (minutes): {goal}\n")
            f.write("Current Minute Count: 0\n")
            f.write(f"Date Started: {datetime.date.today().strftime('%Y-%m-%d')}\n")
            f.write("Notes: \n")
            f.write("Speed Record: -\n")
    # If there is a goal with this title, reset it with the data provided by the user.
    else:
        correct = False
        new_goal = input(f"What will {title}'s new goal be (in minutes)? ")
        while not new_goal.isnumeric():
            new_goal = input("Please enter a new minute goal. ")
        new_goal = int(new_goal)
        for line in prevlines:
            # Checking if we are iterating over the correct lines, and if not, not changing the rest of the lines.
            if "-----------------" in line and title in line:
                correct = True
                lines.append(line)
                continue
            if not correct:
                lines.append(line)
            # If we are iterating over the correct lines, append the lines in the desired format, with the new info.
            else:
                if "Goal (minutes): " in line:
                    lines.append(f"Goal (minutes): {new_goal}\n")
                elif "Current Minute Count: " in line:
                    lines.append("Current Minute Count: 0\n")
                elif "Date Started: " in line:
                    lines.append(f"Date Started: {datetime.date.today().strftime('%Y-%m-%d')}\n")
                elif "Speed Record: " in line:
                    # Since this is supposed to be the last line for a goal, correct can be set to false, so that the rest of the lines are left untouched.
                    lines.append(line)
                    correct = False
                else:
                    # This is just for the notes.
                    lines.append(line)

        with open(f"{os.getcwd()}\\Self-Improver\\result.txt", "w") as f:
            f.writelines(lines)

elif action == "2":
    # Again, getting the lines before modifying, and a list for the lines after modifications.
    prevlines = []
    lines = []
    with open(f"{os.getcwd()}\\Self-Improver\\result.txt") as f:
        prevlines = f.readlines()

    title = input("Please share the goal title you wish to update on: ")

    with open(f"{os.getcwd()}\\Self-Improver\\result.txt", "w") as f:
        # Declaring modification variables, and checking whether we are iterating over the correct lines of 'result.txt', just like above.
        minutes = 0
        goal = 0
        start_date = ""
        addition = ""
        correct = False
        notes = []
        upd_progress = input("Would you like to update your progress for this goal? (type 'yes' if so. Otherwise, you will be able to start writing notes) ").lower()
        for line in prevlines:
            if "---------" in line and title in line:
                correct = True
            elif "---------" in line and not title in line:
                correct = False
            if not correct:
                lines.append(line)
            
            # Performing the desired user action.
            if upd_progress == "yes":
                # If we are iterating over the correct lines, check if the line does or does not contain info to be modified or used later.
                if addition == "":
                    # Checking if the current value is the default one, so that when it is changed, the user isn't asked for more input in each loop.
                    addition = int(input(f"How many minutes have you worked on {title} until now today? "))
                if correct:
                    if not "Current Minute Count: " in line and not "Goal (minutes): " in line and not "Date Started: " in line and not "Speed Record: " in line:
                        lines.append(line)
                    elif "Current Minute Count: " in line:
                        # Modifying the Minute Count for the goal specified.
                        prev_count = int(line[21:].rstrip())
                        lines.append(f"Current Minute Count: {str(prev_count + addition)}\n")
                        minutes = prev_count + addition
                    elif "Goal (minutes): " in line:
                        # Getting the minute goal for this goal.
                        goal = int(line[16:].rstrip())
                        lines.append(line)
                    elif "Date Started: " in line:
                        # Getting the date the goal started as a datetime.datetime object in the format of 'YYYY-MM-DD'.
                        start_date = datetime.datetime.strptime(line[14:].rstrip(), "%Y-%m-%d")
                        lines.append(line)
                    # We must not interfere with Notes in the case the user wants to update the minute count, so if all the other ifs were skipped, and the line being checked is not a note, it is the Speed Record.
                    elif not "Notes: " in line and not line.startswith("  "):
                        # Congratulating the user if they have reached their goal.
                        if minutes >= goal:
                            end_date = datetime.datetime.strptime(str(datetime.datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
                            day_diff = end_date - start_date
                            if day_diff.days > int(line[14:].rstrip()):
                                lines.append(f"Speed Record: {day_diff.days}\n")
                            else:
                                lines.append(line)
                            print(f"Congrats! You have completed this goal in {day_diff.days} days!")
                        else:
                            # If nothing special happened, change nothing.
                            lines.append(line)
            else:
                if correct:
                    # If there are no notes, take some. This way, the user does not have to write notes for each loop.
                    if notes == []:
                        note = "banana"
                        while note != "  \n":
                            note = "  " + input("Type one line for this goal's notes (if you want to stop, type nothing): ") + "\n"
                            notes.append(note)
                        notes.remove("  \n")
                    # Once the line with "Notes: " has been reached, add it, among with the notes provided by the user.
                    if "Notes: " in line:
                        lines.append(line)
                        for item in notes:
                            lines.append(item)
                    # If the line is not a note (notes are indented), append it as it is.
                    elif not line.startswith("  "):
                        lines.append(line)

        f.writelines(lines)

else:
    # Keep showing quotes as long as the user wants to.
    keep_going = "yes"
    while keep_going == "yes":
        print(random.choice(quotes))
        keep_going = input("Want to see more quotes? Type yes if so. ").lower()