# Automatic Cleaning, Visualizing, Storing & Mailing System

The Auto-CVSM System takes company messaging data in .xlsx format and processes them in bulk. After cleaning, visualizing, and storing them in a database, the visuals are sent to the client.
The process is completely automated.

## OVERVIEW

The program is coded entirely in Python 3.11.9, using mainly *pandas, matplotlib, sqlalchemy and smtplib*. See **VERSIONS.txt** for an extended list of library versions. There are two directories of interest; *input* and *output*, where the original excel files and the cleaned excel files & data plots are stored respectively.

### Cleaning

The {file_name}.xlsx files are imported from inside the *input* directory, and each excel is cleaned and saved as it loops through the directory. (The original excel files are NOT modified, new cleaned versions are created instead.)
The program follows the standard data cleaning process, getting rid of rows with incorrect or empty values, making sure the date is stored in proper format.
There is an additional fix that renames the *'msgs_count'* row, in case it's written as *'minimata'*, to ensure consistency across all tables.
Add any other cleaning methods you see fit for your own data.
Once cleaning is finished, the total rows deleted will be mentioned.

### Visualizing

Plots are created to visualize the data. The three plots show the following information:

1. **Bar plot:** The number of messages according to their state (seen or delivered).
2. **Area plot:** Daily messages sent according for each date recorded.
3. **Box plot:** The number of messages according to the day of the week they're sent.

### Exporting

A directory was created prior to the cleaning process, named after the excel file name.
The clean excel and plots are all exported inside their dedicated folder. These folders are stored in the output directory.

### Storing

An SQL database is created on MySQL Workbench, once again named after the file name, with the table *'messages'* in each one.

### Mailing

The visualized data are then sent to the client. The e-mail consists of three attachments that contain the plots, and a message that can be customized in the msg_txt variable. There is an additional mail function with just text that is not used in the system.

### Expected Output

For every file **{file_name}.xlsx**, the system exports should be the following:

> INSIDE *output DIRECTORY*

- *DIRECTORY* {file_name}_folder

> INSIDE *{file_name}_folder*

- clean_{file_name}.xlsx
- clean_{file_name}_plotArea.png
- clean_{file_name}_plotBar.png
- clean_{file_name}_plotBox.png

> INSIDE *SQL ENVIRONMENT*

- *DATABASE* {file_name}_db
- *TABLE* messages

## FILES

- To store all the confidential information needed, create a **passkeys.py** file with the following variables:

```python
input_dir = 'your_input_directory'
output_dir = 'your_output_directory' # where the additional directories will be stored

user = 'your_user'
password = 'your_password'
host = 'your_host'

# sender email info
email = 'your_email'
epass = 'your_email_password'

# receiver email directory
client_emails = {
    'HopOn1':'email@one.com',
    'pigeon':'email@two.com',
    'sparrow':'email@three.com',
    'YesStore':'email@four.com'
}
```

**Passkeys** is imported as **pk** on all files. Make sure to replace all the values with your own. Client emails is a directory with key as the file name and value as the receiver email for testing purposes. Ways to receive receiver email addresses and the input excel files themselves will vary.

Alternatively, if you don't want to use an imported .py file, you can store the information as environment variables using *python-dotenv*.

- The *input* directory contains sample .xlsx files compatible with the cleaning process. We're assuming all client data is stored using the template they were provided. Some files have been changed in ways that are accounted for.

- The file **connection.py** contains functions to create the database. This is done using *SQLAlchemy*, but there is an additonal function containing a method with mysql connector. Opt for using *create_database_Alchemy()* instead.

- The file **mail.py** has the functions required to send the mails. There are two mailing functions, one for text only, and one for text with image attachments. Change the text content as desired.

- The file **plotting.py** has the three plot functions that are combined in the main plot function in **auto.py**.
