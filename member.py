import requests
from base64 import urlsafe_b64decode
from credentials import label_id, url1, url2
from gmailauth import refresh

# access_token = refresh()
headers = {'Authorization': ('Bearer ' + access_token)}


def list_messages(headers):
        params = {'labelIds': label_id, 'q': 'newer_than:2d'}
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


def get_message(headers, identity):
    params = {'id': identity, 'format': 'raw'}
    r = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages/id',
                     headers=headers, params=params)
    j = r.json()
    raw = j['raw']
    d = urlsafe_b64decode(raw)
    p = d.decode()
    s = p.find('https')
    l = len(p)
    print(p[s:l])
    print('----------')
    return(p[s:l])

# for item in list_messages(headers):
#     get_message(headers, item)
