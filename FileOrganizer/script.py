import os
import shutil
import mimetypes

# Getting information about the folder to organize, and the user's name.
# Why have mid_folders instead of just folder with an input? With mid_folders its easier to get the user's name, to be used later.
mid_folders = input("Type the folders from your user's folder to the folder to be organized (separated by '\\') ").split("\\")
user = mid_folders[0]
folder = "C:\\Users\\" + "\\".join(mid_folders)

folder_created = False
new_folder = ""

# Getting the user's desired actions and validating the variable 'segment', so that no errors or unexpected behaviour occurs.
choice = input("Organize by 1: extension or 2: naming segment? (1 or 2) ")
segment = input("Type a segment common to every file to be organized, or an extension to organize by. ")
while segment == "":
    segment = input("Please give a segment or extension. ")

# Iterating over the selected folder, and acting accordingly to the user's desires.
for file in os.listdir(folder):
    if segment in file:
        if choice == "1":
            # Checking the file's type, if Windows has a default folder for it, and if yes, create a new folder in the default one and move the
            # file there.
            filetype = mimetypes.guess_type(f"{folder}\\{file}")[0].split('/')[0]
            if filetype == "image":
                if not folder_created:
                    new_folder = input('Name a folder to to put the files to be organized in: ')
                    os.mkdir(f"C:\\Users\{user}\Pictures\{new_folder}")
                    folder_created = True
                shutil.move(f"{folder}\\{file}", f"C:\\Users\{user}\Pictures\{new_folder}\{file}")
            elif filetype == "text":
                if not folder_created:
                    new_folder = input('Name a folder to to put the files to be organized in: ')
                    os.mkdir(f"C:\\Users\{user}\Documents\{new_folder}")
                    folder_created = True
                shutil.move(f"{folder}\\{file}", f"C:\\Users\{user}\Documents\{new_folder}\{file}")
            elif filetype == "audio":
                if not folder_created:
                    new_folder = input('Name a folder to to put the files to be organized in: ')
                    os.mkdir(f"C:\\Users\{user}\Music\{new_folder}")
                    folder_created = True
                shutil.move(f"{folder}\\{file}", f"C:\\Users\{user}\Music\{new_folder}\{file}")
            elif filetype == "video":
                if not folder_created:
                    new_folder = input('Name a folder to to put the files to be organized in: ')
                    os.mkdir(f"C:\\Users\{user}\Videos\{new_folder}")
                    folder_created = True
                shutil.move(f"{folder}\\{file}", f"C:\\Users\{user}\Videos\{new_folder}\{file}")
            # If there is no default folder for this file type, create one on the selected folder and move the file there.
            elif not folder_created:
                new_folder = input('Name a folder to to put the files to be organized in: ')
                os.mkdir(f"{folder}\{new_folder}")
                folder_created = True
                shutil.move(f"{folder}\\{file}", f"{folder}\{new_folder}\{file}")
            # If there is no default folder, and one has been created by the user, move the file there.
            else:
                shutil.move(f"{folder}\\{file}", f"{folder}\{new_folder}\{file}")
        else:
            # Since files with substrings don't have default folders, just check if there is one, if not, create one, and put the file there.
            if not folder_created:
                new_folder = input('Name a folder to to put the files to be organized in: ')
                os.mkdir(f"{folder}\{new_folder}")
                folder_created = True
                shutil.move(f"{folder}\\{file}", f"{folder}\{new_folder}\{file}")
            else:
                shutil.move(f"{folder}\\{file}", f"{folder}\{new_folder}\{file}")