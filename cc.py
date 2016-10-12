import os
import json
import requests
import xlrd
from credentials import client_id, token, general_list_id, ah_list_id

# Constant Contact API.
base_url = 'https://api.constantcontact.com/v2/activities'
endpoint = '/addcontacts?api_key='
url = base_url + endpoint + client_id
headers = {'Authorization': ('Bearer ' + token)}

# Workbook location.
directory = 'workbooks/'

workbook = ''
for dirpath, dirnames, filenames in os.walk(directory):
    for files in filenames:
        workbook = (dirpath + files)

# Workbook setup.
wb = xlrd.open_workbook(workbook)
sh = wb.sheet_by_index(0)
total_rows = sh.nrows
first_row = 6

# These lists will hold customer data in dictionaries.
general_contacts = []
after_hours_contacts = []

after_hours_film = input('What is the After Hours film? ')


def append_dict_to_list(ls):
    '''Creates dictionary with customer contact info.

    Arguments:
        ls = The list the dictionary will be appended to.

    Returns:
        A list appended with the appropriate contacts.
    '''
    contacts['email_addresses'] = [row_values[3]]
    contacts['first_name'] = row_values[2].title()
    contacts['last_name'] = row_values[1].title()

    if row_values[16] == 'No Primary Phone':
        contacts['home_phone'] = ''
    else:
        contacts['home_phone'] = row_values[16]
    contacts['addresses'] = [address]

    address['line1'] = row_values[11]
    address['line2'] = row_values[12]
    address['city'] = row_values[13].title()
    address['state_code'] = row_values[14]
    address['postal_code'] = row_values[15]

    ls.append(contacts)


def create_payload(ls, list_id):
    '''Creates the JSON payloads sent in the request to the Constant Contact API.

    Arguments:
        ls = The list of customer data generated by append_dict_to_list().
        list_id = The ID of the list in Constant Contact that the new contacts
        will be uploaded to.

    Returns:
        payload: The payload that will be passed to cc(), which handles the
        request to the Constant Contact API.
    '''
    payload = {'import_data': ls,
               'lists': [list_id],
               'column_names': ['Email Address', 'First Name',
                                'Last Name', 'Home Phone',
                                'Address Line 1', 'Address Line 2',
                                'City', 'State',
                                'Zip/Postal Code']}
    return payload


def cc(function):
    '''Uploads JSON payload with customer data to Constant Contact.

    Arguments:
        function = The function create_payload() that creates the
        required payload.
    '''
    r = requests.post(url, headers=headers, json=function)
    print(r.status_code)
    print(r.reason)
    print(r.text)
    print('-------------')

# Loops over the workbook and appends the dictionaries created by calling
# append_dict_to_list into the corresponding lists..
for row in range(first_row, total_rows):
    contacts = {}
    address = {}
    row_values = sh.row_values(row)
    opt_in = row_values[5]
    film_title = row_values[20]
    if not opt_in:
        continue
    elif opt_in and film_title == after_hours_film:
        append_dict_to_list(after_hours_list)
    elif opt_in and film_title != after_hours_film:
        append_dict_to_list(general_list)

cc(create_payload(general_list, general_list_id))
cc(create_payload(after_hours_list, after_hours_list))
