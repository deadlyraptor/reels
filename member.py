import requests
from email import message_from_string
from base64 import urlsafe_b64decode
from credentials import label_id, members_list_id
from credentials import token, client_id
from gmailauth import refresh

# Constant Contact API.
base_url = 'https://api.constantcontact.com/v2/activities'
endpoint = '/addcontacts?api_key='
url = base_url + endpoint + client_id
cc_headers = {'Authorization': ('Bearer ' + token)}

access_token = refresh()

headers = {'Authorization': ('Bearer ' + access_token)}


def list_messages(headers):
        params = {'labelIds': label_id, 'q': 'newer_than:3d'}
        r = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages',
                         headers=headers, params=params)
        j = r.json()
        messages = []
        if 'messages' in j:
            messages.extend(j['messages'])
        message_ids = []
        for item in messages:
            message_ids.append(item['id'])
        return message_ids


def get_message(headers, identity):
    params = {'id': identity, 'format': 'raw'}
    r = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages/id',
                     headers=headers, params=params)
    j = r.json()
    raw = j['raw']
    byte = urlsafe_b64decode(raw)
    string = byte.decode()
    msg = message_from_string(string)
    return msg


def get_contact(msg):
    msg_string = msg.get_payload()
    body = msg_string.split()
    delimiter = '='

    elements = {'first_name': body[22], 'last_name': body[23],
                'email_address': body[24], 'home_phone': body[25]}

    for key in elements:
        delimiter_index = elements[key].find(delimiter)
        elements[key] = elements[key][:delimiter_index]

    members = []
    contact = {}
    contact['email_addresses'] = [elements['email_address']]
    contact['first_name'] = elements['first_name'].title()
    contact['last_name'] = elements['last_name'].title()
    contact['home_phone'] = elements['home_phone']
    members.append(contact)
    return members


def create_payload(contacts, list_id):
    payload = {'import_data': contacts,
               'lists': [list_id],
               'column_names': ['Email Address', 'First Name', 'Last Name',
                                'Home Phone', 'Address Line 1',
                                'Address Line 2', 'City', 'State',
                                'Zip/Postal Code']}
    return payload


def add_contacts(payload):
    '''POSTs a JSON payload to the Constant Contact API.

    Arguments:
        payload = The payload returned by create_payload().
    '''
    r = requests.post(url, headers=cc_headers, json=payload)
    print(r.status_code)
    print(r.reason)
    print(r.text)
    print('-------------')


for item in list_messages(headers):
    contacts = get_contact(get_message(headers, item))
    payload = create_payload(contacts, members_list_id)
    add_contacts(payload)
    # print(payload)
