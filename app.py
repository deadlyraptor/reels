import os
import xlrd
import xlwt

# Assumes directory with the workbooks is relative to script's location.
directory = 'workbooks/'

workbooks = []
for dirpath, dirnames, filenames in os.walk(directory):
    for files in filenames:
        workbooks.append(dirpath + files)

# Sets up the workbook that will be written to.
book = xlwt.Workbook()
sheet = book.add_sheet('Email Adds')

column_headers = ['First Name', 'Last Name', 'Email', 'Address 1', 'Address 2',
                  'City', 'State', 'Zip', 'Phone']

column_number = 0
for header in column_headers:
    sheet.write(0, column_number, header)
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
            variable: A column in columns.

        Returns:
            list: The values of all cells in the class's column.
            """
        rowx = 6
        colx = column
        patron_values = []
        for row in range(first_row, total_rows):
            if not sh.cell_value(rowx, colx=5):
                rowx += 1
            else:
                patron_values.append(sh.cell_value(rowx, colx))
                rowx += 1
        if column in [1, 2, 13]:
            return [value.title() for value in patron_values]
        elif column == 16:
            for index, phone in enumerate(patron_values):
                if phone == 'No Primary Phone':
                    patron_values[index] = ''
            return patron_values
        else:
            return patron_values

    def paste():
        """Write values of list returned by copy() to new workbook.
        """
        column_number = 0
        for column in columns:
            list_to_write = copy(column)
            row_number_to_write = row_number
            for item in list_to_write:
                sheet.write(row_number_to_write, column_number, item)
                row_number_to_write += 1
            column_number += 1
        global row_number
        row_number = row_number_to_write

    paste()

book.save('Email Adds.xls')
