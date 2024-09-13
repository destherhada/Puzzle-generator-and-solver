from aima.search import *
from aima.search import Problem


class Puzzle8(Problem):
    """Problema a del 8-puzzle.  Los estados serán tuplas de nueve elementos,
    permutaciones de los números del 0 al 8 (el 0 es el hueco). Representan la
    disposición de las fichas en el tablero, leídas por filas de arriba a
    abajo, y dentro de cada fila, de izquierda a derecha. Las cuatro
    acciones del problema las representaremos mediante las cadenas:
    "Mover hueco arriba", "Mover hueco abajo", "Mover hueco izquierda" y
    "Mover hueco derecha", respectivamente.
    Para que sea más amigable para el usuario tendermeos que cambiar el nombre de las acciones"""""

    def __init__(self, init, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        self.goal = goal
        self.initial = init
        Problem.__init__(self, self.initial, goal)

    def actions(self,estado):
        pos_hueco=estado.index(0) 
        accs=list()
        if pos_hueco not in (0,1,2):
            accs.append("Mover hueco arriba")

        if pos_hueco not in (6,7,8):
            accs.append("Mover hueco abajo")

        if pos_hueco not in (0,3,6):
            accs.append("Mover hueco izquierda")

        if pos_hueco not in (2,5,8):
            accs.append("Mover hueco derecha")

        return accs

    def result(self,estado,accion):
        pos_hueco = estado.index(0)
        l = list(estado)

        if accion == "Mover hueco arriba":
            l[pos_hueco] = l[pos_hueco - 3]
            l[pos_hueco - 3] = 0


        elif accion == "Mover hueco abajo":
            l[pos_hueco] = l[pos_hueco + 3]
            l[pos_hueco + 3] = 0

        elif accion == "Mover hueco izquierda":
            l[pos_hueco] = l[pos_hueco - 1]
            l[pos_hueco - 1] = 0

        elif accion == "Mover hueco derecha":
            l[pos_hueco] = l[pos_hueco + 1]
            l[pos_hueco + 1] = 0
        return tuple(l)

  
    #aplicamos la heuristica de CHEBYSHEV 
    def h(self, node):
        sum = 0
        for (s, g) in zip(node.state, self.goal):
            if s != g:
                goal_pos = self.goal.index(s)
                goal_y = goal_pos % 3
                goal_x = goal_pos / 3
                actual_pos = node.state.index(s)
                actual_y = actual_pos % 3
                actual_x = actual_pos / 3
                sum += 2 * max(abs(goal_y - actual_y), abs(goal_x - actual_x))
            
        return sum

    def goal_test(self, state):
        return state == self.goal




class Puzzle16(Problem):

  
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)):
        self.goal = goal
        self.initial = initial
        Problem.__init__(self, self.initial, self.goal)

    def actions(self,estado):
        pos_hueco=estado.index(0) 
        accs=list()
        if pos_hueco not in (0,1,2,3):
            accs.append("Mover hueco arriba")

        if pos_hueco not in (12,13,14,15):
            accs.append("Mover hueco abajo")

        if pos_hueco not in (0,4,8,12):
            accs.append("Mover hueco izquierda")

        if pos_hueco not in (3,7,11,15):
            accs.append("Mover hueco derecha")

        return accs

    def result(self,estado,accion):
        pos_hueco = estado.index(0)
        l = list(estado)

        if accion == "Mover hueco arriba":
            l[pos_hueco] = l[pos_hueco - 4]
            l[pos_hueco - 4] = 0


        elif accion == "Mover hueco abajo":
            l[pos_hueco] = l[pos_hueco + 4]
            l[pos_hueco + 4] = 0

        elif accion == "Mover hueco izquierda":
            l[pos_hueco] = l[pos_hueco - 1]
            l[pos_hueco - 1] = 0

        elif accion == "Mover hueco derecha":
            l[pos_hueco] = l[pos_hueco + 1]
            l[pos_hueco + 1] = 0
        return tuple(l)
    
  
    def h(self, node):
        sum = 0
        for (s, g) in zip(node.state, self.goal):
            if s != g:
                goal_pos = self.goal.index(s)
                goal_y = goal_pos % 4
                goal_x = goal_pos / 4
                actual_pos = node.state.index(s)
                actual_y = actual_pos % 4
                actual_x = actual_pos / 4
                sum += 2 * max(abs(goal_y - actual_y), abs(goal_x - actual_x))
            
        return sum
    
    def goal_test(self, state):
        return state == self.goal
