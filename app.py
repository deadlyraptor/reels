import os
import xlrd
import xlwt

directory = 'workbooks/'

workbooks = []
for dirpath, dirnames, filenames in os.walk(directory):
    for files in filenames:
        workbooks.append(dirpath + files)

book = xlwt.Workbook()
sheet = book.add_sheet('Email Adds')
row_number = 0

for thing in workbooks:

    wb = xlrd.open_workbook(thing)
    sh = wb.sheet_by_index(0)
    total_rows = sh.nrows
    first_row = 6

    class Column():
        """Instantiates a class whose attributes are the column number for the data
        it contains and a boolean to check whether the first letter of the str
        ings
        in the list need to be capitalized.
        """
        def __init__(self, col, caps):
            """
            Args:
                col: A column number from the workbook being read.
                caps: Boolean used to run if statement that returns names in
                    proper caps, e.g. NAME --> Name.
            """
            self.col = col
            self.caps = caps

    # The variable names for the class instances are the columns in the
    # workbook.
    c = Column(2, True)  # first name
    b = Column(1, True)  # last name
    d = Column(3, False)  # email
    k = Column(10, False)  # Address 1
    l = Column(11, False)  # Address 2
    m = Column(12, False)  # City
    n = Column(13, False)  # State
    o = Column(14, False)  # Zip
    p = Column(15, False)  # Phone

    classes = [c, b, d, k, l, m, n, o, p]

    def copy(variable):
        """Return column from workbook as a list.

        Args:
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
        if variable.caps:
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
