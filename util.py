import heapq

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
        item = (priority, self.count, x)
        heapq.heappush(self.queue, item)
        self.count += 1

    def pop(self):
        (_, _, x) = heapq.heappop(self.heap)
        return x

    def isEmpty(self):
        return len(self.queue) == 0
