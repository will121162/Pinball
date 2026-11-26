
#key concepts are; there's a queue to hold data once it has been flagged as changed from initial state.
#then the uart sender function takes the oldest item in the queue and sends it to the SQL server to save the game meta data
from random import randint
from SQL_functions import SQL_insert, dynamic_insert
import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


db = mysql.connector.connect( # handels server connection, table specific CRUD is handled by specific calls.
    host=os.environ['HOST'],
    port=os.environ['PORT'],
    user=os.environ['pinball_sqlun'],
    password=os.environ["pinball_sqlpw"],
    database=os.environ['DB'],
)

initialise_cursor = db.cursor()
insert_cursor = db.cursor()

class Queue:
    def __init__(self,stack):
        self.stack = stack

    def tail(self)-> dict: #for practice, pop does it smoother
        tail:dict = self.stack[0]
        self.stack.remove(tail)
        return tail

    def add(self, class_object):
        self.stack.append(class_object)

    def subtract (self):
        return self.stack.pop(0)

queue = Queue(stack=[])

class Pin:
    def __init__(self, num: int, state: bool, points: int | None, time):
        self.num = num #pin number on MC
        self.state = state # digital high or low
        self.points = points # number of points assigned to the pin (high scoring hard to get pins vs low scoring easy pins)
        self.time = time # date time of activation

mario = Pin(state=False, points=0, num=1, time=None)
peach = Pin(state=False, points=0, num=2,time=None)
luigi = Pin(state=False, points=0, num=3,time=None)
bowser = Pin(state=False, points=0, num=4,time=None)
toad = Pin(state=False, points=0, num=5,time=None)
toadette = Pin(state=False, points=0, num=6,time=None)
yoshi = Pin(state=False, points=0, num=7,time=None)
wario = Pin(state=False, points=0, num=8,time=None)

flipper_l = Pin(state=False,points=None,num=40, time=None) #it's a flipper, no points, events needed for logs
flipper_r = Pin(state=False,points=None,num=50, time=None) #it's a flipper, no points, events needed for logs

pins = [mario, peach, luigi, bowser, toad, toadette, yoshi, wario, flipper_l, flipper_r] #flippers included to confirm activation via state check

game_username = ['test_user']

rows = []
columns = f'pin_id , event_time , session_id'
db_dict = {
    'db':db,
    'columns':columns,
    'rows':rows,
}

def send_uart(rows, columns)-> None | int: #uploads data from queue to sql (replicating UART message structure to ESP)
    #SQL_insert(rows=rows,columns=columns,database=database) #old static func.
    dynamic_insert(rows=rows, columns=columns, table_name='events', cursor = insert_cursor, is_init = False)

def initialise_sql(game_username,cursor)-> int | None: #generates and returns new session_id after uploading username to the session table
    #SQL_insert(rows=game_username, columns='player_name',database='sessions')
    #session_id = cursor.fetchone() # fetches last item via cursor (auto generated session_ID) | this uses the cursor for SQL insert, need to define new cursor for initialize
    return dynamic_insert(rows=game_username, columns='player_name', table_name='sessions', cursor = cursor, is_init = True)

loop_unit = 100

session_id = initialise_sql(game_username, initialise_cursor) # need to add ability to return session_id to then upload per row to SQL, session_id is saved per void loop (session)

for i in range(loop_unit): #this is just a limited iterative loop to allow for cycling simulating the void loop in cpp
    loop_time = datetime.now()
    for pin in pins:
        if len(queue.stack) > 100: #not needed for python, needed for cpp MC integration, although it does catch possible queue pop failures
            raise Exception('runtime_stack exceeded 100 units')

        random_int = randint(1, 4)  #a simple method for randomly assigning a 1 in 4 chance
        if random_int == 1:
            pin.state = True

        if pin.state:
            pin.time = loop_time
            metrics_dict = {
                'row':[pin.num,pin.time,session_id],
                'columns':'pin_id, event_time, session_id'
            }
            queue.add(metrics_dict)#pin metrics are mutatable, need to take stamp of present values and append that, ie dict
            pin.state = False
        if len(queue.stack)>0:
            for item in range(len(queue.stack)):
                queue_data = queue.tail() #calls tail once and allows for multiple dict extracts
                row = queue_data['row']
                columns = queue_data['columns']
                send_uart(rows=row,columns=columns)

    if i == loop_unit-1: #pulls closing statistics to validate the loop works as expected. loop_unit-1 allows me to change loop frequency without changing the ith number
        for pin in pins:
            print(f'pin {pin.num} points;{pin.points}')
        print(f'queue length:{len(queue.stack)}')