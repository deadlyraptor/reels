# reels

This repository contains an assortment of Python scripts used to automate various tasks at the Coral Gables Art Cinema.

It consists of the following:

1. Scripts - files meant to be run by users double-clicking the icon on a Windows (or Linux) environment.
2. Modules - support files with functions used by multiple scripts.

## Scripts

* **cc_spreadsheet** - Copies the relevant customer contact information from a spreadsheet and writes it to two new spreadsheets depending on which film a customer purchased tickets for. All spreadsheets must be in .xls format.

* **cc_upload** - Same as above except instead of writing to a spreadsheet, it adds the contacts directly to Constant Contact using its API.

* **member** - Parses an XML file with sales information for memberships sold on a given date by making a request to the Agile reporting API and adding the contacts directly to Constant Contact via its API.

* **photos** - Renames all of the photo files of extensions .jpg, .jpeg, and .png to a new name input by the user but appended with a number, e.g., file name 1, file name 2, etc.

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
10. Membership level (if applicable)

## Modules

* **constantcontact** - Handles all Constant Contact API calls as well as any work needed to prepare data for upload.

* **gmail** - Handles all Gmail API calls, including user authorization, creating messages, and sending messages.

## Setup

Since these scripts are only meant to be run by directly calling them via clicking the icon or calling them from the command line, there's no installation required. The source files can be downloaded and run almost immediately.

A credentials file that contains API keys, tokens, and other sensitive information is required for the modules to work.

### Required packages
```
requests
requests_oauthlib
xlrd
xlwt
```

## Acknowledgements
A big thanks to [jmr0](https://github.com/jmr0) for his continuing patience and enthusiasm in teaching me the ins and outs of programming.
