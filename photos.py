import os
import sys
import tkinter as tk
from tkinter import filedialog

# tkinter is only used for directory prompt
root = tk.Tk()
root.withdraw()  # hides default window
directory = filedialog.askdirectory()

# if user does not select a directory, exit the script
if not directory:
    sys.exit()

base_name = input('Enter the new base filename: ')

# renames each photo in the selected directory
with os.scandir(directory) as photo_directory:
    for number, photo in enumerate(photo_directory, start=1):
        if photo.name.endswith(('.jpg', '.jpeg', '.png')):
            new_name = f'{base_name} {number}.{photo.name.split(".")[1]}'
            os.rename(photo, os.path.join(directory, new_name))
