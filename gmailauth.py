import requests
from requests_oauthlib import OAuth2Session

from credentials import g_client_id, g_client_secret
from credentials import auth_uri, token_uri, redirect_uri, scope

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

google = OAuth2Session(g_client_id, scope=scope, redirect_uri=redirect_uri)

authorization_url, state = google.authorization_url(auth_uri,
                                                    acess_type='offline',
                                                    approval_prompts='force')

print('Please go here and authorize: ', authorization_url)

redirect_response = input('Paste the full redriect URL here: ')

google.fetch_token(token_uri, client_secret=g_client_secret,
                   authorization_response=redirect_response)
