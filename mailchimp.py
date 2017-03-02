import requests
import hashlib
from credentials import chimp_key, chimp_list_id, emails

'''
The workflow for subscribing a person to the MailChimp list is:

1. Authenticate using API
2. Generate MD5 hash of email address
3. Check if email address is subscribed using MD5 hash.
4. If subscribed, unsubscribed or cleaned, do not add the email.
5. If none of the above, add the email and other relevant info.
'''

url = 'https://us14.api.mailchimp.com/3.0'


def mailchimp():
    '''Authenticates using HTTP Basic.

    Arguments:
        none (eventually it should be the key)

    Returns:
        none
    '''
    r = requests.get(url, auth=('javier', chimp_key))


def hash(email):
    '''Generates MD5 hash of the lowercase version of an email address.

    Arguments:
        email = The email address to be checked.

    Returns:
        secure_hash = The hash of the email.
    '''
    secure_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    return secure_hash


def check_email(email):
    '''Returns the subscription status of the email address set to be subscribed.

    Arguments:
        email = The email address to be checked.

    Returns:
        status = The subscription status of the email address.
    '''
    endpoint = '/lists/{0}/members/{1}'.format(chimp_list_id, hash(email))
    r = requests.get(url + endpoint, auth=('javier', chimp_key))
    if r.status_code == 404:
        print('The subscriber isn\'t on the list.')
    elif r.status_code == 200:
        print('The subscriber is {0}.'.format(r.json()['status']))


check_email(emails[0])
