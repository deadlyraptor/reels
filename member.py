import requests
from base64 import urlsafe_b64decode
from credentials import label_id, url1, url2, members_list_id, test_list_id
from credentials import token, client_id
from gmailauth import refresh
import email

# Constant Contact API.
base_url = 'https://api.constantcontact.com/v2/activities'
endpoint = '/addcontacts?api_key='
url = base_url + endpoint + client_id
cc_headers = {'Authorization': ('Bearer ' + token)}

access_token = refresh()

headers = {'Authorization': ('Bearer ' + access_token)}


def list_messages(headers):
        params = {'labelIds': label_id, 'q': 'newer_than:2d'}
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
    msg = email.message_from_string(string)
    return msg


def get_contact(msg):
    msg_string = msg.get_payload()
    ls = msg_string.split()
    delimiter = '='

    first_name = ls[22]
    delimiter_index = first_name.find(delimiter)
    first_name = first_name[:delimiter_index]

    last_name = ls[23]
    delimiter_index = last_name.find(delimiter)
    last_name = last_name[:delimiter_index]

    email_address = ls[24]
    delimiter_index = email_address.find(delimiter)
    email_address = email_address[:delimiter_index]

    home_phone = ls[25]
    delimiter_index = home_phone.find(delimiter)
    home_phone = home_phone[:delimiter_index]

    members = []
    contact = {}
    contact['email_addresses'] = [email_address]
    contact['first_name'] = first_name.title()
    contact['last_name'] = last_name.title()
    contact['home_phone'] = home_phone
    members.append(contact)
    return members


def create_payload(contacts, list_id):
    payload = {'import_data': contacts,
               'lists': [list_id],
               'column_names': ['Email Address', 'First Name',
                                'Last Name', 'Home Phone']}
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
    payload = create_payload(contacts, test_list_id)
    add_contacts(payload)
