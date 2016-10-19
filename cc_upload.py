import os
import xlrd
import requests
from credentials import client_id, token, general_list_id, after_hours_list_id

# Constant Contact API.
base_url = 'https://api.constantcontact.com/v2/activities'
endpoint = '/addcontacts?api_key='
url = base_url + endpoint + client_id
headers = {'Authorization': ('Bearer ' + token)}

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

    if row_values[16] == 'No Primary Phone':
        contact['home_phone'] = ''
    else:
        contact['home_phone'] = row_values[16]

    contact['addresses'] = [address]

    address['line1'] = row_values[11]
    address['line2'] = row_values[12]
    address['city'] = row_values[13].title()
    address['state_code'] = row_values[14]
    address['postal_code'] = row_values[15]

    contacts.append(contact)


def create_payload(contacts, list_id):
    '''Creates the JSON payloads sent in the request to the Constant Contact API.

    Arguments:
        contacts = The list of contacts generated by append_contacts().
        list_id = The ID of the list in Constant Contact that the new contacts
        will be uploaded to.

    Returns:
        payload: a JSON formatted dictionary with a list of contacts, the ID of
        the Constant Contact list the contacts will be added to, and the column
        names of the contacts's data.
    '''
    payload = {'import_data': contacts,
               'lists': [list_id],
               'column_names': ['Email Address', 'First Name',
                                'Last Name', 'Home Phone',
                                'Address Line 1', 'Address Line 2',
                                'City', 'State',
                                'Zip/Postal Code']}
    return payload


def add_contacts(payload):
    '''POSTs a JSON payload to the Constant Contact API.

    Arguments:
        payload = The payload returned by create_payload().
    '''
    r = requests.post(url, headers=headers, json=payload)
    print(r.status_code)
    print(r.reason)
    print(r.text)
    print('-------------')

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

add_contacts(create_payload(general_contacts, general_list_id))
add_contacts(create_payload(after_hours_contacts, after_hours_list_id))