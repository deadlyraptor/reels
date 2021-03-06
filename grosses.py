import os
import xlrd

directory = 'workbooks/'
file = os.listdir(directory)[0]

workbook = (f'{directory}/{file}')

wb = xlrd.open_workbook(workbook)
sheets = wb.sheets()

films = {}
admissions = []
grosses = []

for index, sheet in enumerate(sheets):
    last_row = sheet.nrows  # reaches admission & gross faster
    film = sheet.cell(1, 4).value
    # int removes unecessary .0 since admission is always a whole number
    admission = int(sheet.cell(last_row - 2, 4).value)
    gross = sheet.cell(last_row - 1, 4).value
    figures = dict([
                ('Admissions', admission),
                ('Gross', gross)
                ])
    films[film] = figures
    # easier to sum total admissions & grosses with a list
    # rather than looping through the films dict
    admissions.append(admission)
    grosses.append(gross)

'''
The main purpose of the script is to return the total admissions and gross for
the week but it is helpful to see the figures for each individual film.
'''
for key, value in films.items():
    print(key)
    for key, value in value.items():
        print(key, value)
    print()

print(f'Total attendance: {sum(admissions)}')
print(f'Total gross: {sum(grosses)} \n')

input('Press enter to exit: ')  # keeps window open
