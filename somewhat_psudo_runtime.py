#i've not shared the readme yet - will write soon
#this is a loose structure and not intended to work
#key consepts are; theres a queue to hold data once it has been flagged as changed from inital state.
#then the uart sender function takes the oldest item in the queue and sends it off

class stack:
    def __init__(stack: list):
        self.stack = []

    def head(self):
        return self.stack[0::]

    def tail(self):
        return self.stack[::-1]

    def add(self, object):
        self.stack.append(object)

    def subtract(self):
        tail = self.stack[::-1]
        self.stack.
        del [::-1]

stack = stack()

class pin:
    def __init__(num: int, state: bool, points: int):
        self.num = None
        self.state = False
        self.points = 0
pins = []

def send_uart(pin):
    # sends data via uart to ESP
    pass

for pin in pins:
    if pin.state is True:
        pin.points += 1
        pin.state = False
        stack.head(pin)
    if len(stack) > 0:
        send_uart(stack.tail)
