import sys
import requests
import hashlib
import xml.etree.ElementTree as ET
import google
from credentials import chimp_key, chimp_list_id
from credentials import app_key, user_key, corp_id, report_id, info

'''
The workflow for subscribing a person to the MailChimp list is:

1. Authenticate using API
2. Generate MD5 hash of lowercase version of email address.
3. Check if email address is subscribed using MD5 hash.
4. If subscribed, unsubscribed or cleaned, do not add the email.
5. If none of the above, add the email and other relevant info.
6. Add a note to the subscriber with the date of purchase, membership level,
and whether it was a renewal or not.
'''

url = 'https://us14.api.mailchimp.com/3.0'
endpoints = ['/lists/{0}/members/{1}']


def mailchimp(endpoint):
    '''Authenticates using HTTP Basic.

    Arguments:
        none (eventually it should be the key)

    Returns:
        none
    '''
    r = requests.get(url, auth=('reels', chimp_key))


def hash(email):
    '''Generates MD5 hash of the lowercase version of an email address.

    Arguments:
        email = The email address to be checked.

    Returns:
        secure_hash = The hash of the email.
    '''
    secure_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return secure_hash


def check_subscription(email):
    '''Returns the subscription status of the email address set to be subscribed.

    Arguments:
        email = The email address to be checked.

    Returns:
        status = The subscription status of the email address.
    '''
    endpoint = '/lists/{0}/members/{1}'.format(chimp_list_id, hash(email))
    r = requests.get(url + endpoint, auth=('reels', chimp_key))
    if r.status_code == 404:
        print('The subscriber isn\'t on the list.')
        subscribe_address(generate_payload(collection[count]))
    elif r.status_code == 200:
        print('The subscriber is {0}.'.format(r.json()['status']))


def subscribe_address(payload):
    '''Subscribes an email to a list.

    Arguments:
        payload = The JSON dictionary containing subscriber information.
    '''
    endpoint = '/lists/{0}/members/'.format(chimp_list_id)
    r = requests.post(url + endpoint, auth=('reels', chimp_key), json=payload)


def add_note(email):
    endpoint = '/lists/{0}/members/{1}/notes'.format(chimp_list_id,
                                                     hash(email))
    if collection[count][29].text == 'Y':
        renewal_status = 'Renewed'
    else:
        renewal_status = 'Purchased'
    note = {'note': '{0} {1} membership on {2}.'.format(
                                            collection[count][26].text,
                                            collection[count][41].text[:10],
                                            renewal_status)}
    r = requests.post(url + endpoint, auth=('reels', chimp_key), json=note)
    print(r.json())
# Agile API parameters.


base_url = 'https://prod3.agileticketing.net/api/reporting.svc/xml/render'

params = {'appkey': app_key, 'userkey': user_key, 'corporgid': corp_id,
          'reportid': report_id, 'DatePicker': 'thisweek',
          'MembershipMultiPicker': '130', 'filename': 'memberactivity.xml'}

r = requests.get(base_url, params)
root = ET.fromstring(r.text[3:])

# In order to loop over all the members, this variable points to the number of
# members in the tree.

record_count = int(root[0].attrib['Record_Count'])

if record_count == 0:
    google.create_message(info, info,
                          'reels: No new members to subscribe.',
                          ('There were no membership sales yesterday.\n\n'
                           '---\n'
                           'Sent by reels. Something wrong? Contact Javier.'))
    sys.exit()

# The child elements that deal with actual member data.
collection = root[1][3]

# A helper list used to ensure only unique contacts are added.
emails = []


def generate_payload(collection):
    '''Populates the JSON schema required by the MailChimp API to subscribe new
    contacts to a list. The schema takes the following form:

    'email_address': 'email',
    'status': 'subscribed',
    'merge_fields': {
    'FNAME': 'first name',
    'LNAME': 'last name',
    'PHONE': 'phone',
    'ADDRESS': {
        'addr1': 'address 1',
        'addr2': 'address 2',
        'city': 'city',
        'state': 'state',
        'zip': 'zip code',
        'country': 'USA'
        }
    }

    Arguments:
        collection = The element in the XML tree that contains member info.

    Returns:
        subscriber = A dictionary containing the subscriber info.
    '''
    # MailChimp does not accept None in any field so this if-else replaces an
    # instance of None in the address 2 field with an empty string.
    if collection[10].text is None:
        addr2 = ''
    else:
        addr2 = collection[10].text

    # Same as above but instead for phone numbers.
    if collection[19][0].attrib['Number'] is None:
        phone = ''
    else:
        phone = collection[19][0].attrib['Number']

    payload = {'email_address': collection[7].text,
               'status': 'subscribed',
               'merge_fields': {
                    'FNAME': collection[2].text.title(),
                    'LNAME': collection[4].text.title(),
                    'PHONE': phone,
                    'ADDRESS': {
                        'addr1': collection[9].text,
                        'addr2': addr2,
                        'city': collection[11].text,
                        'state': collection[12].text,
                        'zip': collection[13].text,
                        'country': 'USA'
                        }
                    }}
    return payload


for count in range(record_count):
    # In order to add unique contacts not overwrite ones already subscribed,
    # check that the entry has an email and it is not the same as the previous.
    if (collection[count][7].text and collection[count][7].text not in emails):
        emails.append(collection[count][7].text)
        check_subscription(collection[count][7].text)
        add_note(collection[count][7].text)
