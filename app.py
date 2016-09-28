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

            Attributes:
                col: A column number from the workbook being read.
            """
            self.col = col

    # The variable names for the class instances are the columns in the
    # workbook.
    c = Column(2)  # first name
    b = Column(1)  # last name
    d = Column(3)  # email
    k = Column(10)  # Address 1
    l = Column(11)  # Address 2
    m = Column(12)  # City
    n = Column(13)  # State
    o = Column(14)  # Zip
    p = Column(15)  # Phone

    classes = [c, b, d, k, l, m, n, o, p]

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
            if not sh.cell_value(rowx, colx=4):
                rowx += 1
            else:
                patron_values.append(sh.cell_value(rowx, colx))
                rowx += 1
        if variable.col == 1 or variable.col == 2:
            name_list = [name.capitalize() for name in patron_values]
            return name_list
        elif variable.col == 12:
            city_list = [city.title() for city in patron_values]
            return city_list
        elif variable.col == 15:
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
        for class_instance in classes:
            list_to_write = copy(class_instance)
            row_number_to_write = row_number
            for item in list_to_write:
                sheet.write(row_number_to_write, column_number, item)
                row_number_to_write += 1
            column_number += 1
        global row_number
        row_number = row_number_to_write

    paste()

book.save('Email Adds.xls')
