import requests
import xml.etree.ElementTree as ET
from credentials import app_key, user_key, corp_id, report_id

base_url = 'https://prod3.agileticketing.net/api/reporting.svc/xml/render'
date = '&DatePicker=thisweek'
report = '&MembershipMultiPicker=130&filename=memberactivity.xml'

url = '{}{}{}{}{}{}{}'.format(base_url, app_key, user_key, corp_id, report_id,
                              date, report)
# r = requests.get(url)
# text = r.text
# xml = text[3:]
# root = ET.fromstring(xml)

tree = ET.parse('data.xml')
root = tree.getroot()

members = root[1]
collection = members[3]
summary = root[0].attrib
record_count = int(summary['Record_Count'])

members = []


def append_contacts(collection):
    '''Populates the contact and address dictionaries and then appends them to
    a contacts list.

    Arguments:
        contacts = The list the dictionary will be appended to.
    '''
    contact = {}
    address = {}

    contact['email_addresses'] = [collection[7].text]
    contact['first_name'] = collection[2].text.title()
    contact['last_name'] = collection[4].text.title()
    contact['home_phone'] = collection[19][0].attrib
    contact['custom_field 1'] = collection[26].text

    contact['addresses'] = [address]

    address['line1'] = collection[9].text
    address['line2'] = collection[10].text
    address['city'] = collection[11].text.title()
    address['state_code'] = collection[12].text
    address['postal_code'] = collection[13].text

    members.append(contact)

for count in range(record_count):
    append_contacts(collection[count])

print(members)
