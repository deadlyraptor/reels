import sys
import requests
import xml.etree.ElementTree as ET
import constantcontact as cc
from time import sleep
from credentials import app_key, user_key, corp_id, report_id, test_list_id

# Agile URL is unwieldy and can only be built by joining all the strings.
base_url = 'https://prod3.agileticketing.net/api/reporting.svc/xml/render'
date = '&DatePicker=yesterday'
report = '&MembershipMultiPicker=130&filename=memberactivity.xml'

url = '{}{}{}{}{}{}{}'.format(base_url, app_key, user_key, corp_id, report_id,
                              date, report)
# r = requests.get(url)
# root = ET.fromstring(r.text[3:])

tree = ET.parse('test.xml')
root = tree.getroot()

# In order to loop over all the members, this variable points to the number of
# members in the tree.
record_count = int(root[0].attrib['Record_Count'])

if record_count == 0:
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

payload = cc.create_payload(members, test_list_id)
activity = cc.add_contacts(payload)
status_report = cc.poll_activity(activity)

status = ['COMPLETE', 'ERROR']
while status_report['status'] not in status:
    print('The while loop status is: {}'.format(status_report['status']))
    print('Polling...')
    status_report = cc.poll_activity(activity)
    sleep(5)
else:
    print('Finished!')
    print('The finished status is: {}'.format(status_report['status']))
