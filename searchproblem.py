from snake import Game
from snake import Snake
from snake import Action

# Game Dimensions (rows & cols should evenly divide game board)
WIDTH = 600
HEIGHT = 600
ROWS = 30
COLS = 30
CELL_SIZE = WIDTH // ROWS

'''
Abstract class for a generic search problem.
Does not implement any of the methods.
'''
class SearchProblem:

    '''
    Returns the start state for the search problem.
    '''
    def get_start_state(self):
        pass

    '''
    Input: state, a search state
    Returns: boolean, True if and only if the state is a valid goal state.
    '''
    def is_goal_state(self, state):
        pass

    '''
    Input: state, a search state
    Returns: list of triples (successor, action, cost)
        successor: successor to the current state
        action: action required to get to the successor state
        cost: incremental cost of expanding to the successor
    '''
    def get_successors(self, state):
        pass

    '''
    Input: actions, a list of actions to take
    Retrns: total cost of a sequence of (legal) actions
    '''
    def get_cost_of_actions(self, actions):
        pass


class SimpleSearchProblem(SearchProblem):

    def __init_(self, starting_state):
        self.start_state = starting_state


    def get_start_state(self):
        return self.start_state

    def is_goal_state(self, state):
        return len(state['body']) == (ROWS * COLS) - 1

    def get_successors(self, state):
        pass

