import util
from setup import *
import random


'''
Searchest the deepest nodes in the search tree first
Input: search problem
Returns: search path, a sequence of actions
'''
def dfs(problem, heuristic=None):
    # Initialize problem, pushing first node to frontier
    initial_node = (problem.get_start_state(), [])
    frontier = util.Stack()
    frontier.push(initial_node)
    explored = []

    while not frontier.isEmpty():
        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        explored.append(current_node_state)

        if problem.is_goal_state(current_node_state):
            return current_node_path

        for successor in problem.get_successors(current_node_state):
            action = successor[1]
            next_state = successor[0]

            if next_state not in explored:

                # Check if the frontier contains a node with the nextState
                # If so, remove from the frontier
                # Maintain temp stack to hold items popped from frontier
                # Push items from temp stack back onto frontier
                
                temp_stack = util.Stack()
                while not frontier.isEmpty():
                    current = frontier.pop()
                    #if current[0] == next_state:
                    if current[0]['snake'].head.pos == next_state['snake'].head.pos:
                        break
                    temp_stack.push(current)
                while not temp_stack.isEmpty():
                    frontier.push(temp_stack.pop())

                frontier.push((next_state, current_node_path + [action]))


def dls(problem, heuristic=None):
    cutoff = ROWS + COLS
    initial_node = (problem.get_start_state(), [])
    frontier = util.Stack()
    frontier.push(initial_node)
    explored = []
    # Memory of the last valid node for the cutoff return
    most_recent_node = initial_node
    while True:
        # Fail if frontier is empty
        if frontier.isEmpty():
            print("DFS cutoff was reached.")
            try:
                successor_list = problem.get_better_successors(most_recent_node[0])
                actions = []
                for successor in successor_list:
                    actions.append(successor[1])
                return [random.choice(actions)]
            except IndexError:
                # Arbitrarily return left if get better successors was an empty list
                return [util.Action.LEFT]
        # Remove the last node from the frontier
        current_node = frontier.pop()
        most_recent_node = current_node
        # Add that node to the explored set
        explored.append(current_node[0]['snake'].head.pos)
        # Check if the goal state has been reached, if so return path
        if problem.is_goal_state(current_node[0]) is True:
            # List of the directions chosen is returned
            return current_node[1]

        if len(current_node[1]) <= cutoff:

            # Otherwise, find all successors and update frontier
            successors = problem.get_better_successors(current_node[0])
            for node in successors:
                if node[0]['snake'].head.pos not in explored:
                    # Check that the node is not in the frontier using temp stack
                    bounce = util.Stack()
                    while not frontier.isEmpty():
                        move_node = frontier.pop()
                        if (move_node[0]['snake'].head.pos == current_node[0]['snake'].head.pos):
                            # Discard move_node, it will be replaced later
                            pass
                        # Otherwise keep looking
                        else:
                            bounce.push(move_node)
                    # Push all items from temp stack back into frontier
                    while not bounce.isEmpty():
                        go_back = bounce.pop()
                        frontier.push(go_back)

                    # Add (or replace) the node to the frontier
                    frontier.push((node[0], current_node[1] + [node[1]]))


'''
Search the shallowest nodes in the search tree first
Input: search problem
Returns: search path, a sequence of actions
'''
def bfs(problem, heuristic=None):
    # Initialize problem, pushing first node to frontier
    initial_node = (problem.get_start_state(), [])
    frontier = util.Queue()
    frontier.push(initial_node)
    explored = []

    while not frontier.isEmpty():
        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        explored.append(current_node_state)

        if problem.is_goal_state(current_node_state):
            return current_node_path

        for successor in problem.get_successors(current_node_state):

            action = successor[1]
            next_state = successor[0]

            if next_state not in explored:

                # Check if the frontier contains a node with the next state
                # If so, set boolean which prevents adding to frontier
                # Maintain temp queue to hold items popped from frontier
                # Push items from temp queue back onto frontier

                frontier_contains_next_state = False
                temp_queue = util.Queue()

                while not frontier.isEmpty():
                    current = frontier.pop()
                    if current[0]['snake'].head.pos == next_state['snake'].head.pos:
                        frontier_contains_next_state = True

                    temp_queue.push(current)

                while not temp_queue.isEmpty():
                    frontier.push(temp_queue.pop())

                if not frontier_contains_next_state:
                    frontier.push((next_state, current_node_path + [action]))


def bfs_plus(problem, heuristic=None):
    # Initialize problem, pushing first node to frontier
    initial_node = (problem.get_start_state(), [])
    frontier = util.Queue()
    frontier.push(initial_node)
    explored = []

    while not frontier.isEmpty():
        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        explored.append(current_node_state)

        if problem.is_goal_state(current_node_state):
            return current_node_path

        for successor in problem.get_better_successors(current_node_state):

            action = successor[1]
            next_state = successor[0]

            if next_state not in explored:

                # Check if the frontier contains a node with the next state
                # If so, set boolean which prevents adding to frontier
                # Maintain temp queue to hold items popped from frontier
                # Push items from temp queue back onto frontier

                frontier_contains_next_state = False
                temp_queue = util.Queue()

                while not frontier.isEmpty():
                    current = frontier.pop()
                    if current[0]['snake'].head.pos == next_state['snake'].head.pos:
                        frontier_contains_next_state = True

                    temp_queue.push(current)

                while not temp_queue.isEmpty():
                    frontier.push(temp_queue.pop())

                if not frontier_contains_next_state:
                    frontier.push((next_state, current_node_path + [action]))

    raise Exception("Ran out of states")


'''
Search the node of least total cost first
Input: search problem
Returns: search path, a sequence of actions
'''
def ucs(problem, heuristic=None):
    # Initialize problem, pushing first node to frontier
    initial_node = (problem.get_start_state(), [], 0)
    frontier = util.PriorityQueue()
    frontier.push(initial_node, 0)
    explored = []

    while not frontier.isEmpty():

        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        current_node_cost = current_node[2]
        explored.append(current_node_state)

        if problem.is_goal_state(current_node_state):
            return current_node_path

        for successor in problem.get_successors(current_node_state):
            action = successor[1]
            next_state = successor[0]
            step_cost = successor[2]

            next_cost = current_node_cost + step_cost
            next_node = (next_state, current_node_path + [action], next_cost)

            if next_state not in explored:

                # Check if the frontier contains node with next state
                # If so, replace node in frontier with the next cost
                # (Only if the next cost has a lower priority)
                # Maintain temporary priority queue and push back on to frontier

                frontier_contains_next_state = False
                temp_queue = util.PriorityQueue()

                while not frontier.isEmpty():
                    current = frontier.pop()
                    #if current[0] == next_state:
                    if current[0]['snake'].head.pos == next_state['snake'].head.pos:
                        frontier_contains_next_state = True
                        if current[2] > next_cost:
                            temp_queue.push(next_node, next_cost)
                        else:
                            temp_queue.push(current, current[2])

                    else:
                        temp_queue.push(current, current[2])

                while not temp_queue.isEmpty():
                    temp_node = temp_queue.pop()
                    frontier.push(temp_node, temp_node[2])

                if not frontier_contains_next_state:
                    frontier.push(next_node, next_cost)

def ucs_plus(problem, heuristic=None):
    # Initialize problem, pushing first node to frontier
    initial_node = (problem.get_start_state(), [], 0)
    frontier = util.PriorityQueue()
    frontier.push(initial_node, 0)
    explored = []

    while not frontier.isEmpty():

        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        current_node_cost = current_node[2]
        explored.append(current_node_state)

        if problem.is_goal_state(current_node_state):
            return current_node_path

        for successor in problem.get_better_successors(current_node_state):
            action = successor[1]
            next_state = successor[0]
            step_cost = successor[2]

            next_cost = current_node_cost + step_cost
            next_node = (next_state, current_node_path + [action], next_cost)

            if next_state not in explored:

                # Check if the frontier contains node with next state
                # If so, replace node in frontier with the next cost
                # (Only if the next cost has a lower priority)
                # Maintain temporary priority queue and push back on to frontier

                frontier_contains_next_state = False
                temp_queue = util.PriorityQueue()

                while not frontier.isEmpty():
                    current = frontier.pop()
                    #if current[0] == next_state:
                    if current[0]['snake'].head.pos == next_state['snake'].head.pos:
                        frontier_contains_next_state = True
                        if current[2] > next_cost:
                            temp_queue.push(next_node, next_cost)
                        else:
                            temp_queue.push(current, current[2])

                    else:
                        temp_queue.push(current, current[2])

                while not temp_queue.isEmpty():
                    temp_node = temp_queue.pop()
                    frontier.push(temp_node, temp_node[2])

                if not frontier_contains_next_state:
                    frontier.push(next_node, next_cost)




'''
Search the node that has the lowest combined cost and heuristic first.
Input: search problem, heuristic function
Returns: search path, a sequence of actions
'''
def astar(problem, heuristic):

    # Initialize problem, pushing first node to frontier
    initial_node = (problem.get_start_state(), [], 0)
    frontier = util.PriorityQueue()



    frontier.push(initial_node, heuristic( problem.get_start_state()) )
    explored = []


    while not frontier.isEmpty():

        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        current_node_cost = current_node[2]
        explored.append(current_node_state)

        if problem.is_goal_state(current_node_state):
            return current_node_path

        for successor in problem.get_successors(current_node_state):
            action = successor[1]
            next_state = successor[0]
            step_cost = successor[2]

            next_cost = current_node_cost + step_cost
            next_node = (next_state, current_node_path + [action], next_cost)
            next_priority = next_cost + heuristic(next_state)

            if next_state not in explored:


                # Check if the frontier contains node with next state
                # If so, replace node in frontier with the next priority if lower
                # Maintain temporary priority queue and push back on to frontier

                frontier_contains_next_state = False
                temp_queue = util.PriorityQueue()

                while not frontier.isEmpty():
                    current = frontier.pop()


                    # Get priority by adding the step cost to the heuristic value at the current state
                    current_priority = current[2] + heuristic(current[0])

                    #if current[0] == next_state:
                    if current[0]['snake'].head.pos == next_state['snake'].head.pos:
                        frontier_contains_next_state = True

                        if current_priority > next_priority:
                            temp_queue.push(next_node, next_priority)
                        else:
                            temp_queue.push(current, current_priority)
                    else:
                        temp_queue.push(current, current_priority)

                while not temp_queue.isEmpty():
                    temp_node = temp_queue.pop()
                    temp_priority = temp_node[2] + heuristic(temp_node[0])
                    frontier.push(temp_node, temp_priority)

                if not frontier_contains_next_state:
                    frontier.push(next_node, next_priority)



def astar_plus(problem, heuristic):

    # Initialize problem, pushing first node to frontier
    initial_node = (problem.get_start_state(), [], 0)
    frontier = util.PriorityQueue()



    frontier.push(initial_node, heuristic( problem.get_start_state()) )
    explored = []


    while not frontier.isEmpty():

        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        current_node_cost = current_node[2]
        explored.append(current_node_state)

        if problem.is_goal_state(current_node_state):
            return current_node_path

        for successor in problem.get_better_successors(current_node_state):
            action = successor[1]
            next_state = successor[0]
            step_cost = successor[2]

            next_cost = current_node_cost + step_cost
            next_node = (next_state, current_node_path + [action], next_cost)
            next_priority = next_cost + heuristic(next_state)

            if next_state not in explored:


                # Check if the frontier contains node with next state
                # If so, replace node in frontier with the next priority if lower
                # Maintain temporary priority queue and push back on to frontier

                frontier_contains_next_state = False
                temp_queue = util.PriorityQueue()

                while not frontier.isEmpty():
                    current = frontier.pop()


                    # Get priority by adding the step cost to the heuristic value at the current state
                    current_priority = current[2] + heuristic(current[0])

                    #if current[0] == next_state:
                    if current[0]['snake'].head.pos == next_state['snake'].head.pos:
                        frontier_contains_next_state = True

                        if current_priority > next_priority:
                            temp_queue.push(next_node, next_priority)
                        else:
                            temp_queue.push(current, current_priority)
                    else:
                        temp_queue.push(current, current_priority)

                while not temp_queue.isEmpty():
                    temp_node = temp_queue.pop()
                    temp_priority = temp_node[2] + heuristic(temp_node[0])
                    frontier.push(temp_node, temp_priority)

                if not frontier_contains_next_state:
                    frontier.push(next_node, next_priority)



'''
Search the node that has the lowest heuristic
Input: search problem, heuristic function
Returns: search path, a sequence of actions
'''

def greedy(problem, heuristic):
    # Initialize problem, pushing first node to frontier
    initial_node = (problem.get_start_state(), [], 0)
    frontier = util.PriorityQueue()

    frontier.push(initial_node, heuristic(problem.get_start_state()))
    explored = []

    while not frontier.isEmpty():

        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        current_node_cost = current_node[2]
        explored.append(current_node_state)

        if problem.is_goal_state(current_node_state):
            return current_node_path

        for successor in problem.get_successors(current_node_state):
            action = successor[1]
            next_state = successor[0]
            next_priority = heuristic(next_state)


            next_node = (next_state, current_node_path + [action], heuristic(next_state))


            if next_state not in explored:

                # Check if the frontier contains node with next state
                # If so, replace node in frontier with the next priority if lower
                # Maintain temporary priority queue and push back on to frontier

                frontier_contains_next_state = False
                temp_queue = util.PriorityQueue()

                while not frontier.isEmpty():
                    current = frontier.pop()

                    # Get priority by adding the step cost to the heuristic value at the current state
                    current_priority = heuristic(current[0])

                    # if current[0] == next_state:
                    if current[0]['snake'].head.pos == next_state['snake'].head.pos:
                        frontier_contains_next_state = True

                        if current_priority > next_priority:
                            temp_queue.push(next_node, next_priority)
                        else:
                            temp_queue.push(current, current_priority)
                    else:
                        temp_queue.push(current, current_priority)

                while not temp_queue.isEmpty():
                    temp_node = temp_queue.pop()
                    temp_priority = heuristic(temp_node[0])
                    frontier.push(temp_node, temp_priority)

                if not frontier_contains_next_state:
                    frontier.push(next_node, next_priority)

def greedy_plus(problem, heuristic):
    # Initialize problem, pushing first node to frontier
    initial_node = (problem.get_start_state(), [], 0)
    frontier = util.PriorityQueue()

    frontier.push(initial_node, heuristic(problem.get_start_state()))
    explored = []
    most_recent_node = initial_node

    while not frontier.isEmpty():

        current_node = frontier.pop()
        most_recent_node = current_node
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        current_node_cost = current_node[2]
        explored.append(current_node_state)

        if problem.is_goal_state(current_node_state):
            return current_node_path

        for successor in problem.get_better_successors(current_node_state):
            action = successor[1]
            next_state = successor[0]
            next_priority = heuristic(next_state)


            next_node = (next_state, current_node_path + [action], heuristic(next_state))


            if next_state not in explored:

                # Check if the frontier contains node with next state
                # If so, replace node in frontier with the next priority if lower
                # Maintain temporary priority queue and push back on to frontier

                frontier_contains_next_state = False
                temp_queue = util.PriorityQueue()

                while not frontier.isEmpty():
                    current = frontier.pop()

                    # Get priority by adding the step cost to the heuristic value at the current state
                    current_priority = heuristic(current[0])

                    # if current[0] == next_state:
                    if current[0]['snake'].head.pos == next_state['snake'].head.pos:
                        frontier_contains_next_state = True

                        if current_priority > next_priority:
                            temp_queue.push(next_node, next_priority)
                        else:
                            temp_queue.push(current, current_priority)
                    else:
                        temp_queue.push(current, current_priority)

                while not temp_queue.isEmpty():
                    temp_node = temp_queue.pop()
                    temp_priority = heuristic(temp_node[0])
                    frontier.push(temp_node, temp_priority)

                if not frontier_contains_next_state:
                    frontier.push(next_node, next_priority)
    try:
        print("failsafe")
        successor_list = problem.get_better_successors(most_recent_node[0])
        actions = []
        for successor in successor_list:
            actions.append(successor[1])
        return [random.choice(actions)]
    except IndexError:
        # Arbitrarily return left if get better successors was an empty list
        return [util.Action.LEFT]
