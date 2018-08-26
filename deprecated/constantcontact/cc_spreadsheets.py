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

headers = ['Email', 'First Name', 'Last Name', 'Address 1', 'Address 2',
           'City', 'State', 'Zip', 'Phone']

column_number = 0
for header in headers:
    general_sheet.write(0, column_number, header)
    after_hours_sheet.write(0, column_number, header)
    column_number += 1

# Preps the workbook that contains the information desired.
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


def read():
    """Collects the contact information for each entry in the original workbook.

    Returns:
        tuple: Contains two lists, one with the contacts who purchased tickets
        to te After Hours film and the second with all others.
        """
    general_contacts = []
    after_hours_contacts = []
    for row in range(first_row, total_rows):
        general_contact = []
        after_hours_contact = []
        row_values = sh.row_values(row)
        opt_in = row_values[5]
        film_title = row_values[20]
        # Checks if patron opted-in.
        if not opt_in:
            continue
        # Checks if patron opted-in and purchased tickets for
        # the After Hours film.
        elif opt_in and film_title in films:
            after_hours_contact = [row_values[3], row_values[2].title(),
                                   row_values[1].title(), row_values[11],
                                   row_values[12], row_values[13].title(),
                                   row_values[14], row_values[15],
                                   row_values[16].replace('No Primary Phone',
                                                          '')]
            after_hours_contacts.append(after_hours_contact)
        # Checks if patron opted-in and purchased tickets for
        # non-After Hours films.
        elif opt_in and film_title not in films:
            general_contact = [row_values[3], row_values[2].title(),
                               row_values[1].title(), row_values[11],
                               row_values[12], row_values[13].title(),
                               row_values[14], row_values[15],
                               row_values[16].replace('No Primary Phone', '')]
            general_contacts.append(general_contact)
    return general_contacts, after_hours_contacts


def write(sheet, contacts):
    """Write the contact information of each contact, stored in a list, to a
    worksheet in a given workbook.

    Arguments:
        sheet = The sheet that will be written to in the workbook.
        contacts = The list of contacts that will be written to the sheet.
    """
    for row, contact in enumerate(contacts, start=1):
        for col, data in enumerate(contact):
            sheet.write(row, col, data)

general_list, ah_list = read()
write(general_sheet, general_list)
write(after_hours_sheet, ah_list)

general_book.save('Email Adds - General.xls')
after_hours_book.save('Email Adds - After Hours.xls')
