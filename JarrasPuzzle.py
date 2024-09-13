from aima.search import *



class Jarras(Problem):

    def __init__(self, initial, goal, vol):
        self.initial_state = initial
        self.initial = initial
        self.goal = goal
        self.vol = vol


    def actions(self, state):
        ac = list()
        vol = self.vol
        if state[0] > 0:
            if state[1] < vol[1]:
                ac.append("Verter jarra 1 en jarra 2")
            if state[2] < vol[2]:
                ac.append("Verter jarra 1 en jarra 3")

        if state[1] > 0:
            if state[0] < vol[0]:
                ac.append("Verter jarra 2 en jarra 1")
            if state[2] < vol[2]:
                ac.append("Verter jarra 2 en jarra 3")

        if state[2] > 0:
            if state[0] < vol[0]:
                ac.append("Verter jarra 3 en jarra 1")
            if state[1] < vol[1]:
                ac.append("Verter jarra 3 en jarra 2")

        return ac

    def result(self, state, action):
        p16, p9, p7 = state
        vol = self.vol

        if action == "Verter jarra 1 en jarra 2":
            if p16 > 0 and p9 < vol[1]:
                amount = min(p16, vol[1] - p9)
                return (p16 - amount, p9 + amount, p7)

        elif action == "Verter jarra 1 en jarra 3":
            if p16 > 0 and p7 < vol[2]:
                amount = min(p16, vol[2] - p7)
                return (p16 - amount, p9, p7 + amount)

        elif action == "Verter jarra 2 en jarra 1":
            if p9 > 0 and p16 < vol[0]:
                amount = min(p9, vol[0] - p16)
                return (p16 + amount, p9 - amount, p7)

        elif action == "Verter jarra 2 en jarra 3":
            if p9 > 0 and p7 < vol[2]:
                amount = min(p9, vol[2] - p7)
                return (p16, p9 - amount, p7 + amount)

        elif action == "Verter jarra 3 en jarra 1":
            if p7 > 0 and p16 < vol[0]:
                amount = min(p7, vol[0] - p16)
                return (p16 + amount, p9, p7 - amount)

        elif action == "Verter jarra 3 en jarra 2":
            if p7 > 0 and p9 < vol[1]:
                amount = min(p7, vol[1] - p9)
                return (p16, p9 + amount, p7 - amount)

        return state

    def test_goal(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        differences = [abs(current - goal) for current, goal in zip(node.state, self.goal)]
        return min(differences)

    def value(self, state):
        return 1 if self.is_goal(state) else 0



