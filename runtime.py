#I've not shared the readme yet - will write soon
#this is a loose structure and not intended to work
#key concepts are; there's a queue to hold data once it has been flagged as changed from initial state.
#then the uart sender function takes the oldest item in the queue and sends it off
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
    user=os.environ['SQL_USR_NAME'],
    password=os.environ["SQL_PW"],
    database=database,
)
mycursor = db.cursor()

rows =[]
columns =[]
db_dict = {
    'db':db,
    'columns':columns,
    'rows':rows,
}

class Queue:
    def __init__(self,stack:list):
        self.stack = stack

    def tail(self): #for practice, pop does it smoother
        tail = self.stack[0]
        self.stack.remove(tail)
        return tail

    def add(self, class_object):
        self.stack.append(class_object)

    def subtract (self):
        return self.stack.pop(0)
queue = Queue(stack=[])

class Pin:
    def __init__(self,num: int, state: bool, points: int, time):
        self.num = num
        self.state = state
        self.points = points
        self.time = time

mario = Pin(state=False, points=0, num=1, time = None)
peach = Pin(state=False, points=0, num=2,time = None)
luigi = Pin(state=False, points=0, num=3,time = None)
bowser = Pin(state=False, points=0, num=4,time = None)
toad = Pin(state=False, points=0, num=5,time = None)
toadette = Pin(state=False, points=0, num=6,time = None)
yoshi = Pin(state=False, points=0, num=7,time = None)
wario = Pin(state=False, points=0, num=8,time = None)
pins = [mario, peach, luigi, bowser, toad, toadette, yoshi, wario]

print(mario.state == False)
def send_uart(metrics_dict):
    print(f'data from pin {metrics_dict} sent via uart')
    SQL_insert(db_dict['rows'],db_dict['db'], db_dict['columns'])
    #SQL_insert()
    #SQL table set up with time of upload for instances, this would not be sufficient for final implementation as for game accurate event recording momentary detection is required

for i in range(1000): #this is just a limited iterative loop to allow for cycling simulating the void loop in cpp
    #within the next update I shall add random flips to the pin.state values as to replicate a digital high signal in the MC
    counter = 0
    for pin in pins:
        metrics_dict = {
            'pin_num':pin.num,
            'pin_state':pin.state,
            'pin_points':pin.points,
            'pin_time':pin.time
        }
        if len(queue.stack) > 100: #not needed for python, needed for cpp MC integration, although it does catch possible queue pop failures
            raise Exception('runtime_stack exceeded 100 units')

        random_int = randint(1, 4)  #a simple method for randomly assigning a 1 in 4 chance
        if random_int == 1:
            pin.state = True

        if pin.state is True: #could simplify, left for clarity pin.state = true indicates a digital input on the pin thats defined
            pin.points += 1
            pin.time = datetime.datetime.now()
            pin.state = False
            metrics_dict['pin_points'] = pin.points #pin.points represents number of digital signals received from that node.
            metrics_dict['pin_time'] = pin.time
            metrics_dict['pin_num'] = pin.num
            queue.add(metrics_dict)#pin metrics are mutatable, need to take stamp of present values and append that, ie dict

        if len(queue.stack) > 10:
            for item in range(len(queue.stack)):
                send_uart(queue.subtract())
                counter += 1
                print(f'{counter}')

    if i == 999: #pulls closing statistics to validate the loop works as expected
        for pin in pins:
            print(f'pin {pin.num} points;{pin.points}\n')
        print(f'queue length:{len(queue.stack)}')