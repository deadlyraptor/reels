# contact-copy

These Python scripts are used to upload customer data into a Constant Contact
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

## app.py

Copies the content from a single workbook and pastes it into two
new workbooks. Two workbooks are created because customers are
added to one of two lists, depending on what film they watched.

## cc.py

Reads the content from a single workbook, extracts the required data, and stores
it in a specially formatted JSON payload. A request POST request is then made
that adds the contacts to the relevant list in Constant Contact API.

### Required packages
```
xlrd
xlwt
requests
```
