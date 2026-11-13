

class Node:
    def __init__(self,pin:int,score:int,logs:dict):
        self.logs = {
            'sensor':None,
            'game_time':None,
            'score':None
        }
        self.score = 0
        self.pin = None


mushroom = Node

mushroom.pin = 1
mushroom.score = 0
mushroom.logs['score'] = mushroom.score

bowser = Node
bowser.pin = 2
bowser.score = 0

