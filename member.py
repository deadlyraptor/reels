import requests
from credentials import label_id
from gmailauth import refresh

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
        # return messages
        message_ids = []
        for item in messages:
            message_ids.append(item['id'])
        return message_ids

print(list_messages(headers))


def get_message(headers, identity):
    params = {'id': identity, format: 'metadata'}
    r = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages/id',
                     headers=headers, params=params)
    j = r.json()
    print(r.status_code, r.reason)
    h = j['payload']
    subject = ''
    for header in h['headers']:
        if header['name'] == 'Subject':
            subject = header['value']
            break
    print(subject)

for item in list_messages(headers):
    get_message(headers, item)

# get_message(headers, list_messages(headers))
