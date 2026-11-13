import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

database = os.environ['DB']

db = mysql.connector.connect(
    host=os.environ['HOST'],
    port=os.environ['PORT'],
    user=os.environ['SQL_USR_NAME'],
    password=os.environ["SQL_PW"],
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
    mycursor.executemany(
    f'insert into {database} ({columns}) '
        'values (%s,%s,%s,%s,%s,%s,%s)',
        rows,

        )
    db.commit()
