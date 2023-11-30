# Install following library's

pip install zipfile
pip install requests
pip install sqlalchemy 

# Note I have used mysql sql server in background so please install the connector you wanted
pip install mysql-connector-python


# Search for Database Credentials and replace following credentials with what you have 
# in code.py file
database_username = 'root'
database_password = ''
database_host = 'localhost'
database_port = '3306'
database_name = 'cricket_data'


# I have created the cricket_data as schema. You can use following command to create database.
create database cricket_data;


# I have base URL where I have taken the ODI cup data, You can take the once which you wanted, By replacing in following Base URL in code.py file
base_url = "https://cricsheet.org/downloads/rlc_json.zip"


# Execute the query to get the output.
