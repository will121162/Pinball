import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

database = os.environ['DB']

db = mysql.connector.connect(
    host=os.environ['HOST'],
    port=os.environ['PORT'],
    user=os.environ['pinball_sqlun'],
    password=os.environ["pinball_sqlpw"],
    database=database,
)
mycursor = db.cursor()
rows = []
'''

{
	dbname:{
		db_cols:[list],
		log_1:[X,'NS',Y],
	}
}
'''
columns = f'first_name, age, country_code, last_name, email, unique_str, is_admin'

def SQL_insert(rows,database,columns)->None:

    value_string = 'values ('
    for items in rows: #adds placeholder per item in rows
        value_string += '%s,'
    value_string = value_string[:-1] # removes final coma to maintain sql syntax
    value_string += ')'
    print(value_string,'\n===============================value string===================') # print for validation of value_string
    mycursor.executemany(
    f'insert into {database} ({columns}) ' #keeping dynamic for reuse, example below is static.
    f'{value_string}',
        rows,

        )
    db.commit()
''' static example
my_cursor.executemany(
'insert into users (first_name, age, country_code, last_name, email, unique_str, is_admin) '
    'values (%s,%s,%s,%s,%s,%s,%s)', #one per item in rows
    rows,

    )
db.commit()
'''