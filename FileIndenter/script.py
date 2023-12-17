from tkinter import filedialog
import re

# Opening the File Explorer on Tkinter, and prompting the user to select a file from there.
file = filedialog.askopenfilename(title="Select a file.", filetypes=[("All files", "*.*")])

# Making sure that a file was selected.
if not file:
    print("Next time make sure to select a file.")
    exit()

# Getting the file's current indentation, and making sure it is valid.
current_indentation = input("Enter the file's current space indentation: ")
while not current_indentation.isnumeric():
    current_indentation = input("Please enter a number for the file's current indentation: ")
current_indentation = int(current_indentation)

# Getting the file's desired indentation, and making sure it is valid.
final_indentation = input("How many spaces should the file end up being indented by? ")
while not final_indentation.isnumeric():
    final_indentation = input("Please type a number for the file's final indentation: ")
final_indentation = int(final_indentation)

# Getting the file's lines.
lines = []
with open(file) as f:
    lines = f.readlines()

# Filling a new list up with the new, processed lines.
new_lines = []
for line in lines:
    # Unless we check that the line is not a newline character, the line would be stripped and the empty line would not be present in the processed version of the file.
    if line == "\n":
        new_lines.append("\n")
        continue
    # Getting the line's spaces, and indenting the line accordingly (first getting how many blocks up the line is, multiplying it by final_indentation to get the desired indentation).
    spaces = len(re.search(r"^( *)", line).group(1))
    new_lines.append(f"{(spaces // current_indentation) * final_indentation * " "}{line.lstrip()}")

# Finally, writing the processed lines to the file.
with open(file, "w") as f:
    f.writelines(new_lines)