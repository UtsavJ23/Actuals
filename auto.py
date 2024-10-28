import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from sqlalchemy import create_engine
import datetime
import os

os.chdir("/Users/utsavjha/Coding/Python/Actuals")

# 1. Authenticate with Google Sheets API using credentials.json
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/utsavjha/Coding/Python/Actuals/credentials.json", scope)
client = gspread.authorize(creds)

# 2. Open the Google Spreadsheet
spreadsheet = client.open("DataSheet")

# 3. Access Sheet 1 and get data
sheet1 = spreadsheet.worksheet("Sheet1")
data = sheet1.get_all_values()

# 4. Access Sheet 2 and paste data
sheet2 = spreadsheet.worksheet("Sheet2")
sheet2.clear()
sheet2.insert_rows(data, row=1)

print("Data successfully copied from Sheet 1 to Sheet 2")

# 5. Send data to a local PostgreSQL database
df = pd.DataFrame(data[1:], columns=data[0])

# Database connection details - update these with your PostgreSQL credentials
engine = create_engine('postgresql+psycopg2://admin:adminstrator@localhost:5432/my_database')

# Insert data into PostgreSQL table (replace 'your_table_name' with your actual table name)
df.to_sql('data_sheet', con=engine, if_exists='replace', index=False)
print("Data sent to PostgreSQL at", datetime.datetime.now())