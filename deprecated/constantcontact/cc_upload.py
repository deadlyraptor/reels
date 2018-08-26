import os
import requests
import xlrd
import constantcontact as cc
from credentials import general_list_id, after_hours_list_id

# Assumes directory with the workbook is relative to script's location.
directory = 'workbooks/'

workbook = ''
for dirpath, dirnames, filenames in os.walk(directory):
    for files in filenames:
        workbook = (dirpath + files)

# Preps the workbook.
wb = xlrd.open_workbook(workbook)
sh = wb.sheet_by_index(0)
total_rows = sh.nrows
first_row = 6  # skips the first six rows as they are irrelevant.

# These lists will hold customer data in dictionaries.
general_contacts = []
after_hours_contacts = []

# This creates a list with all of the After Hours films in the workbook.
films = []
weeks = int(input('How many weeks are in the workbook? '))
for week in range(0, weeks):
    film = input('The After Hours film for week {} was: '.format(week + 1))
    films.append(film)


def append_contacts(contacts):
    '''Populates the contact and address dictionaries and then appends them to
    a contacts list.

    Arguments:
        contacts = The list the dictionary will be appended to.
    '''
    contact['email_addresses'] = [row_values[3]]
    contact['first_name'] = row_values[2].title()
    contact['last_name'] = row_values[1].title()
    contact['home_phone'] = row_values[16].replace('No Primary Phone', '')

    contact['addresses'] = [address]

    address['line1'] = row_values[11]
    address['line2'] = row_values[12]
    address['city'] = row_values[13].title()
    address['state_code'] = row_values[14]
    address['postal_code'] = row_values[15]

    contacts.append(contact)

# Loops over the workbook and appends the dictionaries created by calling
# append_contacts into the corresponding lists.
for row in range(first_row, total_rows):
    contact = {}
    address = {}
    row_values = sh.row_values(row)
    opt_in = row_values[5]
    film_title = row_values[20]
    if not opt_in:
        continue
    elif opt_in and film_title in films:
        append_contacts(after_hours_contacts)
    elif opt_in and film_title not in films:
        append_contacts(general_contacts)

# General list.
general_payload = cc.create_payload(general_contacts, [general_list_id])
activity = cc.add_contacts(general_payload)
status_report = cc.get_status(activity)
cc.poll_activity(status_report)

# After Hours list.
after_hours_payload = cc.create_payload(after_hours_contacts,
                                        [after_hours_list_id])
activity = cc.add_contacts(after_hours_payload)
status_report = cc.get_status(activity)
cc.poll_activity(status_report)
