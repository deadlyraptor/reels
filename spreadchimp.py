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
    headers = ['First Name', 'Last Name', 'Email', 'Phone', 'Full address']
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


for film in films:
    save_workbook(create_workbook(), film)
