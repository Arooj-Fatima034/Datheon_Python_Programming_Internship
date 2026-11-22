# Task 3: File Organizer

This is a Python script that organizes a messy folder (like Downloads). It looks at the extension of each file and moves it into a folder like Documents, Images, Videos, Archives or Code.

## Features

- Checks the extension of every file
- Creates category folders automatically
- Moves files using shutil.move()
- Renames a file if the same name already exists (photo_1.jpg), so nothing gets overwritten
- Handles PermissionError and FileExistsError
- Skips files with unknown extensions
- Prints a summary of moved, skipped and failed files
- Saves a log of everything in organizer.log

Files used: os, shutil, pathlib and logging.

## How to run

1. Open a terminal in the folder where organizer.py is saved.
2. Run: python organizer.py
3. Enter the path of the folder you want to organize, or press Enter to use the Downloads folder.
