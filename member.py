import sys
import requests
import xml.etree.ElementTree as ET
import constantcontact as cc
from credentials import app_key, user_key, corp_id, report_id
from credentials import general_list_id, members_list_id
from time import sleep
from gmail import create_message

# Agile API parameters.
base_url = 'https://prod3.agileticketing.net/api/reporting.svc/xml/render'

params = {'appkey': app_key, 'userkey': user_key, 'corporgid': corp_id,
          'reportid': report_id, 'DatePicker': 'yesterday',
          'MembershipMultiPicker': '130', 'filename': 'memberactivity.xml'}

r = requests.get(base_url, params)
root = ET.fromstring(r.text[3:])

# In order to loop over all the members, this variable points to the number of
# members in the tree.
record_count = int(root[0].attrib['Record_Count'])

if record_count == 0:
    create_message('info@gablescinema.com', 'info@gablescinema.com',
                   'New Constant Contact Actvitiy: No new members to add.',
                   ('There were no membership sales yesterday.\n\n'
                    '---\n'
                    'Sent by reels. Something wrong? Contact Javier.'))
    sys.exit()

# The child elements that deal with actual member data.
collection = root[1][3]
members = []


def append_members(collection):
    '''Populates the contact, address, and custom fields dictionaries and then
    appends them to the members list.

    Arguments:
        collection = The element in the XML tree that contains member info.
    '''
    contact = {}
    address = {}
    membership = {}

    contact['email_addresses'] = [collection[7].text]
    contact['first_name'] = collection[2].text.title()
    contact['last_name'] = collection[4].text.title()
    contact['home_phone'] = collection[19][0].attrib['Number']

    contact['addresses'] = [address]

    address['line1'] = collection[9].text
    address['line2'] = collection[10].text
    address['city'] = collection[11].text.title()
    address['state_code'] = collection[12].text
    address['postal_code'] = collection[13].text

    contact['custom_fields'] = [membership]

    membership['name'] = 'Membership Level'
    membership['value'] = collection[26].text

    members.append(contact)

for count in range(record_count):
    if collection[count][7].text:
        append_members(collection[count])

payload = cc.create_payload(members, [general_list_id, members_list_id])
activity = cc.add_contacts(payload)
status_report = cc.poll_activity(activity)

while status_report['status'] != 'COMPLETE':
    status_report = cc.poll_activity(activity)
    sleep(5)
else:
    if status_report['error_count'] == 0:
        create_message('info@gablescinema.com', 'info@gablescinema.com',
                       'New Constant Contact Activity: {} member(s) added with \
                       no errors.'.format(status_report['contact_count']),
                       ('Added {} member(s) added.\n\n'
                        '---\n'
                        'Sent by reels. Something wrong? Contact Javier.'.format(status_report['contact_count'])))
    else:
        create_message('info@gablescinema.com', 'info@gablescinema.com',
                       'New Constant Contact Activity: {} member(s) added with \
                       {} error(s).'.format(status_report['contact_count'],
                                            status_report['error_count']),
                       ('The error(s) were: {}.\n\n'
                        '---\n'
                        'Sent by reels. Something wrong? Contact Javier.'.format(status_report['errors'])))
