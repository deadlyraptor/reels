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
collections = members[3]
details = collections[0]

first_name = details[2].text
# print(first_name)

for name in root.iter('{Membership_MemberList_Extract}FirstName'):
    print(name.text)

for name in root.iter():
    print(name.tag)
