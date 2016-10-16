import requests
from credentials import label_id
from gmailauth import refresh

access_token = refresh()
headers = {'Authorization': ('Bearer ' + access_token)}


def list_messages(headers):
        params = {'labelIds': label_id, 'q': 'newer_than:2d'}
        r = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages',
                         headers=headers, params=params)

        j = r.json()
        print(j)
        messages = []
        if 'messages' in j:
            messages.extend(j['messages'])
        return messages

print(get_messages(headers))

message_id = '157c86f6b45c2040'


def get_message(headers, identity):
    params = {'id': identity, }
    r = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages',
                     headers=headers, params=)


{'messages': [{'threadId': 'hash1', 'id': 'hash2'}],
'resultSizeEstimate': 1}
