# reels

This suite of Python scripts are used to automate various tasks at the Coral Gables Art Cinema.

upload customer data into a Constant Contact
database by reading from an Excel workbook formatted as .xls.

The customer data collected includes:

1. First name
2. Last name
3. Email
4. Address 1
5. Address 2
6. City
7. State
8. Zip
9. Phone number

## cc_spreadsheet

Reads the customer contact information from a single workbook and writes it to
one of two new workbooks, depending on which film the customer purchased tickets for.

*the spreadsheets must be in .xls format*

## cc_upload

Reads the customer contact information from a single workbook, stores it into one
of two JSON payloads, and adds the contacts to one of two lists in Contact Contact via
a POST request. The payload and list the contact is added to is dependent on the
film for which he or she purchased tickets.

*the spreadsheets must be in .xls format*

## member

Extracts the contact information for new members stored in the body of an email confirming new member activity and stores it in a JSON payload. This payload is uploaded to Constant Contact via a POST request.

### Required packages
```
requests
requests_oauthlib
xlrd
xlwt
```
