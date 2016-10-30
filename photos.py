import os
from datetime import date

# Programs at the Coral Gables Art Cinema.
programs = ['1. Main Features', '2. After Hours', '3. Special Screenings',
            '4. Family Day on Aragon', '5. National Theatre Live',
            '6. See It in 70mm', '7. Alternative Content']

for program in programs:
    print(program)

index = int(input('Select a program by its number: '))
program = programs[index - 1][3:]


title = input('Select a film: ')
photo_dir = input('Location of the photos: ')
new_name = input('Enter new base file name: ')

root = 'M:/Coral Gables Art Cinema/Programming/'
year = str(date.today().year)

path = os.path.join(root, program, year, title, photo_dir)

num_suffix = 1
for photo in os.listdir(path):
    final_name = '{} {}.jpg'.format(new_name, num_suffix)
    os.rename(os.path.join(path, photo), os.path.join(path, final_name))
    num_suffix += 1
