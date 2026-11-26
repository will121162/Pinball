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
insert_cursor = db.cursor()

initialise_cursor = db.cursor()
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

def SQL_insert(rows,database,columns)->None: # might delete and refactor to use dynamic insert

    value_string = 'values ('
    column_split_list = columns.split()
    for items in column_split_list: #adds placeholder per item in columns
        value_string += '%s,'
    value_string = value_string[:-1] # removes final coma to maintain sql syntax
    value_string += ')'
    print(value_string,'\n===============================value string===================') # print for validation of value_string
    insert_cursor.execute(
    f'insert into {database} ({columns}) ' #keeping dynamic for reuse, example below is static.
    f'{value_string}',
        rows,
        )
    db.commit()


def initialise_insert(rows,database,columns)-> None: #now not needed, might delete but left for clarity over thinking
    value_string = 'values ('
    column_split_list = columns.split()
    for items in column_split_list:  # adds placeholder per item in columns
        value_string += '%s,'
    value_string = value_string[:-1]  # removes final coma to maintain sql syntax
    value_string += ')'
    print(value_string,
          '\n===============================value string===================')  # print for validation of value_string
    initialise_cursor.execute(
        f'insert into {database} ({columns}) '  # keeping dynamic for reuse, example below is static.
        f'{value_string}',
        rows,
    )
    db.commit()


def dynamic_insert(rows, columns, table_name, cursor, is_init:bool = False)-> int | None: #did not consider issues with cursor in last functions, thus made cursor static, now using dynamic cursor for greater dynamism
    value_string = 'values ('
    column_split_list = columns.split()
    for items in column_split_list:  # adds placeholder per item in columns
        value_string += '%s,'
    value_string = value_string[:-1]  # removes final coma to maintain sql syntax
    value_string += ')'
    cursor.execute( # cursor is inputted as to keep unique, allows for concurrent read writes of session ID while returning session specific session IDs
        f'insert into {table_name} ({columns}) '  # keeping dynamic for reuse, example below is static.
        f'{value_string}',
        rows,
    )

    db.commit()

    if is_init:
        return cursor.lastrowid
''' 
static example
my_cursor.executemany(
'insert into users (first_name, age, country_code, last_name, email, unique_str, is_admin) '
    'values (%s,%s,%s,%s,%s,%s,%s)', #one per item in rows
    rows,

    )
db.commit()
'''