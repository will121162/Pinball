
#key concepts are; there's a queue to hold data once it has been flagged as changed from initial state.
#then the uart sender function takes the oldest item in the queue and sends it to the SQL server to save the game meta data
from random import randint
from SQL_functions import SQL_insert
import mysql.connector
import os
import datetime
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

mario = Pin(state=False, points=0, num=1, time = None)
peach = Pin(state=False, points=0, num=2,time = None)
luigi = Pin(state=False, points=0, num=3,time = None)
bowser = Pin(state=False, points=0, num=4,time = None)
toad = Pin(state=False, points=0, num=5,time = None)
toadette = Pin(state=False, points=0, num=6,time = None)
yoshi = Pin(state=False, points=0, num=7,time = None)
wario = Pin(state=False, points=0, num=8,time = None)

flipper_l = Pin(state=False,points=None,num=40, time=None) #its a flipper, no points
flipper_r = Pin(state=False,points=None,num=50, time=None) #its a flipper, no points

pins = [mario, peach, luigi, bowser, toad, toadette, yoshi, wario, flipper_l, flipper_r] #flippers included to confirm activation via state check

game_username = 'test_user'

rows = []
columns = f'pin_id , event_time'
db_dict = {
    'db':db,
    'columns':columns,
    'rows':rows,
}


def send_uart(output_dict, database_method):
    SQL_insert(rows=output_dict['row'],columns=output_dict['columns'],database=database_method)
'''
def initialise_sql(): # left for another day
    SQL_insert(rows=game_username, columns='player_name',database=None)
'''
loop_unit = 100
for i in range(loop_unit): #this is just a limited iterative loop to allow for cycling simulating the void loop in cpp
    counter = 0
    for pin in pins:
        if len(queue.stack) > 100: #not needed for python, needed for cpp MC integration, although it does catch possible queue pop failures
            raise Exception('runtime_stack exceeded 100 units')

        random_int = randint(1, 4)  #a simple method for randomly assigning a 1 in 4 chance
        if random_int == 1:
            pin.state = True

        if pin.state is True: #could simplify, left for clarity pin.state = true indicates a digital input on the pin thats defined
            pin.time = datetime.time()

            metrics_dict = {
                'row':[pin.num,pin.time],
                'columns':f'pin_id , event_time'
            }
            queue.add(metrics_dict)#pin metrics are mutatable, need to take stamp of present values and append that, ie dict
            pin.state = False
        if len(queue.stack) > 0:
            for item in range(len(queue.stack)):
                send_uart(queue.tail(),db)


    if i == loop_unit-1: #pulls closing statistics to validate the loop works as expected. loop_unit-1 allows me to change loop frequency without changing the ith number
        for pin in pins:
            print(f'pin {pin.num} points;{pin.points}\n')
        print(f'queue length:{len(queue.stack)}')