import sys
import requests
import xml.etree.ElementTree as ET
import constantcontact as cc
import google
from credentials import app_key, user_key, corp_id, report_id, email
from credentials import general_list_id, members_list_id
from time import sleep

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
    google.create_message(email, email,
                          'New Constant Contact Actvitiy: No new members to \
                           add.',
                          ('There were no membership sales yesterday.\n\n'
                           '---\n'
                           'Sent by reels. Something wrong? Contact Javier.'))
    sys.exit()

# The child elements that deal with actual member data.
collection = root[1][3]
# The list of contacts passed to the Constant Contact functions.
members = []
# A helper list used to ensure only unique contacts. Constant Contact determins
# if a contact is unique by the email address.
emails = []


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

    membership['name'] = 'Custom Field 1'
    membership['value'] = collection[26].text

    members.append(contact)

for count in range(record_count):
    # In order to add unique contacts and not overwrite ones already added,
    # check that the entry has an email and it is not the same as the previous.
    if (collection[count][7].text and
       collection[count][7].text not in emails):
        emails.append(collection[count][7].text)
        append_members(collection[count])

payload = cc.create_payload(members, [general_list_id, members_list_id])
activity = cc.add_contacts(payload)
status_report = cc.get_status(activity)
cc.poll_activity(status_report)
