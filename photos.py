import os
from datetime import date

# Programs at the Coral Gables Art Cinema.
programs = ['1. Main Features', '2. After Hours', '3. Special Screenings',
            '4. Family Day on Aragon', '5. National Theatre Live',
            '6. See It in 70mm', '7. Alternative Content']

for program in programs:
    print(program)

# These variables will make-up the full path, which takes the form:
# M:/Coral Gables Art Cinema/Programming/PROGRAM/YEAR/TITLE/LOCATION OF PHOTOS
root = 'M:/Coral Gables Art Cinema/Programming/'
index = int(input('Select a program by its number: '))
program = programs[index - 1][3:]
year = str(date.today().year)
title = input('Select a film: ')
photo_dir = input('Location of the photos: ')

new_name = input('Enter new base file name: ')

# The full path to the files, using the variables above.
path = os.path.join(root, program, year, title, photo_dir)

# Collect all the .jpg or .png files in the directory.
photos = []
for file in os.listdir(path):
    if file[-4:] in ('.jpg', '.jpeg', '.png'):
        photos.append(file)

# Rename all of the photos collected above and keep the same file type.
for number, photo in enumerate(photos, start=1):
    final_name = '{} {}{}'.format(new_name, number, photo[-4:])
    os.rename(os.path.join(path, photo), os.path.join(path, final_name))
