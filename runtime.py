#I've not shared the readme yet - will write soon
#this is a loose structure and not intended to work
#key concepts are; there's a queue to hold data once it has been flagged as changed from initial state.
#then the uart sender function takes the oldest item in the queue and sends it off
from random import randint
from SQL_functions import SQL_insert
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

class Queue:
    def __init__(self,stack:list):
        self.stack = []

    def tail(self):
        tail = self.stack[-1]
        self.stack.remove(tail)
        return tail

    def add(self, class_object):
        self.stack.append(class_object)

    def subtract (self):
        return self.stack.pop(0)

runtime_stack = Queue()

class Pin:
    def __init__(self,num: int, state: bool, points: int):
        self.num = 0
        self.state = False
        self.points = 0

mario = Pin(state=False, points=0, num=1)
peach = Pin(state=False, points=0, num=2)
luigi = Pin(state=False, points=0, num=3)
bowser = Pin(state=False, points=0, num=4)
pins = [mario, peach, luigi, bowser]

print(mario.state == False)
def send_uart(queue_tail):
    print(f'data from pin {queue_tail.num} sent via uart')
    #SQL_insert(rows, database, columns)
    #SQL_insert()

for i in range(1000): #this is just a limited iterative loop to allow for cycling simulating the void loop in cpp
    #within the next update I shall add random flips to the pin.state values as to replciate a digital high signal in the MC
    counter = 0
    for pin in pins:
        random_int = randint(1, 4)  #a simple method for randomly assigning a 1 in 4 chance
        if random_int == 1:
            pin.state = True
        if pin.state is True: #could simplify, left for clarity pin.state = true indicates a digital input on the pin thats defined
            pin.points += 1 #pin.points represents number of digital signals received from that node.
            pin.state = False
            runtime_stack.add(pin)

        if len(runtime_stack.stack) > 1:
            send_uart(runtime_stack.subtract())
            counter += 1
            print(counter)

