import xlrd
import xlwt
import settings

wb = xlrd.open_workbook(settings.location)
sh = wb.sheet_by_index(0)
total_rows = sh.nrows
first_row = 6


class Column():
    '''Instantiates a class whose attributes are the column number for the data
    it contains and a boolean to check whether the first letter of the strings
    in the list need to be capitalized.
    '''
    def __init__(self, col, caps):  # col = column number, caps = True or False
        self.col = col
        self.caps = caps

# The variable names for the class instances are the columns in the workbook.
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
        print(city_list)
        return city_list
    else:
        return patron_values

book = xlwt.Workbook()
sheet = book.add_sheet('Email Adds')


def paste():
    column_number = 0
    for class_instance in classes:
        list_to_write = copy(class_instance)
        for row_number, item in enumerate(list_to_write):
            sheet.write(row_number, column_number, item)
        column_number += 1

paste()

book.save('Email Adds.xls')
