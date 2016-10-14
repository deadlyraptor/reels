import os
import xlrd
import xlwt

# Assumes the directory with the workbook is relative to the script's location.
directory = 'workbooks/'

workbook = ''
for dirpath, dirnames, filenames in os.walk(directory):
    for files in filenames:
        workbook = (dirpath + files)

# Sets up the general workbook that will be written to.
general_book = xlwt.Workbook()
general_sheet = general_book.add_sheet('Email Adds - General')

# Sets up the After Hours workbook that will be written to.
after_hours_book = xlwt.Workbook()
after_hours_sheet = after_hours_book.add_sheet('Email Adds - After Hours')

headers = ['First Name', 'Last Name', 'Email', 'Address 1', 'Address 2',
           'City', 'State', 'Zip', 'Phone']

column_number = 0
for header in headers:
    general_sheet.write(0, column_number, header)
    after_hours_sheet.write(0, column_number, header)
    column_number += 1

# Preps the workbook.
wb = xlrd.open_workbook(workbook)
sh = wb.sheet_by_index(0)
total_rows = sh.nrows
first_row = 6  # skips the first six rows as they are irrelevant.

# This creates a list with all of the After Hours films in the workbook.
films = []
weeks = int(input('How many weeks are in the workbook? '))
for week in range(0, weeks):
    film = input('The After Hours film for week {} was: '.format(week + 1))
    films.append(film)

# The different columns in which customer data is found.
first_name = 2
last_name = 1
email = 3
address_one = 11
address_two = 12
city = 13
state = 14
zip_code = 15
phone_number = 16

columns = [first_name, last_name, email, address_one, address_two, city, state,
           zip_code, phone_number]


def copy(column):
    """Return column from workbook as a list.

    Arguments:
        column: A column in columns.

    Returns:
        tuple: The two lists containing the cell values in each column.
        """
    rowx = 6
    colx = column
    general_values = []
    after_hours_contact_values = []
    for row in range(first_row, total_rows):
        opt_in = sh.cell_value(rowx, colx=5)
        film_title = sh.cell_value(rowx, colx=20)
        # Checks if patron opted-in.
        if not opt_in:
            rowx += 1
        # Checks if patron opted-in and purchased tickets for the After Hours film.
        elif opt_in and film_title in films:
            after_hours_contact_values.append(sh.cell_value(rowx, colx))
            rowx += 1
        # Checks if patron opted-in and purchased tickets for non-After Hours films.
        elif opt_in and film_title not in films:
            general_values.append(sh.cell_value(rowx, colx))
            rowx += 1
    # Formats first names, last names and cities as title cased.
    if column in [1, 2, 13]:
        return [value.title() for value in general_values], [value.title() for value in after_hours_contact_values]
    elif column == 16:
        for index, phone in enumerate(general_values):
            if phone == 'No Primary Phone':
                general_values[index] = ''
        for index, phone in enumerate(after_hours_contact_values):
            if phone == 'No Primary Phone':
                after_hours_contact_values[index] = ''
        return general_values, after_hours_contact_values
    else:
        return general_values, after_hours_contact_values

column_number = 0


def paste(sheet, list):
    """Write values of lists returned by copy() to new workbooks.
    """
    row = 1
    for item in list:
        sheet.write(row, column_number, item)
        row += 1

for column in columns:
    general_list_to_write, ah_list_to_write = copy(column)
    paste(general_sheet, general_list_to_write)
    paste(after_hours_sheet, ah_list_to_write)
    column_number += 1

general_book.save('Email Adds - General.xls')
after_hours_book.save('Email Adds - After Hours.xls')
