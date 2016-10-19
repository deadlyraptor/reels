import requests
from bs4 import BeautifulSoup
from credentials import url1, url2

# r = requests.get(url1)
soup = BeautifulSoup(open('member1.html'), 'html.parser')

style = 'word-wrap:break-word;white-space:pre-wrap;font-style:normal;' + \
        'font-family:Arial;font-size:8pt;font-weight:400;text-decoration:none;' + \
        'unicode-bidi:normal;color:Black;direction:ltr;layout-flow:horizontal;' + \
        'writing-mode:lr-tb;vertical-align:top;text-align:left;'

# div_contents = (soup.find_all('div', style=style))
# div_contents.next
div_contents = soup.find_all(text=True)
name = div_contents[33]
address_one = div_contents[35]
email = div_contents[36]
address_two = div_contents[37]
city = address_two[:5]
state = address_two[-9:-7]
zip_code = address_two[-5:]
home_phone = div_contents[38]

membership = div_contents[57]
print(membership)
print(name)
print(email[7:])
print(home_phone[7:])
print(address_one)
print(city)
print(state)
print(zip_code)
