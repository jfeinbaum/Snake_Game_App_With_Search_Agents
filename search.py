import util

'''
Searchest the deepest nodes in the search tree first
Input: search problem
Returns: search path, a sequence of actions
'''
def dfs(problem):
    # Initialize problem, pushing first node to frontier
    initial_node = (problem.getStartState(), [])
    frontier = util.Stack()
    frontier.push(initial_node)
    explored = []

    while not frontier.isEmpty():
        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        explored.append(current_node_state)

        if problem.isGoalState(current_node_state):
            return current_node_path

        for successor in problem.getSuccessors(current_node_state):
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
                    if current[0] == next_state:
                        break
                    temp_stack.push(current)
                while not temp_stack.isEmpty():
                    frontier.push(temp_stack.pop())

                frontier.push((next_state, current_node_path + [action]))


'''
Search the shallowest nodes in the search tree first
Input: search problem
Returns: search path, a sequence of actions
'''
def bfs(problem):
    # Initialize problem, pushing first node to frontier
    initial_node = (problem.getStartState(), [])
    frontier = util.Queue()
    frontier.push(initial_node)
    explored = []

    while not frontier.isEmpty():
        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        explored.append(current_node_state)

        if problem.isGoalState(current_node_state):
            return current_node_path

        for successor in problem.getSuccessors(current_node_state):
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
                    if current[0] == next_state:
                        frontier_contains_next_state = True
                    temp_queue.push(current)

                while not temp_queue.isEmpty():
                    frontier.push(temp_queue.pop())

                if not frontier_contains_next_state:
                    frontier.push((next_state, current_node_path + [action]))


'''
Search the node of least total cost first
Input: search problem
Returns: search path, a sequence of actions
'''
def ucs(problem):
    # Initialize problem, pushing first node to frontier
    initial_node = (problem.getStartState(), [], 0)
    frontier = util.PriorityQueue()
    frontier.push(initial_node, 0)
    explored = []

    while not frontier.isEmpty():

        current_node = frontier.pop()
        current_node_state = current_node[0]
        current_node_path = current_node[1]
        current_node_cost = current_node[2]
        explored.append(current_node_state)

        if problem.isGoalState(current_node_state):
            return current_node_path

        for successor in problem.getSuccessors(current_node_state):
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
                    if current[0] == next_state:
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
    
    
