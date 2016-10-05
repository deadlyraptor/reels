import os
import xlrd
import xlwt

# Assumes directory with the workbooks is relative to script's location.
directory = 'workbooks/'

workbooks = []
for dirpath, dirnames, filenames in os.walk(directory):
    for files in filenames:
        workbooks.append(dirpath + files)

# Sets up the general workbook that will be written to.
general_book = xlwt.Workbook()
general_sheet = general_book.add_sheet('Email Adds - General')
# Sets up the After Hours workbook that will be written to.
after_hours_book = xlwt.Workbook()
after_hours_sheet = after_hours_book.add_sheet('Email Adds - After Hours')

column_headers = ['First Name', 'Last Name', 'Email', 'Address 1', 'Address 2',
                  'City', 'State', 'Zip', 'Phone']

column_number = 0
for header in column_headers:
    general_sheet.write(0, column_number, header)
    after_hours_sheet.write(0, column_number, header)
    column_number += 1

# The first row that will be written to. This variable increments each time the
# main loop runs. The stored value is the row number where the second iteration
# of the loop must starting writing to.
row_number = 1

for workbook in workbooks:

    wb = xlrd.open_workbook(workbook)
    sh = wb.sheet_by_index(0)
    total_rows = sh.nrows
    first_row = 6
    # after_hours_film = input('What is the After Hours film?: ')
    after_hours_film = 'Kill Bill: Volume 1'

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

    columns = [first_name, last_name, email, address_one, address_two, city,
               state, zip_code, phone_number]

    def copy(column):
        """Return column from workbook as a list.

        Arguments:
            column: A column in columns.

        Returns:
            tuple: The two lists containing the cell values in each column.
            """
        rowx = 6
        colx = column
        patron_values = []
        ah_patron_values = []
        for row in range(first_row, total_rows):
            opt_in = sh.cell_value(rowx, colx=5)
            film_title = sh.cell_value(rowx, colx=20)
            # Checks if patron opted-in.
            if not opt_in:
                rowx += 1
            # Checks if patron opted-in and purchased tickets for the After Hours film.
            elif opt_in and film_title == after_hours_film:
                ah_patron_values.append(sh.cell_value(rowx, colx))
                rowx += 1
            # Checks if patron opted-in and purchased tickets for non-After Hours films.
            elif opt_in and not film_title == after_hours_film:
                patron_values.append(sh.cell_value(rowx, colx))
                rowx += 1
        # Formats first names, last names and cities as title cased.
        if column in [1, 2, 13]:
            return [value.title() for value in patron_values], [value.title() for value in ah_patron_values]
        elif column == 16:
            for index, phone in enumerate(patron_values):
                if phone == 'No Primary Phone':
                    patron_values[index] = ''
            for index, phone in enumerate(ah_patron_values):
                if phone == 'No Primary Phone':
                    ah_patron_values[index] = ''
            return patron_values, ah_patron_values
        else:
            return patron_values, ah_patron_values

    column_number = 0

    def paste(sheet_to_write, list_to_write):
        """Write values of lists returned by copy() to new workbooks.
        """
        row_number_to_write = row_number
        for item in list_to_write:
            sheet_to_write.write(row_number_to_write, column_number, item)
            row_number_to_write += 1
        # global row_number
        # row_number = row_number_to_write

    for column in columns:
        general_list_to_write, ah_list_to_write = copy(column)
        paste(general_sheet, general_list_to_write)
        paste(after_hours_sheet, ah_list_to_write)
        column_number += 1

general_book.save('Email Adds - General.xls')
after_hours_book.save('Email Adds - After Hours.xls')
