import heapq
from enum import Enum


'''
List data structure with LIFO policy
'''
class Stack:

    def __init__(self):
        self.stack = []

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        return self.stack.pop()

    def isEmpty(self):
        return len(self.stack) == 0

'''
List data structure with FIFO policy
'''
class Queue:

    def __init__(self):
        self.queue = []

    def push(self, x):
        self.queue.insert(0, x)

    def pop(self):
        return self.queue.pop()

    def isEmpty(self):
        return len(self.queue) == 0

'''
Modified queue data structure where each item has an associated priority
'''
class PriorityQueue:

    def __init__(self):
        self.queue = []
        self.size = 0

    def push(self, x, priority):
        item = (priority, self.size, x)
        heapq.heappush(self.queue, item)
        self.size += 1

    def pop(self):
        (_, _, x) = heapq.heappop(self.queue)
        return x

    def isEmpty(self):
        return len(self.queue) == 0


class Action(Enum):
    # Also referred to as direction,
    # Up and down are inverted here to reflect the graphics on the screen
    # Use .value[0] and .value[1] to access x,y from an action enum
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    STOP = (0, 0)


