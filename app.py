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

# after_hours_film = input('What is the After Hours film?: ')
after_hours_film = 'Kill Bill: Volume 1'

# The first row that will be written to. This variable increments each time the
# main loop runs. The stored value is the row number where the second iteration
# of the loop must starting writing to.
row_number = 1

for workbook in workbooks:

    wb = xlrd.open_workbook(workbook)
    sh = wb.sheet_by_index(0)
    total_rows = sh.nrows
    first_row = 6

    class Column():
        """A class used to store column number of each required column.
        """
        def __init__(self, col):
            """Instantiates class with one attribute.

            Attribute:
                col: A column number from the workbook being read.
            """
            self.col = col

    first_name = Column(2)
    last_name = Column(1)
    email = Column(3)
    address_one = Column(11)
    address_two = Column(12)
    city = Column(13)
    state = Column(14)
    zip_code = Column(15)
    phone_number = Column(16)

    columns = [first_name, last_name, email, address_one, address_two, city,
               state, zip_code, phone_number]

    def copy(variable):
        """Return column from workbook as a list.

        Arguments:
            variable: The class instance found in list classes.

        Returns:
            list: The values of all cells in the class's column.
            """
        rowx = 6
        colx = variable.col
        patron_values = []
        for row in range(first_row, total_rows):
            if not sh.cell_value(rowx, colx=5) or sh.cell_value(rowx, colx=20) == after_hours_film:
                rowx += 1
            else:
                patron_values.append(sh.cell_value(rowx, colx))
                rowx += 1
        if variable.col == 1 or variable.col == 2:
            name_list = [name.title() for name in patron_values]
            return name_list
        elif variable.col == 13:
            city_list = [city.title() for city in patron_values]
            return city_list
        elif variable.col == 16:
            for index, phone in enumerate(patron_values):
                if phone == 'No Primary Phone':
                    patron_values[index] = ''
            return patron_values
        else:
            return patron_values

    def copyAH(variable):
        """Return column from workbook as a list.

        Arguments:
            variable: The class instance found in list classes.

        Returns:
            list: The values of all cells in the class's column.
            """
        rowx = 6
        colx = variable.col
        ah_patron_values = []
        for row in range(first_row, total_rows):
            if not sh.cell_value(rowx, colx=5) or not sh.cell_value(rowx, colx=20) == after_hours_film:
                rowx += 1
            elif sh.cell_value(rowx, colx=5) and sh.cell_value(rowx, colx=20) == after_hours_film:
                ah_patron_values.append(sh.cell_value(rowx, colx))
                rowx += 1
        if variable.col == 1 or variable.col == 2:
            ah_name_list = [name.title() for name in ah_patron_values]
            return ah_name_list
        elif variable.col == 13:
            ah_city_list = [city.title() for city in ah_patron_values]
            return ah_city_list
        elif variable.col == 16:
            for index, phone in enumerate(ah_patron_values):
                if phone == 'No Primary Phone':
                    patron_values[index] = ''
            return ah_patron_values
        else:
            return ah_patron_values

    def paste():
        """Write values of list returned by copy() to new workbook.
        """
        column_number = 0
        for column in columns:
            list_to_write = copy(column)
            row_number_to_write = row_number
            for item in list_to_write:
                general_sheet.write(row_number_to_write, column_number, item)
                row_number_to_write += 1
            column_number += 1
        global row_number
        row_number = row_number_to_write

    def pasteAH():
        """Write values of list returned by copy() to new workbook.
        """
        column_number = 0
        for column in columns:
            list_to_write = copyAH(column)
            row_number_to_write = row_number
            for item in list_to_write:
                after_hours_sheet.write(row_number_to_write, column_number, item)
                row_number_to_write += 1
            column_number += 1
        global row_number
        row_number = row_number_to_write

    paste()
    pasteAH()

general_book.save('Email Adds - General.xls')
after_hours_book.save('Email Adds - After Hours.xls')
