import requests
from credentials import label_id, access_token

headers = {'Authorization': ('Bearer ' + access_token)}

params = {'labelIds': label_id, 'q': 'newer_than:2d'}

r = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages',
                 headers=headers, params=params)

print(r.status_code)
print(r.reason)
print(r.content)

messages = []
if 'messages' in r:
    messages.extend(r['messages'])

print(messages)
