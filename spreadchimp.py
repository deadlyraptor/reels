import os
import xlrd
import xlwt

# Assumes the directory with the workbook is relative to the script's location.
directory = 'workbooks/'

workbook = ''
for dirpath, dirnames, filenames in os.walk(directory):
    for files in filenames:
        workbook = (dirpath + files)

'''
Test films include:
Repulsion
The Crying Game
Saint Joan
My LIfe as a Zucchini
'''
# Collects the names of all the films for which individual workbooks need to be
# created.
films = []
wbs = int(input('Number of workbooks to create: '))
for wb in range(0, wbs):
    film = input('Name the film: ')
    films.append(film)


def create_workbook():
    '''Creates a workbook.

    Arguments:
        none

    Returns:
        book = The workbook that was opened.
    '''
    headers = ['Email', 'First Name', 'Last Name', 'Phone', 'Address 1',
               'Address 2', 'City', 'State', 'Zip']
    book = xlwt.Workbook()
    sheet = book.add_sheet('Contacts')
    column_number = 0
    for header in headers:
        sheet.write(0, column_number, header)
        column_number += 1
    return book


def save_workbook(book, film):
    '''Saves the workbook created in create_workbook().

    Arguments:
        book = The object returned by calling create_workbook().
        film = The name of the film that will part of the workbook's name.

    Returns:
        none
    '''
    book.save('{0} contacts.xls'.format(film))


# Preps the workbook that contains the information desired.
wb = xlrd.open_workbook(workbook)
sh = wb.sheet_by_index(0)
total_rows = sh.nrows
first_row = 6  # skips the first six rows as they are irrelevant.


def prep_contacts():
    contacts = []
    for row in range(first_row, total_rows):
        contact = []
        row_values = sh.row_values(row)
        opt_in = row_values[5]
        film_title = row_values[20]
        if not opt_in:
            continue
        elif opt_in and film_title in films:
            contact = [row_values[3],  # email
                       row_values[2].title(),  # first name
                       row_values[1].title(),  # last name
                       row_values[16].replace('No Primary Phone', ''),  # phone
                       row_values[11],  # addrss 1
                       row_values[12],  # address 2
                       row_values[13].title(),  # city
                       row_values[14],   # state
                       row_values[15]]  # zip
            contacts.append(contact)
    return contacts


for film in films:
    save_workbook(create_workbook(), film)
    prep_contacts()
