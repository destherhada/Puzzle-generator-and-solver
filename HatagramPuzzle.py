import numpy as np
import random
from random import randrange

# posiciones:
# 0 -> tal y como viene en piezas
# 1-> la pieza girada  90º sentido de agujas del reloj
# 2 -> la pieza girada 180º sentido de agujas del reloj
# 3 -> la pieza girada 270º sentido de agujas del reloj
# 4 -> la pieza original flipeada                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
# 5 ->  90º + flip 
# 6 -> 180º + flip
# 7 -> 270º + flip
posiciones = [0, 1, 2, 3, 4, 5, 6, 7]

def rotar(pieza, pos):
    if pos == 0:
        return pieza
    elif pos == 1:
        return np.rot90(pieza, 3)
    elif pos == 2:
        return np.rot90(pieza, 2)
    elif pos == 3:
        return np.rot90(pieza, 1)
    elif pos == 4:
        return np.fliplr(pieza)
    elif pos == 5:
        return np.rot90(np.fliplr(pieza), 3)
    elif pos == 6:
        return np.rot90(np.fliplr(pieza), 2)
    elif pos == 7:
        return np.rot90(np.fliplr(pieza), 1)




#la coordenada de colocación de la casilla sera la de arriba izq. diferente de  -1

#los individuos tendran la siguiente forma:
# (coordenada, pos) x piezas 
#si coordenada -1,-1 no posicionamos la pieza


#reducción de individuos invalidos, si una pieza pisa a otra o no cabe, no lo contamos como invalido
# decimos que la pieza no esta puesta

#funcion fitness casillas ocupadas / casillas totales 
#para chekear que puede ser solucion -> ver si todas las casillas del tablero estan ocupadas 

#necesitamos funciones auxiliares para, se puede colocar pieza? (si pisa, o si cabe) si no  -> coordenada -1, -1



#GENERAR INDIVIDUOS ALEATORIOS 
# (coordenad, pos) x pieza 
#coordenada tiene que estar dentro de los valores del tablero o -1,-1
# pos 0-7 
#tamaño de la población inicial N = 500?
#generamos tambien individuos con piezas sin colocar 

def generarPoblacionInicial(tablero, piezas, N):
    poblacion = []
    for i in range(N):
        individuo = []
        for idx, pieza in enumerate(piezas):
            while True:
                coordi = randrange(len(tablero))
                coordj = randrange(len(tablero[0]))
                pos = randrange(8)
                if cabeEnTablero(tablero, rotar(piezas[idx], pos), coordi, coordj):
                    individuo.append([coordi, coordj, pos])
                    break
        poblacion.append(individuo)
    return poblacion


#LA FUNCION DE VALIDEZ DEBE VER SI HAY PIEZAS QUE SE PISAN, O PIEZAS QUE NO CABEN EN EL ESPACIO ASIGNADO ALEATORIAMENTE
#SI ES ALGUNA DE ESAS PONEMOS I,J = -1,-1 (piezas no colocadas)
def marcarInvalidos(poblacion, tablero, piezas):
    for individuo in poblacion:
        tabAux = np.copy(tablero)
        for idx, pieza in enumerate(individuo):
            i, j, pos = pieza
            if i == -1 and j == -1:
                continue
            piezaRotada = rotar(piezas[idx], pos)
            if not cabeEnTablero(tabAux, piezaRotada, i, j):
                pieza[0] = -1
                pieza[1] = -1
            else:
                tabAux = ponerEnTablero(tabAux, piezaRotada, i, j, idx)
    return poblacion



def cabeEnTablero(tablero, pieza, initi, initj):
    
    if (initi + pieza.shape[0] - 1  > tablero.shape[0] - 1) or (initj + pieza.shape[1] - 1  > tablero.shape[1] - 1):
        return False
    else:
        for i in range(initi, initi + pieza.shape[0]):
            for j  in range(initj, initj + pieza.shape[1]): 
                if (pieza[i - initi][j - initj] != -1) and (tablero[i][j] != 0):
                        return False

        return True

def ponerEnTablero(tablero, pieza, initi, initj, numPieza):
    for i in range(initi, initi + pieza.shape[0]):
        for j  in range(initj, initj + pieza.shape[1]): 
            if pieza[i - initi][j - initj] != -1 and tablero[i][j] == 0:
                tablero[i][j] = numPieza
    return tablero

def fitness_func(individuo, tablero, piezas):
    tablero_temp = np.copy(tablero)
    penalizacion = 0
    for idx, pieza in enumerate(individuo):
        i, j, pos = pieza
        pieza_rotada = rotar(piezas[idx], pos)
        if i == -1 and j == -1:
            penalizacion += 10
        elif cabeEnTablero(tablero_temp, pieza_rotada, i, j):
            tablero_temp = ponerEnTablero(tablero_temp, pieza_rotada, i, j, idx + 1)
        else:
            penalizacion += 5
    casillas_ocupadas = np.sum(tablero_temp > 0)
    casillas_totales = np.sum(tablero >= 0)
    return (casillas_ocupadas / casillas_totales) - penalizacion



#selección por torneo
def seleccion_por_torneo(poblacion, tamano_torneo, tablero, piezas):
    participantes_torneo = random.sample(poblacion, tamano_torneo)
    participantes_torneo.sort(key=lambda ind: fitness_func(ind, tablero, piezas), reverse=True)
    return participantes_torneo[0]


#Funcion de cruce en un punto
def cruce_un_punto(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1) - 1) 
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    
    return hijo1, hijo2


#Calculamos  que contribucion hace cada pieza al fitness final
def calcular_impacto(poblacion, tablero, piezas):
    impactos = np.zeros(len(piezas))
    fitness_totales = []

    for individuo in poblacion:
        fitness = fitness_func(individuo, tablero, piezas)
        fitness_totales.append(fitness)
        
        for idx, pieza in enumerate(individuo):
            i, j, pos = pieza
            pieza_rotada = rotar(piezas[idx], pos)
            if cabeEnTablero(tablero, pieza_rotada, i, j):
                impacto = fitness_func(individuo, tablero, piezas) - fitness_func(individuo[:idx] + [(i, j, pos)] + individuo[idx+1:], tablero, piezas)
                impactos[idx] += impacto
    
    impactos = impactos / len(poblacion)
    return impactos, fitness_totales


#Mutamos las piezas con impacto negativo ya que son las que hacen mal al fitness general 
def mutacion_dirigida(individuo, prob_mutacion, impactos, tablero):
    nuevo_individuo = individuo.copy()

    for idx in range(len(nuevo_individuo)):
        if random.random() < prob_mutacion:
            impacto = impactos[idx]
            
            if impacto < 0:
                nueva_coordi = randrange(len(tablero))
                nueva_coordj = randrange(len(tablero[0]))
                nueva_pos = randrange(8)
                nuevo_individuo[idx] = [nueva_coordi, nueva_coordj, nueva_pos]
    
    return nuevo_individuo



def GA_dirigido(poblacion, tablero, piezas, tamano_torneo, prob_cruce, prob_mutacion, num_generaciones):
    for i in range(num_generaciones):
        nueva_poblacion = []
        
        impactos, fitness_totales = calcular_impacto(poblacion, tablero, piezas)
        
        while len(nueva_poblacion) < len(poblacion):
            padre1 = seleccion_por_torneo(poblacion, tamano_torneo, tablero, piezas)
            padre2 = seleccion_por_torneo(poblacion, tamano_torneo, tablero, piezas)
            
            if random.random() < prob_cruce:
                hijo1, hijo2 = cruce_un_punto(padre1, padre2)
            else:
                hijo1, hijo2 = padre1, padre2
            
            hijo1 = mutacion_dirigida(hijo1, prob_mutacion, impactos, tablero)
            hijo2 = mutacion_dirigida(hijo2, prob_mutacion, impactos, tablero)
            
            nueva_poblacion.extend([hijo1, hijo2])
        
        if len(nueva_poblacion) > len(poblacion):
            nueva_poblacion = nueva_poblacion[:len(poblacion)]
        
        poblacion = nueva_poblacion
    
    return poblacion
