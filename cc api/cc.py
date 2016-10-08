import requests
from credentials import client_id, token
from credentials import test_list, general_list, after_hours_list

base_url = 'https://api.constantcontact.com/v2/activities'
endpoint = '/addcontacts?api_key='
url = base_url + endpoint + client_id

headers = {'Authorization': ('Bearer ' + token)}

d = {
    'first_name': 'Jane'
    'last_name': 'Smith',

}

adds = {
    "import_data": [{
        "email_addresses": [
            "user1@example.com"
        ],
        "first_name": "John",
        "last_name": "Smith",
        "home_phone": "5555551212",
        "addresses": [{
            "line1": "123 Partridge Lane",
            "line2": "Apt. 3",
            "city": "Anytown",
            "state_code": "NH",
            "postal_code": "02145"}]
    },
     {
        "email_addresses": [
            "user2@example.com"
        ],
        "first_name": "Jane",
        "last_name": "Doe",
        "home_phone": "5555551213",
        "addresses": [{
            "line1": "456 Jones Road",
            "city": "AnyTownShip",
            "state_code": "DE",
            "postal_code": "01234"}],
    }],
    "lists": [
        "1455741462",
    ],
    "column_names": [
        "Email Address",
        "First Name",
        "Last Name",
        "Address Line 1",
        "Address line 2",
        "City",
        "State",
        "Zip/Postal Code",
        "Home Phone",
    ]
}

# cc = requests.post(url, headers=headers, json=adds)
