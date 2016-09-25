import xlrd
import xlwt
import settings

wb = xlrd.open_workbook(settings.location)
sh = wb.sheet_by_index(0)
total_rows = sh.nrows
first_row = 6

fname = []
def firstName():
    rowx = 6
    colx = 2
    for row in range(first_row, total_rows):
        if not sh.cell_value(rowx, colx=4):
            rowx += 1
        else:
            fname.append(sh.cell_value(rowx, colx))
            rowx += 1
    print(fname)

lname = []
def lastName():
    rowx = 6
    colx = 1
    for row in range(first_row, total_rows):
        if not sh.cell_value(rowx, colx=4):
            rowx += 1
        else:
            lname.append(sh.cell_value(rowx, colx))
            rowx += 1
    print(lname)

elist = []
def email():
    rowx = 6
    colx = 3
    for row in range(first_row, total_rows):
        if not sh.cell_value(rowx, colx=4):
            rowx += 1
        else:
            elist.append(sh.cell_value(rowx, colx))
            rowx += 1
    print(elist)

firstName()
lastName()
email()

book = xlwt.Workbook()
sheet = book.add_sheet('Email Adds')


def wfname():
    column_number = 0
    for row_number, item in enumerate(fname):
        sheet.write(row_number, column_number, item)


def wlname():
    column_number = 1
    for row_number, item in enumerate(lname):
        sheet.write(row_number, column_number, item)


def wemail():
    column_number = 2
    for row_number, item in enumerate(elist):
        sheet.write(row_number, column_number, item)

wfname()
wlname()
wemail()

book.save('Email Adds.xls')
