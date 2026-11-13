

class Node:
    def __init__(self,pin:int,score:int,logs:dict):
        self.logs = {
            'sensor':None,
            'game_time':None,
            'score':None,
            'updated':False
        }
        self.score = 0
        self.pin = None

'''
class nodes are named after mario characters for fun, they represent a node on the playing field, 
where an input will trigger a physical event, such as a solenoid firing, or nothing such as bobble head
style node where the ball will just trigger a point execution via limit switch or prehaps hall effect switch



'''

mushroom = Node

mushroom.pin = 1
mushroom.score = 0
#mushroom.logs['score'] = mushroom.score
#mushroom.logs['sensor'] = mushroom.pin
#^ dont want to put objects in objects

bowser = Node
bowser.pin = 2
bowser.score = 0


game_logs:list = []

game_status:bool = False

while game_status:
    if Node.logs['updated'] is True:
        game_logs.append(Node.logs)
        Node.logs['updated'] = False

while not game_status:

    pass