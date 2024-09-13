import copy
import numpy as np
from aima.search import Problem

class stompOnIt(Problem):
    def __init__(self, initial, goal):
        self.initial = tuple(map(tuple, np.array(initial)))  
        self.goal = tuple(map(tuple, np.array(goal))) 
        self.n = len(initial)
        self.m = len(initial[0])

    def actions(self, state):
        ac = []
        for i in range(self.n):
            for j in range(self.m):
                ac.append("stomp on position " + str(i) + "," + str(j))
        return ac

    def result(self, state, action):
        new_state = [list(row) for row in state]
        i, j = map(int, action.split()[-1].split(','))
        new_state[i][j] = abs(new_state[i][j] - 1)
        if i + 1 < self.n:
            new_state[i + 1][j] = abs(new_state[i + 1][j] - 1)
        if i - 1 >= 0:
            new_state[i - 1][j] = abs(new_state[i - 1][j] - 1)
        if j + 1 < self.m:
            new_state[i][j + 1] = abs(new_state[i][j + 1] - 1)
        if j - 1 >= 0:
            new_state[i][j - 1] = abs(new_state[i][j - 1] - 1)
        return tuple(map(tuple, new_state))  

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        return np.sum(np.array(node.state) != np.array(self.goal))

