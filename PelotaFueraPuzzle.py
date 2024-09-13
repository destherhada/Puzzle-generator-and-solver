from aima.search import *
from aima.search import Problem


class Pelotazos(Problem):
  
  """Representamos los estados como tuplas () con longitud del array del tablero
      -1 -> representa las casillas  no accesibles
      1 -> representa la pelota roja
      0 -> representa los huecos
      2-8 -> representa las diferentes piezas del tablero

"""
  def __init__(self, initial, goal, n_piezas, n, m):
    self.initial = initial
    self.goal = goal
    self.m = m #row
    self.n = n #col
    self.k = n_piezas

  def goal_test(self, state):
    return state[self.goal] == 1


  def actions(self, state):
    N = self.n
    M = self.m
    K = self.k
    pelota = state.index(1)
    ac = list()

    if (pelota % N != N - 1) and (pelota + 1 < len(state)) and state[pelota + 1] == 0:
        ac.append("Mover pelota a la derecha")
    if (pelota % N != 0) and state[pelota - 1] == 0:
        ac.append("Mover pelota a la izquierda")
    if pelota >= N and state[pelota - N] == 0:
        ac.append("Mover pelota arriba")
    if pelota + N < len(state) and state[pelota + N] == 0:
        ac.append("Mover pelota abajo")
    if K > 0:
      for pieza in range(2, K + 1):
          if pieza in state:
            pospieza = state.index(pieza)

            #acciones para pieza 1x1
            if (pospieza % N != N - 1) and (pospieza + 1 < len(state)) and state[pospieza + 1] == 0:
                ac.append("Mover pieza 1x1 nº: " + str(pieza) + " a la derecha")
            if (pospieza % N != 0) and state[pospieza - 1] == 0:
                ac.append("Mover pieza 1x1 nº: " + str(pieza) + " a la izquierda")
            if pospieza >= N and state[pospieza - N] == 0:
                ac.append("Mover pieza 1x1 nº: " + str(pieza) + " arriba")
            if pospieza + N < len(state) and state[pospieza + N] == 0:
                ac.append("Mover pieza 1x1 nº: " + str(pieza) + " abajo")

            #acciones para pieza 1x2 1 col 2 filas
            if pospieza + N < len(state) and state[pospieza + N] == pieza:
                if (pospieza % N != N - 1) and state[pospieza + 1] == 0 and state[pospieza + N + 1] == 0:
                    ac.append("Mover pieza 1x2 nº: " + str(pieza) + " a la derecha")
                if (pospieza % N != 0) and state[pospieza - 1] == 0 and state[pospieza + N - 1] == 0:
                    ac.append("Mover pieza 1x2 nº: " + str(pieza) + " a la izquierda")
                if pospieza + 2 * N < len(state) and state[pospieza + 2 * N] == 0:
                    ac.append("Mover pieza 1x2 nº: " + str(pieza) + " abajo")
                if pospieza >= N and state[pospieza - N] == 0:
                    ac.append("Mover pieza 1x2 nº: " + str(pieza) + " arriba")

            #acciones para pieza 2x1 2 cols 1 fila
            if pospieza % N != N - 1 and state[pospieza + 1] == pieza:
                if pospieza % N != N - 2 and state[pospieza + 2] == 0:
                    ac.append("Mover pieza 2x1 nº: " + str(pieza) + " a la derecha")
                if pospieza % N != 0 and state[pospieza - 1] == 0:
                    ac.append("Mover pieza 2x1 nº: " + str(pieza) + " a la izquierda")
                if pospieza + N < len(state) and state[pospieza + N] == 0 and state[pospieza + N + 1] == 0:
                    ac.append("Mover pieza 2x1 nº: " + str(pieza) + " abajo")
                if pospieza >= N and state[pospieza - N] == 0 and state[pospieza - N + 1] == 0:
                    ac.append("Mover pieza 2x1 nº: " + str(pieza) + " arriba")

            #acciones para pieza 2x2
            if pospieza % N != N - 1 and pospieza + N < len(state) and state[pospieza + 1] == pieza and state[pospieza + N] == pieza and state[pospieza + N + 1] == pieza:
                if pospieza % N != N - 2 and state[pospieza + 2] == 0 and state[pospieza + N + 2] == 0:
                    ac.append("Mover pieza 2x2 nº: " + str(pieza) + " a la derecha")
                if pospieza % N != 0 and state[pospieza - 1] == 0 and state[pospieza + N - 1] == 0:
                    ac.append("Mover pieza 2x2 nº: " + str(pieza) + " a la izquierda")
                if pospieza + 2 * N < len(state) and state[pospieza + 2 * N] == 0 and state[pospieza + 2 * N + 1] == 0:
                    ac.append("Mover pieza 2x2 nº: " + str(pieza) + " abajo")
                if pospieza >= N and state[pospieza - N] == 0 and state[pospieza - N + 1] == 0:
                    ac.append("Mover pieza 2x2 nº: " + str(pieza) + " arriba")

    return ac



  def result(self, state, action):
    N = self.n
    M = self.m
    K = self.k
    sstate = list(state)
    pospelota = state.index(1)
    if action == "Mover pelota a la derecha":
        sstate[pospelota], sstate[pospelota + 1] = sstate[pospelota + 1], sstate[pospelota]
    elif action == "Mover pelota a la izquierda":
        sstate[pospelota], sstate[pospelota - 1] = sstate[pospelota - 1], sstate[pospelota]
    elif action == "Mover pelota arriba":
        sstate[pospelota], sstate[pospelota - N] = sstate[pospelota - N], sstate[pospelota]
    elif action == "Mover pelota abajo":
        sstate[pospelota], sstate[pospelota + N] = sstate[pospelota + N], sstate[pospelota]
  
    for pieza in range(2, K+1):
      if pieza in state:
        pospieza = state.index(pieza)
        if action == "Mover pieza 1x1 nº: " + str(pieza) + " a la derecha":
            sstate[pospieza], sstate[pospieza + 1] = sstate[pospieza + 1], sstate[pospieza]
        elif action == "Mover pieza 1x1 nº: " + str(pieza) + " a la izquierda":
            sstate[pospieza], sstate[pospieza - 1] = sstate[pospieza - 1], sstate[pospieza]
        elif action == "Mover pieza 1x1 nº: " + str(pieza) + " abajo":
            sstate[pospieza], sstate[pospieza + N] = sstate[pospieza + N], sstate[pospieza]
        elif action == "Mover pieza 1x1 nº: " + str(pieza) + " arriba":
            sstate[pospieza], sstate[pospieza - N] = sstate[pospieza - N], sstate[pospieza]

        ##2 filas 1 columna
        elif action == "Mover pieza 1x2 nº: " + str(pieza) + " a la derecha":
          sstate[pospieza], sstate[pospieza + 1], sstate[pospieza + N], sstate[pospieza + N + 1] = 0, pieza, 0, pieza
        elif action == "Mover pieza 1x2 nº: " + str(pieza) + " a la izquierda":
          sstate[pospieza], sstate[pospieza - 1], sstate[pospieza + N], sstate[pospieza + N - 1] = 0, pieza, 0, pieza
        elif action == "Mover pieza 1x2 nº: " + str(pieza) + " abajo":
          sstate[pospieza], sstate[pospieza + N], sstate[pospieza + N], sstate[pospieza + 2 * N] = 0, pieza, 0, pieza
        elif action == "Mover pieza 1x2 nº: " + str(pieza) + " arriba":
          sstate[pospieza], sstate[pospieza - N], sstate[pospieza + N], sstate[pospieza] = 0, pieza, 0, pieza

        elif action == "Mover pieza 2x1 nº: " + str(pieza) + " a la derecha":
          sstate[pospieza], sstate[pospieza + 1], sstate[pospieza + 2] = 0, pieza, pieza
        elif action == "Mover pieza 2x1 nº: " + str(pieza) + " a la izquierda":
          sstate[pospieza - 1], sstate[pospieza], sstate[pospieza + 1] = pieza, pieza, 0
        elif action == "Mover pieza 2x1 nº: " + str(pieza) + " abajo":
          sstate[pospieza], sstate[pospieza + 1], sstate[pospieza + N], sstate[pospieza + N + 1] = 0, 0, pieza, pieza
        elif action == "Mover pieza 2x1 nº: " + str(pieza) + " arriba":
          sstate[pospieza - N], sstate[pospieza - N + 1], sstate[pospieza], sstate[pospieza + 1] = pieza, pieza, 0, 0

        elif action == "Mover pieza 2x2 nº: " + str(pieza) + " a la derecha":
          sstate[pospieza], sstate[pospieza + 1], sstate[pospieza + N], sstate[pospieza + N + 1], sstate[pospieza + 2], sstate[pospieza + N + 2] = 0, pieza, 0, pieza, pieza, pieza
        elif action == "Mover pieza 2x2 nº: " + str(pieza) + " a la izquierda":
          sstate[pospieza - 1], sstate[pospieza], sstate[pospieza + N - 1], sstate[pospieza + N], sstate[pospieza + 1], sstate[pospieza + N + 1] = pieza, pieza, pieza, pieza, 0, 0
        elif action == "Mover pieza 2x2 nº: " + str(pieza) + " abajo":
          sstate[pospieza], sstate[pospieza + 1], sstate[pospieza + N], sstate[pospieza + N + 1], sstate[pospieza + 2 * N], sstate[pospieza + 2 * N + 1] = 0, 0, 0, 0, pieza, pieza
        elif action == "Mover pieza 2x2 nº: " + str(pieza) + " arriba":
          sstate[pospieza - 2 * N], sstate[pospieza - 2 * N + 1], sstate[pospieza - N], sstate[pospieza - N + 1], sstate[pospieza], sstate[pospieza + 1] = pieza, pieza, pieza, pieza, 0, 0

    return tuple(sstate)

    
    #aplicamos la heuristica de CHEBYSHEV 
  def h(self, node):
      sum = 0
      pos_pelota = node.state.index(1)
      actual_y = pos_pelota % self.n
      actual_x = pos_pelota // self.n
      goal_pos = self.goal
      goal_y = goal_pos % self.n
      goal_x = goal_pos // self.n
      sum = 2 * max(abs(goal_y - actual_y), abs(goal_x - actual_x))

      return sum
  
  def value(self, state):
      sum = 0
      pos_pelota = state.index(1)
      actual_y = pos_pelota % self.n
      actual_x = pos_pelota // self.n
      goal_pos = self.goal
      goal_y = goal_pos % self.n
      goal_x = goal_pos // self.n
      sum = 2 * max(abs(goal_y - actual_y), abs(goal_x - actual_x))
      return sum

  
  def path_cost(self, c, state1, action, state2):
        return c + 1

