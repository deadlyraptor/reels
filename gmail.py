import os
import requests
from requests_oauthlib import OAuth2Session
from credentials import g_client_id, g_client_secret, refresh_token
from email.mime.text import MIMEText

auth_uri = 'https://accounts.google.com/o/oauth2/auth'
token_uri = 'https://accounts.google.com/o/oauth2/token'
redirect_uri = 'http://localhost'
scope = ['https://www.googleapis.com/auth/gmail.compose']


def gmail_auth():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    google = OAuth2Session(g_client_id, scope=scope, redirect_uri=redirect_uri)

    authorization_url, state = google.authorization_url(auth_uri,
                                                        access_type='offline',
                                                        approval_prompts='force')

    print('Please go here and authorize: ', authorization_url)

    redirect_response = input('Paste the full redriect URL here: ')

    tokens = google.fetch_token(token_uri, client_secret=g_client_secret,
                                authorization_response=redirect_response)


def refresh():
    fields = {'grant_type': 'refresh_token', 'client_id': g_client_id,
              'client_secret': g_client_secret, 'refresh_token': refresh_token}
    r = requests.post(token_uri, data=fields)
    token = r.json()
    access_token = token['access_token']
    return access_token


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    send_message(message.as_string().encode())


def send_message(message):
    url = 'https://www.googleapis.com/upload/gmail/v1/users/me/messages/send'
    headers = {'Authorization': ('Bearer ' + refresh()),
               'Content-Type': 'message/rfc822'}
    params = {'uploadType': 'media'}

    r = requests.post(url, headers=headers, params=params, data=msg)
