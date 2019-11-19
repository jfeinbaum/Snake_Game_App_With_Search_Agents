import random
from searchproblem import get_moves


class MDP:




    def get_start_state(self):
        """
        Return the start state of the MDP.
        """
        pass


    def get_possible_actions(self, state):
        """
        Return list of possible actions from 'state'.
        """
        pass


    def get_transition_states_and_probs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.

        Note that in Q-Learning and reinforcment
        learning in general, we do not know these
        probabilities nor do we directly model them.
        """
        pass


    def get_reward(self, state, action, nextState):
        """
        Get the reward for the state, action, nextState transition.

        Not available in reinforcement learning.
        """
        pass


    def is_terminal(self, state):
        """
        Returns true if the current state is a terminal state.  By convention,
        a terminal state has zero future rewards.  Sometimes the terminal state(s)
        may have no possible actions.  It is also common to think of the terminal
        state as having a self-loop action 'pass' with zero reward; the formulations
        are equivalent.
        """
        pass


class Markov(MDP):

    def __init__(self, game, starting_state):
        self.game = game
        self.starting_state = starting_state




    def get_start_state(self):
        return self.starting_state


    def get_possible_actions(self, state):
        actions = get_moves()
        possible = []
        for a in actions:
            successor = self.game.get_new_state(state, a)
            if not successor['snake'].wall_collide() and not successor['snake'].body_collide():
                possible.append(a)
        return possible










