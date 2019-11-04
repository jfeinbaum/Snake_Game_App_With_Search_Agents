from snake import Game
from snake import Snake
from snake import Action

'''
Abstract class for a generic search problem.
Does not implement any of the methods.
'''
class SearchProblem:

    '''
    Returns the start state for the search problem.
    '''
    def getStartState(self):
        pass

    '''
    Input: state, a search state
    Returns: boolean, True if and only if the state is a valid goal state.
    '''
    def isGoalState(self, state):
        pass

    '''
    Input: state, a search state
    Returns: list of triples (successor, action, cost)
        successor: successor to the current state
        action: action required to get to the successor state
        cost: incremental cost of expanding to the successor
    '''
    def getSuccessors(self, state):
        pass

    '''
    Input: actions, a list of actions to take
    Retrns: total cost of a sequence of (legal) actions
    '''
    def getCostOfActions(self, actions):
        pass


class simpleSearchProblem(SearchProblem):

    def __init_(self):


    def getStartState(self):


    def isGoalState(self, state):

    def getSuccessors(self, state):

    def getCostOfActions(self, actions):