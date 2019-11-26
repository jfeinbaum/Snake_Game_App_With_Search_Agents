import heapq
import time
from enum import Enum
from setup import *


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

'''
Returns the Manhattan distance between points xy1 and xy2
'''
def manhattanDistance( state ):
    xy1 = state['snake'].head.pos
    xy2 = state['food']
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )



'''
If the food is covered on 2 or more sides, count from the last segment
bordering the food until the tail is reached so the food is freed;
Returns manhattan distance minus that count
'''
def foodTrappedHeuristic( state ):
    manhattan = manhattanDistance(state)
    adjacent_positions = adjacent_to_food(state['food'])
    adjacent_segments = trapped_food(state['snake'].body, adjacent_positions)
    if len(adjacent_segments) >= 2:
        max_i = 0
        for pos, i in enumerate(state['snake'].body):
            if pos in adjacent_segments:
                if i > max_i:
                    max_i = i
        rem_segments = len(state['snake'].body[max_i:])
        return manhattan - rem_segments
    else:
        return manhattan







'''
Returns the 4 coordinates adjacent to the current food position.
'''
def adjacent_to_food( food_pos ):
    right = (food_pos[0]+1, food_pos[1])
    left = (food_pos[0]-1, food_pos[1])
    up = (food_pos[0], food_pos[1]-1)
    down = (food_pos[0], food_pos[1]+1)
    return [right, left, up, down]

'''
Returns the body segments adjacent to the food
'''
def trapped_food (body, adjacents):
    hits = []
    for adj in adjacents:
        if adj in body or out_of_bounds(adj):
            hits.append(adj)
    return hits

'''
Returns true if the given position is out of game bounds, false otherwise
'''
def out_of_bounds(pos):
    return pos[0] < 0 or pos[1] < 0 or pos[0] >= ROWS or pos[1] >= COLS

'''
Class to log information about the
'''

class Log:

    def __init__(self, algo_name, heuristic=None):
        self.algo_name = algo_name
        self.heuristic = heuristic
        self.record = []
        self.death = None
        self.start_time = None
        self.end_time = None

    def __str__(self):
        cat = ""
        cat += "Algorithm: " + self.algo_name + "\n"
        if self.heuristic:
            cat += "Heuristic: " + self.heuristic + "\n"
        total_time = 0
        score = 0
        times = []
        for i in range(len(self.record)):
            total_time += self.record[i][0]
            score = i
            times.append(str(self.record[i][0]))
        cat += "Score: " + str(score) + "\n"
        cat += "Times: " + str(times) + "\n"
        cat += "Cause of Death:  " + self.death + "\n"
        cat += "Total Time:      " + str(total_time) + " seconds\n"
        cat += "Average Time: " + str(total_time/len(self.record)) + " seconds\n"
        cat += "-" * 100 + "\n"
        return cat

    def readable_stats(self):
        cat = ""
        cat += "Algorithm: " + self.algo_name + "\n"
        if self.heuristic:
            cat += "Heuristic: " + self.heuristic + "\n"
        cat += "-------------------\n"
        total_time = 0
        for i in range(len(self.record)):
            total_time += self.record[i][0]
            cat += "Turn " + str(i + 1) + ":\n"
            cat += "\tTime:  " + str(self.record[i][0]) + "\n"
            cat += "\tScore: " + str(self.record[i][1]) + "\n"
        cat += "-------------------\n"
        cat += "Summary:\n"
        cat += "Cause of Death:  " + self.death + "\n"
        cat += "Total Time:      " + str(total_time) + " seconds\n"
        cat += "Average Time   : " + str(total_time/len(self.record)) + " seconds\n"
        cat += "\n\n" + "-" * 100 + "\n\n"
        return cat

    def start_stopwatch(self):
        self.start_time = time.clock()

    def stop_stopwatch(self):
        self.end_time = time.clock()

    def update(self, score):
        self.record.append((self.end_time - self.start_time, score))

    def terminate(self, reason):
        self.death = reason

    def save(self, filename):
        file = open(filename, 'a')
        file.write(str(self))
        file.close()
