from tkinter import *
from PIL import Image, ImageTk
import random
import HatagramPuzzle
import JarrasPuzzle
import PelotaFueraPuzzle
import Puzzle816
import StompPuzzle
from aima.search import astar_search
from aima.search import *
import re
import numpy as np
from tkinter import messagebox
import math


#######################################################################
##############DEF GLOBALES##############################################
lista_piezas = []
contador_piezas = 0
elementos_tablero = []
estado_tablero = []
paso_actual = 0


def show_frame(frame):
    frame.tkraise()


def validate_numeric_input(P):
    if P.isdigit():
        return True
    return False

def validate_image_input(P):
    pattern = r'^[\d,]*$'

    if re.match(pattern,P):
        return True
    return False

def get_entry_value(entry):
    try:
        value = entry.get()
        if value == '':
            return 0
        return int(value)
    except ValueError:
        return 0


####################################################################################
####################### FUNCIONES AUX JARRAS  ######################################
###################################################################################



def resolver_jarras():
    try:
        global paso_actual
        init_jarras = (get_entry_value(s1), get_entry_value(s2), get_entry_value(s3))
        fin_jarras = (get_entry_value(f1), get_entry_value(f2), get_entry_value(f3))
        cap_jarras = (get_entry_value(vol_jarra1), get_entry_value(vol_jarra2), get_entry_value(vol_jarra3))

        instancia_jarras = JarrasPuzzle.Jarras(init_jarras, fin_jarras, cap_jarras)
        resolucion_jarras = astar_search(instancia_jarras)
        sol = resolucion_jarras.solution() if resolucion_jarras else None

        if sol:
            n_pasos_sol = f"Faltan {len(sol)} para llegar a la solución"
            pista_jarras = "El siguiente paso debes hacer es: " + sol[0]
            paso_actual = 0
            boton_mas_pistas = Button(frame_resolver_jarras, text="Otra pista", command=lambda:print_pista_jarras(sol))
            boton_mas_pistas.grid(row=10, column=2, padx=5, pady=5, sticky="nsew")
        else:
            pista_jarras = "No se encontró solución"
        
        label_jarras_resolucion.config(text=pista_jarras)
        label_jarras_resolucion_pasos.config(text=n_pasos_sol)
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def print_pista_jarras(solucion):
    try:
        global paso_actual
        if paso_actual + 1  < len(solucion):
            paso_actual +=1
            n_pasos_sol = f"Faltan {len(solucion) - paso_actual} para llegar a la solución"
            pista_jarras = "El siguiente paso debes hacer es: " + solucion[paso_actual]
            label_jarras_resolucion.config(text=pista_jarras)
            label_jarras_resolucion_pasos.config(text=n_pasos_sol)
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def generar_jarras(dificultad):
    try:
        intentos = 0
        max_intentos = 10000
        maxa = maxb = maxc = fa = fb = fc = 0
        solution = None

        while intentos < max_intentos:
            intentos += 1  
            maxa = random.randint(1, 25)
            maxb = random.randint(1, 25)
            maxc = random.randint(1, 25)
            fa = random.randint(0, maxa)
            fb = random.randint(0, maxb)
            fc = random.randint(0, maxc)

            p = JarrasPuzzle.Jarras((maxa, 0, 0), (fa, fb, fc), (maxa, maxb, maxc))
            solution = astar_search(p)

            if solution is not None and hasattr(solution, 'solution'):
                dif = len(solution.solution())
                if (dificultad == "Fácil" and 1 <= dif < 8) or \
                   (dificultad == "Intermedio" and 8 <= dif < 15) or \
                   (dificultad == "Difícil" and 15 <= dif < 20) or \
                   (dificultad == "Muy difícil" and 20 <= dif < 25):
                    print(dif)
                    break

        if solution is not None:
            estado_inicial_label_jarras = Label(frame_generar_jarras, text="ESTADO INICIAL", bg="lightblue", font=("Helvetica", 12))
            estado_objetivo_label_jarras = Label(frame_generar_jarras, text="ESTADO OBJETIVO", bg="lightblue", font=("Helvetica", 12))

            estado_inicial_label_jarras.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
            estado_objetivo_label_jarras.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

            canvas = Canvas(frame_generar_jarras, bg="lightblue")
            canvas.grid(row=4, column=1, rowspan=10, columnspan=2, sticky="nsew", padx=20, pady=20)
            pintar_generado_jarras(canvas, (maxa, 0, 0), (fa, fb, fc), (maxa, maxb, maxc))
        else:
            messagebox.showinfo("Información", "No se pudo generar una solución válida después de múltiples intentos.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        
def pintar_generado_jarras(canvas, estado_inicial, estado_objetivo, capacidades):

    num_jarras = len(capacidades)
    jarra_width = 120
    jarra_height = 200
    spacing = 20
    offset = 220 

    canvas_width = (num_jarras * (jarra_width + spacing) * 2) + offset - spacing
    canvas_height = jarra_height + 60
    canvas.config(width=canvas_width, height=canvas_height)

    color_liquido = "blue"
    color_borde = "black"


    for idx, (estado, capacidad) in enumerate(zip(estado_inicial, capacidades)):
        x = idx * (jarra_width + spacing)
        y = 10

        canvas.create_rectangle(x, y, x + jarra_width, y + jarra_height, outline=color_borde, width=2)
        if estado > 0:
            height_liquido = (estado / capacidad) * jarra_height
            canvas.create_rectangle(x, y + (jarra_height - height_liquido), x + jarra_width, y + jarra_height, fill=color_liquido, outline=color_borde)
        canvas.create_text(x + jarra_width / 2, y + jarra_height / 2, text=str(estado), font=("Arial", 16))
        canvas.create_text(x + jarra_width / 2, y + jarra_height + 20, text=f"Max: {capacidad}", font=("Arial", 12))


    offset_x = num_jarras * (jarra_width + spacing) + offset 

    for idx, (estado, capacidad) in enumerate(zip(estado_objetivo, capacidades)):
        x = offset_x + idx * (jarra_width + spacing)
        y = 10

        canvas.create_rectangle(x, y, x + jarra_width, y + jarra_height, outline=color_borde, width=2)
        if estado > 0:
            height_liquido = (estado / capacidad) * jarra_height
            canvas.create_rectangle(x, y + (jarra_height - height_liquido),x + jarra_width, y + jarra_height,fill=color_liquido, outline=color_borde)
        
        canvas.create_text(x + jarra_width / 2, y + jarra_height / 2, text=str(estado), font=("Arial", 16))
        canvas.create_text(x + jarra_width / 2, y + jarra_height + 20, text=f"Max: {capacidad}", font=("Arial", 12))


####################################################################################
####################### FUNCIONES AUX PUZZLE8 ######################################
####################################################################################

def resolver_imagen():
    try:
        global paso_actual
        init_estado = (estado_imagen.get())
        tupla_estado = tuple(map(int, init_estado.split(',')))
        obj_estado = estado_imagen_objetivo.get()
        tupla_obj = tuple(map(int, obj_estado.split(',')))
        sol = None
        if len(tupla_estado) == 9:
            instancia_imagen = Puzzle816.Puzzle8(tupla_estado,tupla_obj)
            resolucion_imagen = astar_search(instancia_imagen)
            sol = resolucion_imagen.solution() if resolucion_imagen else None 
        elif len(tupla_estado) == 16:
            instancia_imagen = Puzzle816.Puzzle16(tupla_estado,tupla_obj)
            resolucion_imagen = astar_search(instancia_imagen)
            sol = resolucion_imagen.solution() if resolucion_imagen else None

        if sol:
            n_pasos_sol = f"Faltan {len(sol)} para llegar a la solución"
            pista_imagen = "El siguiente paso debes hacer es: " + sol[0]
            paso_actual = 0
            boton_mas_pistas = Button(frame_resolver_imagen, text="Otra pista", command=lambda:print_pista_puzzle8(sol))
            boton_mas_pistas.grid(row=8, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
        else:
            pista_imagen = "No se encontró solución"
        
        label_imagen_resolucion.config(text=pista_imagen)
        label_imagen_resolucion_pasos.config(text=n_pasos_sol)
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def print_pista_puzzle8(solucion):
    try:
        global paso_actual
        if paso_actual + 1  < len(solucion):
            paso_actual +=1
            n_pasos_sol = f"Faltan {len(solucion) - paso_actual} para llegar a la solución"
            pista_imagen = "El siguiente paso debes hacer es: " + solucion[paso_actual]
            label_imagen_resolucion.config(text=pista_imagen)
            label_imagen_resolucion_pasos.config(text=n_pasos_sol)
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    

def generar_imagen(dificultad):
    try:
        intentos = 0
        max_intentos = 10000
        tupla_aleatoria = ()
        numeros= ()
        estado_objetivo = ()
        estado_nuevo = ()
        estado_init = ()
        while intentos < max_intentos:
            intentos += 1  
            solution = None
            if dificultad == "Fácil" or dificultad == "Intermedio":
                #generamos un estado aleatorio
                numeros = list(range(9))
                random.shuffle(numeros)
                tupla_aleatoria = tuple(numeros)
                estado_init = tupla_aleatoria
                p = Puzzle816.Puzzle8(tupla_aleatoria)
                acciones_posibles = p.actions(tupla_aleatoria)
                #aplicamos un numero de acciones aleatoriamente al estado para crear un estado objetivo
                if dificultad == "Fácil":
                    for i in range (6):
                        indice = random.randint(0,len(acciones_posibles) -1)
                        estado_nuevo = p.result(tupla_aleatoria, acciones_posibles[indice])
                        tupla_aleatoria = estado_nuevo
                        acciones_posibles = p.actions(estado_nuevo)
                else:
                    for i in range (11):
                        indice = random.randint(0,len(acciones_posibles)-1)
                        estado_nuevo = p.result(tupla_aleatoria,acciones_posibles[indice])
                        tupla_aleatoria = estado_nuevo
                        acciones_posibles = p.actions(estado_nuevo)

                p = Puzzle816.Puzzle8(estado_init, estado_nuevo)
                solution = astar_search(p)
            elif dificultad == "Difícil" or dificultad == "Muy difícil":
                numeros = list(range(16))
                random.shuffle(numeros)
                tupla_aleatoria = tuple(numeros)
                estado_init = tupla_aleatoria
                p = Puzzle816.Puzzle16(tupla_aleatoria)
                acciones_posibles = p.actions(tupla_aleatoria)

                if dificultad == "Difícil":
                    for i in range (11):
                        indice = random.randint(0,len(acciones_posibles)-1)
                        estado_nuevo = p.result(tupla_aleatoria, acciones_posibles[indice])
                        tupla_aleatoria = estado_nuevo
                        acciones_posibles = p.actions(estado_nuevo)  
                else:
                    for i in range (16):
                        indice = random.randint(0,len(acciones_posibles)-1)
                        estado_nuevo = p.result(tupla_aleatoria,acciones_posibles[indice])
                        tupla_aleatoria = estado_nuevo
                        acciones_posibles = p.actions(estado_nuevo)                  
                
                p = Puzzle816.Puzzle16(estado_init, estado_nuevo)
                solution = astar_search(p)

            if solution is not None:
                dif = len(solution.solution())
                if (dificultad == "Fácil" and dif < 6):
                   break
                elif(dificultad == "Intermedio" and dif>=6 and dif < 11):
                   break
                elif (dificultad == "Difícil" and dif >= 6 and dif < 11):
                   break
                elif (dificultad == "Muy difícil" and dif >=10 and dif < 16):
                    break



        estado_inicial_label_imagen = Label(frame_generar_imagen, text="ESTADO INICIAL", font=("Helvetica", 12), bg="lightyellow")
        estado_objetivo_label_imagen = Label(frame_generar_imagen, text="ESTADO OBJETIVO",  font=("Helvetica", 12), bg="lightyellow")

        if solution is not None:
            estado_inicial_label_imagen.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
            estado_objetivo_label_imagen.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
            
            canvas = Canvas(frame_generar_imagen, bg="lightyellow")
            canvas.grid(row=4, column=1, rowspan=10, columnspan=2, sticky="nsew")
            
            pintar_generado_imagen(canvas, estado_init,estado_nuevo, len(estado_init)) 
        else:
            messagebox.showinfo("Información", "No se pudo generar una solución válida después de múltiples intentos.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def pintar_generado_imagen(canvas, estado, estado_obj, tamaño):
    filas, columnas = 0,0
    if tamaño == 9:
        filas, columnas = 3, 3
        cell_size = 150
    elif tamaño == 16:
        filas, columnas = 4, 4
        cell_size = 100
    else:
        raise ValueError("El tamaño debe ser 9 (3x3) o 16 (4x4)")

    margen = 200
    canvas_width = (columnas * cell_size) * 2 + margen
    canvas_height = filas * cell_size
    canvas.config(width=canvas_width, height=canvas_height)
    

    for i in range(filas):
        for j in range(columnas):
            valor = estado[i * columnas + j]
            color = "white" if valor == 0 else "lightgrey" 
            canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color, outline="black")
            if valor != 0:
                canvas.create_text((j + 0.5) * cell_size, (i + 0.5) * cell_size, text=str(valor), font=("Arial", 16))

    for i in range(filas):
        for j in range(columnas):
            valor = estado_obj[i * columnas + j]
            color = "white" if valor == 0 else "lightgrey" 
            canvas.create_rectangle(j * cell_size + columnas * cell_size + margen, i * cell_size,
                                    (j + 1) * cell_size + columnas * cell_size + margen, 
                                    (i + 1) * cell_size, fill=color, outline="black")
            if valor != 0:
                canvas.create_text((j + 0.5) * cell_size + columnas * cell_size + margen, 
                                   (i + 0.5) * cell_size, text=str(valor), font=("Arial", 16))

    




####################################################################################
####################### FUNCIONES AUX STOMP ########################################
####################################################################################


def stomp(i,j, elementos):

    if elementos[i][j].cget("bg") == "black":
        elementos[i][j].config(bg="white")
    else:
        elementos[i][j].config(bg="black")

    return elementos

def dibujar_tablero_stomp():
    try:
        label_inicial = Label(frame_resolver_stomp, text="Dibuja el estado inicial", bg='lightpink')
        label_inicial.grid(row=5, column=1, columnspan=5, padx=10, pady=10, sticky="nsew")

        n_filas = int(numero_filas.get())
        n_columnas = int(numero_columnas.get())
        elementos = []

        for i in range(n_filas):
            elem_fila = []
            for j in range(n_columnas):
                elem = Button(frame_resolver_stomp, width=2, height=2, bg="white", command=lambda i=i, j=j, elementos=elementos: stomp(i, j, elementos))
                elem.grid(row=i + 7, column=j +1, sticky="nsew")
                elem_fila.append(elem)
            elementos.append(elem_fila)
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    return elementos


def dibujar_tablero_objetivo():
    try:
        label_inicial = Label(frame_resolver_stomp, text="Dibuja el estado objetivo", bg='lightpink')
        label_inicial.grid(row=5, column=6, columnspan=5, padx=10, pady=10,sticky="nsew")

        n_filas = int(numero_filas.get())
        n_columnas = int(numero_columnas.get())
        elementos = []

        for i in range(n_filas):
            elem_fila = []
            for j in range(n_columnas):
                elem = Button(frame_resolver_stomp, width=2, height=2, bg="white", command=lambda i=i, j=j, elementos=elementos: stomp(i, j, elementos))
                elem.grid(row=i + 7, column=j + 7, sticky="nsew")
                elem_fila.append(elem)
            elementos.append(elem_fila)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    return elementos



def tablero_to_array(elementos):
    try:
        n_filas = int(numero_filas.get())
        n_columnas = int(numero_columnas.get())
        estado = []

        for i in range(n_filas):
            elem_fila = []
            for j in range(n_columnas):
                if elementos[i][j].cget("bg") == "black":
                    elem_fila.append(1)
                else:
                    elem_fila.append(0)
            estado.append(elem_fila)
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    return estado

def dibujar_stomp():
    try:
        valor_elementos_inicial = dibujar_tablero_stomp()
        valor_elementos_objetivo = dibujar_tablero_objetivo()    
        button_generar_solucion = Button(frame_resolver_stomp, text="Resolver", command=lambda estado_inicial=valor_elementos_inicial, estado_objetivo=valor_elementos_objetivo: resolver_stomp(estado_inicial,estado_objetivo) )
        button_generar_solucion.grid(row=calculo_fila, column=1, columnspan=10, padx=10, pady=10, sticky="nsew")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")




def resolver_stomp(valor_elementos_inicial, valor_elementos_objetivo):
    try:
        global paso_actual
      
        estado_inicial = tablero_to_array(valor_elementos_inicial)
        estado_objetivo = tablero_to_array(valor_elementos_objetivo)
        instancia_stomp = StompPuzzle.stompOnIt(estado_inicial, estado_objetivo)
        resolucion_stomp= astar_search(instancia_stomp)
        sol = resolucion_stomp.solution() if resolucion_stomp else None

        if sol:
            n_pasos_sol_stomp = f"Faltan {len(sol)} para llegar a la solución"
            pista_stomp = "El siguiente paso debes hacer es: " + sol[0]
            paso_actual = 0
            boton_mas_pistas = Button(frame_resolver_stomp, text="Otra pista", command=lambda:print_pista_stomp(sol))
            boton_mas_pistas.grid(row=calculo_fila + 4, column=1, columnspan=10, padx=10,pady=10, sticky="nsew")
        else:
            pista_stomp = "No se encontró solución"
        
        label_stomp_resolucion.config(text=pista_stomp)
        label_stomp_resolucion_pasos.config(text=n_pasos_sol_stomp)
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def print_pista_stomp(solucion):
    try:
        global paso_actual
        if paso_actual + 1  < len(solucion):
            paso_actual +=1
            n_pasos_sol = f"Faltan {len(solucion) - paso_actual} para llegar a la solución"
            pista_imagen = "El siguiente paso debes hacer es: " + solucion[paso_actual]
            label_stomp_resolucion.config(text=pista_imagen)
            label_stomp_resolucion_pasos.config(text=n_pasos_sol)
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def generar_stomp(dificultad):
    try:
        max_intentos = 1000
        intentos = 0
        stomp_tablero_inicial = []
        stomp_tablero_objetivo = []
        while intentos < max_intentos:
            solution = None
            if dificultad== "Fácil" or dificultad== "Intermedio":
                stomp_tablero_inicial = np.random.choice([0, 1], (3, 3))
                estado_init = stomp_tablero_inicial
                p = StompPuzzle.stompOnIt(stomp_tablero_inicial, stomp_tablero_objetivo)
                acciones_posibles = p.actions(stomp_tablero_inicial)
                if dificultad=="Fácil":
                    for i in range(6):
                        indice = random.randint(0,len(acciones_posibles)-1)
                        estado_nuevo = p.result(stomp_tablero_inicial, acciones_posibles[indice])
                        stomp_tablero_inicial = estado_nuevo
                        acciones_posibles = p.actions(estado_nuevo)
                else:
                    for i in range(11):
                        indice = random.randint(0,len(acciones_posibles)-1)
                        estado_nuevo = p.result(stomp_tablero_inicial, acciones_posibles[indice])
                        stomp_tablero_inicial = estado_nuevo
                        acciones_posibles = p.actions(estado_nuevo)   
                p = StompPuzzle.stompOnIt(estado_init, estado_nuevo)  
                solution = astar_search(p)                   
            elif dificultad == "Difícil" or dificultad == "Muy difícil":
                stomp_tablero_inicial = np.random.choice([0, 1], (4, 4))
                estado_init = stomp_tablero_inicial
                p = StompPuzzle.stompOnIt(stomp_tablero_inicial, stomp_tablero_objetivo)
                acciones_posibles = p.actions(stomp_tablero_inicial)
                if dificultad == "Difícil":
                    for i in range(11):
                        indice = random.randint(0,len(acciones_posibles)-1)
                        estado_nuevo = p.result(stomp_tablero_inicial, acciones_posibles[indice])
                        stomp_tablero_inicial = estado_nuevo
                        acciones_posibles = p.actions(estado_nuevo)                       
                else:
                    for i in range(15):
                        indice = random.randint(0,len(acciones_posibles)-1)
                        estado_nuevo = p.result(stomp_tablero_inicial, acciones_posibles[indice])
                        stomp_tablero_inicial = estado_nuevo
                        acciones_posibles = p.actions(estado_nuevo)
                p = StompPuzzle.stompOnIt(estado_init, estado_nuevo)   
                solution = astar_search(p)    

            if solution is not None:
                dif = len(solution.solution())

                if dificultad == "Fácil" and dif < 5:
                    break
                elif dificultad == "Intermedio" and dif > 5 and dif < 20:
                    break
                elif dificultad == "Difícil" and dif < 5:
                    break
                elif dificultad == "Muy difícil" and dif > 5 and dif < 20:
                    break

            intentos += 1

        estado_inicial_label_stomp = Label(frame_generar_stomp, text="ESTADO INICIAL", bg='lightpink', font=("Helvetica", 12))
        estado_objetivo_label_stomp = Label(frame_generar_stomp, text="ESTADO OBJETIVO", bg='lightpink', font=("Helvetica", 12))

        if solution is not None:
            estado_inicial_label_stomp.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
            estado_objetivo_label_stomp.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
            canvas = Canvas(frame_generar_stomp,bg='lightpink')
            canvas.grid(row=4, column=1, rowspan=10, columnspan=2, sticky="nsew")
            pintar_generado_stomp(canvas, estado_init, estado_nuevo, len(estado_init),len(estado_nuevo))
        else:
            messagebox.showinfo("Información", "No se pudo generar una solución válida después de múltiples intentos.")

    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")


def pintar_generado_stomp(canvas, estado_inicial, estado_objetivo, filas, columnas):
    if filas == 3:
        cell_size = 150
    else:
        cell_size = 100
    canvas_width = columnas * cell_size * 2 
    canvas_height = filas * cell_size
    canvas.config(width=canvas_width, height=canvas_height)
    colores = ["white", "black"] 

    for i in range(filas):
        for j in range(columnas):
            color_index = estado_inicial[i][j]
            color = colores[color_index]
            canvas.create_rectangle(j * cell_size, i * cell_size,(j + 1) * cell_size, (i + 1) * cell_size, fill=color, outline="black")
    
    offset_x = columnas * cell_size + 200

    for i in range(filas):
        for j in range(columnas):
            color_index = estado_objetivo[i][j]
            color = colores[color_index]
            canvas.create_rectangle(j * cell_size + offset_x, i * cell_size, (j + 1) * cell_size + offset_x, (i + 1) * cell_size,fill=color, outline="black")
    



####################################################################################
####################### FUNCIONES AUX PELOTA #######################################
####################################################################################

def cambia_color(i,j, casillas):
    """black -> -1 (casillas no accesibles)
       red -> 1 (pelota)
       gold1 -> (casilla objetivo)
       lightpink, blue, orange, darkgreen, darkorchid -> piezas
       white -> casilla vacia"""
    
    colores = ["white", "black", "red", "gold1", "lightpink", "blue", "orange", "darkgreen", "darkorchid"]
    color_actual_idx = colores.index(casillas[i][j].cget("bg"))
    siguiente_color = (color_actual_idx + 1) % len(colores) 
    casillas[i][j].config(bg=colores[siguiente_color])

    return casillas


def dibujar_tablero_pelota():
    try:
        label_explicacion_pelota = Label(frame_resolver_pelota, wraplength=500, font=("Helvetica", 12), bg='lightgreen', text="Haz click en las casillas para cambiar su color,(blanco:casilla vacia, negro:casilla no accesible, rojo:pelota, amarillo:objetivo de la pelota, resto de colores: piezas )")
        label_inicial_pelota = Label(frame_resolver_pelota, bg='lightgreen', text="Dibuja el estado inicial", font=("Helvetica", 12))
        label_explicacion_pelota.grid(row=4, column=1, columnspan=2, sticky="nsew")
        label_inicial_pelota.grid(row=5, column=1, columnspan=2, sticky="nsew")

        n_filas = int(numero_filas_pelota.get())
        n_columnas = int(numero_columnas_pelota.get())
        casillas = []

        for i in range(n_filas):
            elem_fila = []
            for j in range(n_columnas):
                elem = Button(frame_resolver_pelota, width=1, height=8, bg="white", command=lambda i=i, j=j, casillas=casillas: cambia_color(i, j, casillas))
                elem.grid(row=i + 7, column=j + 1, sticky="nsew")
                elem_fila.append(elem)
            casillas.append(elem_fila)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    return casillas






def tablero_to_tuple_pelota(elementos):
    n_filas = int(numero_filas_pelota.get())
    n_columnas = int(numero_columnas_pelota.get())
    estado = []

    for i in range(n_filas):
        for j in range(n_columnas):
            if elementos[i][j].cget("bg") == "black":
                estado.append(-1)
            elif elementos[i][j].cget("bg") == "white":
                estado.append(0)
            elif elementos[i][j].cget("bg") == "red":
                estado.append(1)
            elif elementos[i][j].cget("bg") == "gold1":
                estado.append(100)
            elif elementos[i][j].cget("bg") == "lightpink":
                estado.append(2)
            elif elementos[i][j].cget("bg") == "blue":
                estado.append(3)
            elif elementos[i][j].cget("bg") == "orange":
                estado.append(4)
            elif elementos[i][j].cget("bg") == "darkgreen":
                estado.append(5)
            elif elementos[i][j].cget("bg") == "darkorchid":
                estado.append(6)

    estado_tupla = tuple(estado)
    return estado_tupla

def dibujar_pelota():
    try:
        valor_elementos_inicial_pelota = dibujar_tablero_pelota()

        button_generar_solucion = Button(frame_resolver_pelota, text="Resolver", command=lambda estado_inicial=valor_elementos_inicial_pelota: resolver_pelota(estado_inicial) )
        button_generar_solucion.grid(row=calculo_fila_pelota + 6, column=1, columnspan=4, pady=10, padx=10, sticky="nsew")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def resolver_pelota(estado_inicial):
    try:
        global paso_actual
        n_pasos_sol = ""
        
        estado_inicial_pelota = tablero_to_tuple_pelota(estado_inicial)
        casilla_objetivo = estado_inicial_pelota.index(100)
        aux = list(estado_inicial_pelota)
        aux[casilla_objetivo] = 0
        estado_inicial_pelota = tuple(aux)
        numero_piezas = 0
        for i in range(2,7):
            if estado_inicial_pelota.count(i) > 0:
                numero_piezas+=1
        instancia_stomp = PelotaFueraPuzzle.Pelotazos(estado_inicial_pelota, casilla_objetivo, numero_piezas,int(numero_columnas_pelota.get()), int(numero_filas_pelota.get()))
        resolucion_pelota= astar_search(instancia_stomp)
        sol = resolucion_pelota.solution() if resolucion_pelota else None

        if sol:
            n_pasos_sol = f"Faltan {len(sol)} para llegar a la solución"
            paso_actual = 0
            pista_pelota = "El siguiente paso debes hacer es: " + sol[0]
            boton_mas_pistas = Button(frame_resolver_pelota, text="Otra pista", command=lambda:print_pista_pelota(sol))
            boton_mas_pistas.grid(row=calculo_fila_pelota+ 12, column=1, columnspan=5, padx=10, pady=10,sticky="nsew")
        else:
            pista_pelota = "No se encontró solución usando A*, ahora probamos con Simulated Annealing"
            label_pelota_resolucion.config(text=pista_pelota)
            resolucion_pelota_SA = simulated_annealing(instancia_stomp)
            pista_pelota= f"Las piezas en el estado objetivo estan asi: {resolucion_pelota_SA}"
            label_pelota_resolucion.config(text=pista_pelota)
            #pintar_solucion_pelota(resolucion_pelota_SA)

        label_pelota_resolucion.config(text=pista_pelota)
        label_pelota_resolucion_pasos.config(text=n_pasos_sol)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def print_pista_pelota(solucion):
    global paso_actual
    if paso_actual + 1  < len(solucion):
        paso_actual +=1
        n_pasos_sol = f"Faltan {len(solucion) - paso_actual} para llegar a la solución"
        pista_pelota = "El siguiente paso debes hacer es: " + solucion[paso_actual]
        label_pelota_resolucion.config(text=pista_pelota)
        label_pelota_resolucion_pasos.config(text=n_pasos_sol)


def generar_pelota(dificultad):
    try:
        max_intentos = 1000
        intentos = 0
        tablero_inicial_pelota = []
        posicion_pelota_final = 0
        solution = None

        while intentos < max_intentos:
            intentos+=1
            solution = None
            if dificultad == "Fácil":
                tablero_inicial_pelota = random.choices([-1, 0, 2], weights=[0.15, 0.6, 0.25], k=7)
                posicion_pelota_inicial = random.randint(0,8)
                tablero_inicial_pelota.insert(posicion_pelota_inicial, 1)
                posicion_pelota_final = random.randint(0,8)
                tablero_inicial_pelota.insert(posicion_pelota_final, 0)
                numero_piezas = 0
                if tablero_inicial_pelota.count(2) > 0:
                        numero_piezas+=1
                if comprobar_piezas(tablero_inicial_pelota, 1):
                    init = tuple(tablero_inicial_pelota)
                    p = PelotaFueraPuzzle.Pelotazos(init,posicion_pelota_final,numero_piezas,3,3)
                    solution = astar_search(p)
            elif dificultad == "Intermedio":
                tablero_inicial_pelota = random.choices([-1, 0, 2, 3], weights=[0.1, 0.6, 0.2, 0.1], k=7)
                posicion_pelota_inicial = random.randint(0,8)
                tablero_inicial_pelota.insert(posicion_pelota_inicial, 1)
                posicion_pelota_final = random.randint(0,8)
                tablero_inicial_pelota.insert(posicion_pelota_final, 0)
                numero_piezas = 0
                for i in range(2,4):
                    if tablero_inicial_pelota.count(i) > 0:
                        numero_piezas+=1
                if comprobar_piezas(tablero_inicial_pelota, 2):
                    init = tuple(tablero_inicial_pelota)
                    p = PelotaFueraPuzzle.Pelotazos(init,posicion_pelota_final,numero_piezas,3,3)
                    solution = astar_search(p)
            elif dificultad == "Difícil" :
                tablero_inicial_pelota = random.choices([-1, 0, 2, 3, 4], weights=[0.1, 0.3, 0.3, 0.2, 0.1], k=14)
                posicion_pelota_inicial = random.randint(0,15)
                tablero_inicial_pelota.insert(posicion_pelota_inicial, 1)
                posicion_pelota_final = random.randint(0,15)
                tablero_inicial_pelota.insert(posicion_pelota_final, 0)
                numero_piezas = 0
                for i in range(2,5):
                    if tablero_inicial_pelota.count(i) > 0:
                        numero_piezas+=1
                if comprobar_piezas(tablero_inicial_pelota, 4):
                    init = tuple(tablero_inicial_pelota)
                    p = PelotaFueraPuzzle.Pelotazos(init,posicion_pelota_final,numero_piezas,4,4)   
                    solution = astar_search(p)
            elif dificultad == "Muy difícil":
                tablero_inicial_pelota = random.choices([-1, 0, 2, 3, 4, 5, 6], weights=[0.05, 0.3, 0.2, 0.15, 0.1, 0.1, 0.1], k=14)
                posicion_pelota_inicial = random.randint(0,15)
                tablero_inicial_pelota.insert(posicion_pelota_inicial, 1)
                posicion_pelota_final = random.randint(0,15)
                tablero_inicial_pelota.insert(posicion_pelota_final, 0)
                numero_piezas = 0
                for i in range(2,7):
                    if tablero_inicial_pelota.count(i) > 0:
                        numero_piezas+=1
                if comprobar_piezas(tablero_inicial_pelota, 6):
                    init = tuple(tablero_inicial_pelota)
                    p = PelotaFueraPuzzle.Pelotazos(init,posicion_pelota_final,numero_piezas,4,4)   
                    solution = astar_search(p)


        estado_inicial_label_pelota = Label(frame_generar_pelota, text="ESTADO INICIAL", bg="lightgreen")

        if solution is not None:
            dif = len(solution.solution())
            if dificultad == "Fácil" and numero_piezas >= 0 and numero_piezas < 2 and dif < 5:
                estado_inicial_label_pelota.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
                canvas = Canvas(frame_generar_pelota,bg="lightgreen")
                canvas.grid(row=8, column=1, rowspan=10, columnspan=2, sticky="nsew")
                pintar_generado_pelota(canvas, tablero_inicial_pelota, 3, 3,posicion_pelota_final, 150)
            elif dificultad == "Intermedio" and numero_piezas == 2 and dif < 10 and dif > 5:
                estado_inicial_label_pelota.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
                canvas = Canvas(frame_generar_pelota,bg="lightgreen")
                canvas.grid(row=8, column=1, rowspan=10, columnspan=2, sticky="nsew")
                pintar_generado_pelota(canvas, tablero_inicial_pelota, 3, 3,posicion_pelota_final, 150)
            elif dificultad == "Difícil" and numero_piezas == 3 and  dif > 5 and dif < 15:
                estado_inicial_label_pelota.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
                canvas = Canvas(frame_generar_pelota,bg="lightgreen")
                canvas.grid(row=8, column=1, rowspan=10, columnspan=2, sticky="nsew")
                pintar_generado_pelota(canvas, tablero_inicial_pelota, 4, 4,posicion_pelota_final, 150)
            elif dificultad == "Muy difícil" and numero_piezas >= 4 and numero_piezas <  6 and dif > 10:
                estado_inicial_label_pelota.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
                canvas = Canvas(frame_generar_pelota, bg="lightgreen")
                canvas.grid(row=8, column=1, rowspan=10, columnspan=2, sticky="nsew")
                pintar_generado_pelota(canvas, tablero_inicial_pelota, 4, 4,posicion_pelota_final, 150)
            else:
                    solution = None

    
        else:
            messagebox.showinfo("Información", "No se pudo generar una solución válida después de múltiples intentos.")


    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def comprobar_piezas(tablero, numpiezas):
    cols = math.sqrt(len(tablero))
    for k in range(2,numpiezas+1):
        indices =  [i for i, x in enumerate(tablero) if x == k]
        if len(indices) == 2:
            if (indices[0] + 1 != indices[1])  or (indices[1] % cols == 0):
                return False
            elif (indices[0] + cols != indices[1]):
                return False
        elif len(indices) == 3:
            return False
        elif len(indices) == 4:
            if(indices[0] + 1 != indices[1]) or (indices[0] + cols != indices[2]) or (indices[1] + cols != indices[3]) or (indices[2] +1 != indices[3]) or (indices[1] % cols == 0) or (indices[3] % cols == 0):
                return False
        elif len(indices) > 4:
            return False
    
    return True


            
def pintar_generado_pelota(canvas, estado, filas, columnas, pelota_obj, cell_size):
    canvas_width = columnas * cell_size
    canvas_height = filas * cell_size
    canvas.config(width=canvas_width, height=canvas_height)

    estado[pelota_obj] = 100

    for i in range(filas):
        for j in range(columnas):
            valor = estado[i * columnas + j]
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size

            if valor == -1:
                continue 

            elif valor == 1: 
                canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
                canvas.create_oval(x1, y1, x2, y2, fill="red", outline="black")

            elif valor == 0: 
                canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")

            elif valor==100:
                canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
                canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

            elif valor == 2:
                canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")
            
            elif valor == 3:
                canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="black")
            
            elif valor ==4:
                canvas.create_rectangle(x1, y1, x2, y2, fill="pink", outline="black")
            
            elif valor == 5:
                canvas.create_rectangle(x1, y1, x2, y2, fill="orange", outline="black")
            
            elif valor == 6:
                canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black")





####################################################################################
####################### FUNCIONES AUX HATAGRAM #####################################
####################################################################################

def sel(i,j, elementos):
    if elementos[i][j].cget("bg") == "black":
        elementos[i][j].config(bg="white")
    else:
        elementos[i][j].config(bg="black")

    return elementos

def dibujar_tablero(filas, columnas):
    try:
        elementos_tablero = []

        for i in range(filas):
            fila = []
            for j in range(columnas):
                boton =  Button(frame_resolver_puzzle, width=2, height=2, bg="white",
                                command=lambda i=i, j=j: cambia_color(i, j, elementos_tablero))
                boton.grid(row=i + 5, column=j+1, sticky="nsew")
                fila.append(boton)
            elementos_tablero.append(fila)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    return elementos_tablero



def tablero_to_array_puzzle(elementos):
    n_filas = int(numero_filas_puzzle.get())
    n_columnas = int(numero_columnas_puzzle.get())
    estado = []

    for i in range(n_filas):
        elem_fila = []
        for j in range(n_columnas):
            if elementos[i][j].cget("bg") == "black":
                elem_fila.append(-1)
            elif elementos[i][j].cget("bg") == "white":
                elem_fila.append(0)
            elif elementos[i][j].cget("bg") == "red":
                elem_fila.append(1)
            elif elementos[i][j].cget("bg") == "gold1":
                elem_fila.append(2)
            elif elementos[i][j].cget("bg") == "lightpink":
                elem_fila.append(3)
            elif elementos[i][j].cget("bg") == "blue":
                elem_fila.append(4)
            elif elementos[i][j].cget("bg") == "orange":
                elem_fila.append(5)
            elif elementos[i][j].cget("bg") == "darkgreen":
                elem_fila.append(6)
            elif elementos[i][j].cget("bg") == "darkorchid":
                elem_fila.append(7)

        estado.append(elem_fila)
    return estado

def pieza_to_array(elementos, n_pieza):
    try:
        n_filas = int(numero_filas_pieza.get())
        n_columnas = int(numero_columnas_pieza.get())
        estado = []

        for i in range(n_filas):
            elem_fila = []
            for j in range(n_columnas):
                if elementos[i][j].cget("bg") == "black":
                    elem_fila.append(-1)
                elif elementos[i][j].cget("bg") == "white":
                    elem_fila.append(n_pieza+1)
            estado.append(elem_fila)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")           
    return estado




def resolver_puzzle(lista_piezas, lista_tablero):
    try:
        tamano_torneo = 5
        prob_cruce = 0.8
        prob_mutacion = 0.15
        num_generaciones = 100
        tamano_poblacion = 1000

        array_piezas = [np.array(sublista) for sublista in lista_piezas]
        array_tablero = np.array(lista_tablero)

        poblacion_inicial = HatagramPuzzle.generarPoblacionInicial(array_tablero, array_piezas, tamano_poblacion)
        poblacion_valida = HatagramPuzzle.marcarInvalidos(poblacion_inicial, array_tablero, array_piezas)
        poblacion_final = HatagramPuzzle.GA_dirigido(poblacion_valida, array_tablero, array_piezas, tamano_torneo, prob_cruce, prob_mutacion, num_generaciones)
        poblacion_final_valida = HatagramPuzzle.marcarInvalidos(poblacion_final, array_tablero, array_piezas)
        mejor_individuo = HatagramPuzzle.seleccion_por_torneo(poblacion_final_valida, tamano_torneo, array_tablero, array_piezas)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        dar_pista_puzzle(mejor_individuo)


def dar_pista_puzzle(mejor_individuo):
    try:
        pieza = []
        for i in range(len(mejor_individuo)):
            if mejor_individuo[i][0] != -1:
                pieza_idx = i + 1 
                pieza = mejor_individuo[i]

        texto = f"La pieza {pieza_idx} se coloca en la posición del tablero: {pieza[0]},{pieza[1]} con el giro número: {pieza[2]}"
        label_solucion = Label(frame_resolver_puzzle, text=texto)
        label_solucion.grid(row=35,column=0)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def guardar_tablero():
    try:
        filas = int(numero_filas_puzzle.get())
        columnas = int(numero_columnas_puzzle.get())
        tablero_init = dibujar_tablero(filas, columnas)
        
        boton_guardar_tab = Button(frame_resolver_puzzle, text="Guardar tablero", command=lambda:guardar_tablero_total(tablero_init))
        boton_guardar_tab.grid(row=filas+5, column=1, columnspan=10, padx=10, pady=10, sticky="nsew")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")


def guardar_tablero_total(casillas):
    try:
        global estado_real
        filas = int(numero_filas_puzzle.get())

        estado_real = tablero_to_array_puzzle(casillas)

        piezas_label =  Label(frame_resolver_puzzle, text="Número de piezas:",bg='MediumPurple1', font=("Helvetica", 12))
        piezas_label.grid(row=filas + 6, column=1, columnspan=5, padx=10, pady=10, sticky="nsew")
        numero_piezas_entry.grid(row=filas + 6, column=6, columnspan=5, padx=10, pady=10, sticky="nsew")
        boton_piezas.grid(row=filas + 7, column=1 , columnspan=5, padx=10, pady=10, sticky="nsew")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def dibujar_pieza(filas, columnas):
    try:
        pieza = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                boton =  Button(frame_resolver_puzzle, width=2, height=2, bg="white",
                                command=lambda i=i, j=j: sel(i, j, pieza))
                boton.grid(row=i + 18, column=j+1, sticky="nsew")
                fila.append(boton)
            pieza.append(fila)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    return pieza

def inicializar_piezas():
    global contador_piezas
    contador_piezas = 0

    filas_pieza_label.grid(row=11, column=1, columnspan=5, padx=10,pady=10, sticky="nsew")
    numero_filas_pieza.grid(row=11, column=6, columnspan=5, padx=10,pady=10, sticky="nsew")
    columnas_pieza_label.grid(row=12, column=1, columnspan=5, padx=10,pady=10, sticky="nsew")
    numero_columnas_pieza.grid(row=12, column=6, columnspan=5, padx=10,pady=10, sticky="nsew")
    boton_siguiente_pieza.grid(row=13, column=1, columnspan=5, padx=10,pady=10, sticky="nsew")

def procesar_pieza():
    global contador_piezas
    try:
        filas = int(numero_filas_pieza.get())
        columnas = int(numero_columnas_pieza.get())
        pieza = dibujar_pieza(filas, columnas)

        boton_guardar_pieza =  Button(frame_resolver_puzzle, text="Guardar y seguir",
                                        command=lambda: guardar_pieza(pieza, boton_guardar_pieza))
        boton_guardar_pieza.grid(row=20 + filas, column=1, columnspan=5, padx=10,pady=10, sticky="nsew")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")


def guardar_pieza(pieza,boton_guardar_pieza):
    global contador_piezas
    try:
        numero_piezas = int(numero_piezas_entry.get())

        p = pieza_to_array(pieza, contador_piezas)
        lista_piezas.append(p)

        contador_piezas += 1
        if contador_piezas == numero_piezas:
            boton_siguiente_pieza.config(state= DISABLED)
            boton_guardar_pieza.config(state= DISABLED)
            boton_generar_resultado = Button(frame_resolver_puzzle, text="Resolver", command=lambda:resolver_puzzle(lista_piezas, estado_real))
            boton_generar_resultado.grid(row=30, column=1,columnspan=5, padx=10,pady=10, sticky="nsew")
        else:
            limpiar_pieza()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")


def limpiar_pieza():
    numero_filas_pieza.delete(0, END)
    numero_columnas_pieza.delete(0, END)

def pieza_to_array(elementos, n_pieza):
    n_filas = len(elementos)
    n_columnas = len(elementos[0])
    estado = []

    for i in range(n_filas):
        elem_fila = []
        for j in range(n_columnas):
            if elementos[i][j].cget("bg") == "black":
                elem_fila.append(-1)
            elif elementos[i][j].cget("bg") == "white":
                elem_fila.append(n_pieza + 1)
        estado.append(elem_fila)
    return estado






 



root = Tk()
root.title("Menú principal")
root.geometry("1200x1000")


img_back = PhotoImage(file="assets\\back.png")
imagen_jarras = PhotoImage(file="assets\\water_pitchers.PNG")
imagen_pelota = PhotoImage(file="assets\\get_the_ball_out.PNG")
imagen_puzzle_8 = PhotoImage(file="assets\\puzzle_8.PNG")
imagen_stomp = PhotoImage(file="assets\\stomp.PNG")
imagen_hatgram = PhotoImage(file="assets\\hatgram.PNG")

frame_jarras = Frame(root, bg='lightblue')
frame_pelota = Frame(root, bg='lightgreen')
frame_imagen = Frame(root, bg='lightyellow')
frame_stomp = Frame(root, bg='lightpink')
frame_puzzle = Frame(root, bg='MediumPurple1')
frame_main_menu = Frame(root, bg='lightyellow')
frame_resolver_jarras = Frame(root, bg='lightblue')
frame_generar_jarras = Frame(root, bg='lightblue')
frame_resolver_pelota = Frame(root,bg='lightgreen')
frame_generar_pelota= Frame(root, bg='lightgreen')
frame_resolver_imagen= Frame(root, bg='lightyellow')
frame_generar_imagen = Frame(root, bg='lightyellow')
frame_resolver_puzzle = Frame(root, bg='MediumPurple1')
frame_generar_puzzle = Frame(root, bg='MediumPurple1')
frame_resolver_stomp = Frame(root, bg='lightpink')
frame_generar_stomp = Frame(root, bg='lightpink')


lista_frames = [frame_jarras, frame_pelota, frame_imagen, frame_stomp, frame_puzzle, frame_main_menu, frame_resolver_jarras, frame_generar_jarras,frame_resolver_pelota, frame_generar_pelota,
                frame_generar_imagen,frame_resolver_imagen,frame_resolver_puzzle,frame_generar_puzzle, frame_generar_stomp, frame_resolver_stomp]
for frame in lista_frames:
    frame.place(x=0, y=0, width=1200, height=1000)



########################################################################################################################
######################################   JARRAS    #####################################################################
########################################################################################################################
##Añadimos elementos al frame general del problema de las jarras
frame_jarras.grid_columnconfigure(0, weight=0)
frame_jarras.grid_columnconfigure(1, weight=1)
frame_jarras.grid_columnconfigure(2, weight=1)
label1 = Label(frame_jarras, text="WATER PITCHERS", bg='lightblue', font=("Helvetica", 16))
label_jarras = Label(frame_jarras, bg='lightblue', text="El puzle de las jarras consiste en que hay tres jarras de las que sabemos la capacidad máxima de líquido que pueden contener. Se nos da un estado inicial y un estado objetivo, en los que se determina la cantidad de líquido que tiene cada jarra. El juego consiste en llegar del estado inicial al estado objetivo mediante las acciones de mover el líquido contenido en las diferentes jarras de una a otra.", wraplength=500,font=("Helvetica", 12))
label_imagen = Label(frame_jarras,bg='lightblue', image=imagen_jarras)
button_main_menu = Button(frame_jarras, image=img_back, command=lambda: show_frame(frame_main_menu))
button_resolver_jarras = Button(frame_jarras, text="Resolver", command=lambda: show_frame(frame_resolver_jarras))
button_generar_jarras = Button(frame_jarras, text="Generar", command=lambda: show_frame(frame_generar_jarras))

button_main_menu.grid(row=0, column=0)
label1.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
label_imagen.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
label_jarras.grid(row= 2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
button_resolver_jarras.grid(row=3, column=1, pady=5,padx=5, sticky="nsew")
button_generar_jarras.grid(row=3, column=2, pady=5,padx=5, sticky="nsew")

##Añadimos elementos al frame de resolver jarras
frame_resolver_jarras.grid_columnconfigure(0, weight=0)
frame_resolver_jarras.grid_columnconfigure(1, weight=1)
frame_resolver_jarras.grid_columnconfigure(2, weight=1)
frame_resolver_jarras.grid_columnconfigure(3, weight=1)

label_resolver_jarras = Label(frame_resolver_jarras, text="RESOLVER WATER PITCHERS", bg='lightblue', font=("Helvetica", 16))
button_menu_jarras = Button(frame_resolver_jarras, image=img_back, command=lambda: show_frame(frame_jarras))
vol_jarra1_label = Label(frame_resolver_jarras,bg='lightblue', text="Capacidad máxima de la jarra 1:")
vcmd = (root.register(validate_numeric_input), '%P')
vol_jarra1 = Entry(frame_resolver_jarras, validate="key", validatecommand=vcmd)
vol_jarra2_label = Label(frame_resolver_jarras,bg='lightblue', text="Capacidad máxima de la jarra 2:")
vcmd = (root.register(validate_numeric_input), '%P')
vol_jarra2 = Entry(frame_resolver_jarras, validate="key", validatecommand=vcmd)
vol_jarra3_label = Label(frame_resolver_jarras,bg='lightblue', text="Capacidad máxima de la jarra 3:")
vcmd = (root.register(validate_numeric_input), '%P')
vol_jarra3 = Entry(frame_resolver_jarras, validate="key", validatecommand=vcmd)
s1_label = Label(frame_resolver_jarras, bg='lightblue',text="Contenido actual de la jarra 1:")
vcmd = (root.register(validate_numeric_input), '%P')
s1 = Entry(frame_resolver_jarras, validate="key", validatecommand=vcmd)
s2_label = Label(frame_resolver_jarras, bg='lightblue',text="Contenido actual de la jarra 2:")
vcmd = (root.register(validate_numeric_input), '%P')
s2 = Entry(frame_resolver_jarras, validate="key", validatecommand=vcmd)
s3_label = Label(frame_resolver_jarras,bg='lightblue', text="Contenido actual de la jarra 3:")
vcmd = (root.register(validate_numeric_input), '%P')
s3 = Entry(frame_resolver_jarras, validate="key", validatecommand=vcmd)
f1_label = Label(frame_resolver_jarras, bg='lightblue',text="Contenido final de la jarra 1:")
vcmd = (root.register(validate_numeric_input), '%P')
f1 = Entry(frame_resolver_jarras, validate="key", validatecommand=vcmd)
f2_label = Label(frame_resolver_jarras,bg='lightblue', text="Contenido final de la jarra 2:")
vcmd = (root.register(validate_numeric_input), '%P')
f2 = Entry(frame_resolver_jarras, validate="key", validatecommand=vcmd)
f3_label = Label(frame_resolver_jarras,bg='lightblue', text="Contenido final de la jarra 3:")
vcmd = (root.register(validate_numeric_input), '%P')
f3 = Entry(frame_resolver_jarras, validate="key", validatecommand=vcmd)
button_resolver = Button(frame_resolver_jarras, text="Resolver", command=resolver_jarras)
label_jarras_resolucion = Label(frame_resolver_jarras, bg='lightblue', text="")
label_jarras_resolucion_pasos = Label(frame_resolver_jarras, bg='lightblue', text="")

label_resolver_jarras.grid(row=0, column=1, columnspan=3,pady=10, padx=10, sticky="nsew")
button_menu_jarras.grid(row=0, column=0)
vol_jarra1_label.grid(row=1, column=1, pady=5, padx=5, sticky="nsew")
vol_jarra1.grid(row=2, column=1,pady=5, padx=5, sticky="nsew" )
vol_jarra2_label.grid(row=1, column=2, pady=5, padx=5, sticky="nsew")
vol_jarra2.grid(row=2, column=2, pady=5, padx=5, sticky="nsew")
vol_jarra3_label.grid(row=1, column=3, pady=5, padx=5, sticky="nsew")
vol_jarra3.grid(row=2, column=3, pady=5, padx=5, sticky="nsew")
s1_label.grid(row=3, column=1, pady=5, padx=5, sticky="nsew")
s1.grid(row=4, column=1, pady=5, padx=5, sticky="nsew")
s2_label.grid(row=3, column=2, pady=5, padx=5, sticky="nsew")
s2.grid(row=4, column=2, pady=5, padx=5, sticky="nsew")
s3_label.grid(row=3, column=3, pady=5, padx=5, sticky="nsew")
s3.grid(row=4, column=3, pady=5, padx=5, sticky="nsew")
f1_label.grid(row=5, column=1, pady=5, padx=5, sticky="nsew")
f1.grid(row=6, column=1, pady=5, padx=5, sticky="nsew")
f2_label.grid(row=5, column=2, pady=5, padx=5, sticky="nsew")
f2.grid(row=6, column=2, pady=5, padx=5, sticky="nsew")
f3_label.grid(row=5, column=3, pady=5, padx=5, sticky="nsew")
f3.grid(row=6, column=3, pady=5, padx=5, sticky="nsew")
button_resolver.grid(row=7, column=2, pady=10, padx=10, sticky="nsew")
label_jarras_resolucion.grid(row=8, column=2, pady=10, padx=10, sticky="nsew")
label_jarras_resolucion_pasos.grid(row=9, column=2,pady=10, padx=10, sticky="nsew" )



##Añadimos elementos al frame de generar el problema de las jarras
frame_generar_jarras.grid_columnconfigure(0, weight=0)
frame_generar_jarras.grid_columnconfigure(1, weight=1)
frame_generar_jarras.grid_columnconfigure(2, weight=1)

dificultades_puzzles = ["Fácil", "Intermedio", "Difícil", "Muy difícil"]
dificultad_seleccionada = StringVar(frame_generar_jarras)
dificultad_seleccionada.set("Selecciona una opción")
menu_dificultad = OptionMenu(frame_generar_jarras, dificultad_seleccionada, *dificultades_puzzles)
menu_dificultad.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
label_generar_jarras = Label(frame_generar_jarras, text="GENERAR WATER PITCHERS",bg="lightblue", font=("Helvetica", 16))
button_menu_jarras = Button(frame_generar_jarras, image=img_back, command=lambda: show_frame(frame_jarras))
label_generar_jarras_extra = Label(frame_generar_jarras, text="Seleccione la dificultad del puzle generado",bg="lightblue", font=("Helvetica", 12) )
label_generar_jarras.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
label_generar_jarras_extra.grid(row=1, column=1, columnspan=2, padx=10,pady=10, sticky="nsew")
button_menu_jarras.grid(row=0, column=0)
button_generar_jarras = Button(frame_generar_jarras, text="Generar Puzzle", command=lambda:generar_jarras(dificultad_seleccionada.get()))
button_generar_jarras.grid(row=2, column=2, padx=10,pady=10, sticky="nsew")



########################################################################################################################
######################################   PELOTA    #####################################################################
########################################################################################################################
frame_pelota.grid_columnconfigure(0, weight=0)
frame_pelota.grid_columnconfigure(1, weight=1)
frame_pelota.grid_columnconfigure(2, weight=1)


"""Añadimos contenido al frame de la opcion de pelota"""
label2 = Label(frame_pelota, text="GET THE BALL OUT", bg='lightgreen', font=("Helvetica", 16))
label_pelota = Label(frame_pelota, bg='lightgreen', wraplength=500,font=("Helvetica", 12), text="Este tipo de puzle consiste en, dado un tablero con piezas, una pelota, posiciones vacías y una posición objetivo para la pelota, conseguir mover la pelota de la posición inicial a la posición objetivo. Para ello hay que mover la pelota y/o mover las piezas para abrir camino a la pelota. ")
label_imagen_pelota = Label(frame_pelota,bg='lightgreen', image=imagen_pelota)
button_main_menu = Button(frame_pelota, image=img_back, command=lambda: show_frame(frame_main_menu))
button_resolver_pelota = Button(frame_pelota, text="Resolver", command=lambda: show_frame(frame_resolver_pelota))
button_generar_pelota = Button(frame_pelota, text="Generar", command=lambda: show_frame(frame_generar_pelota))
button_main_menu.grid(row=0, column=0)
label2.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
label_imagen_pelota.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
label_pelota.grid(row= 2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
button_resolver_pelota.grid(row=3, column=1, pady=5,padx=5, sticky="nsew")
button_generar_pelota.grid(row=3, column=2, pady=5,padx=5, sticky="nsew")



"""Añadimos contenido al frame de resolver pelota"""
frame_resolver_pelota.grid_columnconfigure(0, weight=0)
frame_resolver_pelota.grid_columnconfigure(1, weight=1)
frame_resolver_pelota.grid_columnconfigure(2, weight=1)
frame_resolver_pelota.grid_columnconfigure(3, weight=1)
frame_resolver_pelota.grid_columnconfigure(4, weight=1)

label_resolver_pelota = Label(frame_resolver_pelota, text="RESOLVER GET THE BALL OUT", font=("Helvetica", 16), bg='lightgreen')
button_menu_pelota = Button(frame_resolver_pelota, image=img_back, command=lambda: show_frame(frame_pelota))
filas_label_pelota = Label(frame_resolver_pelota, text="Numero de filas del tablero:",font=("Helvetica", 12), bg='lightgreen')
vcmd = (root.register(validate_numeric_input), '%P')
numero_filas_pelota = Entry(frame_resolver_pelota, textvariable= StringVar(value="2"), validate="key", validatecommand=vcmd)
columnas_label_pelota = Label(frame_resolver_pelota, text="Numero de columnas del tablero:",font=("Helvetica", 12), bg='lightgreen')
vcmd = (root.register(validate_numeric_input), '%P')
numero_columnas_pelota = Entry(frame_resolver_pelota, validate="key", validatecommand=vcmd)
button_generar_tablero_pelota = Button(frame_resolver_pelota, text="Dibujar tablero", command=dibujar_pelota)
label_pelota_resolucion = Label(frame_resolver_pelota, text="", bg='lightgreen',font=("Helvetica", 10))
label_pelota_resolucion_pasos = Label(frame_resolver_pelota, text="", bg='lightgreen',font=("Helvetica", 10))

button_menu_pelota.grid(row=0, column=0)
label_resolver_pelota.grid(row=0, column=1, columnspan=4, pady=10, padx=10, sticky="nsew")
filas_label_pelota.grid(row=1, column=1,columnspan=2, padx=10, pady=10, sticky="nsew")
numero_filas_pelota.grid(row=1, column=3, padx=10,pady=10, sticky="nsew")
columnas_label_pelota.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
numero_columnas_pelota.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")
button_generar_tablero_pelota.grid(row=3, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

calculo_fila_pelota = int(numero_filas_pelota.get()) + 7
label_pelota_resolucion.grid(row=calculo_fila_pelota + 10, column=1, columnspan=4, pady=10, padx=10, sticky="nsew")
label_pelota_resolucion_pasos.grid(row=calculo_fila_pelota + 11, column=1, columnspan=4, pady=10, padx=10, sticky="nsew")

"""Añadimos contenido al frame de generar pelota"""
frame_generar_pelota.grid_columnconfigure(0, weight=0)
frame_generar_pelota.grid_columnconfigure(1, weight=1)
frame_generar_pelota.grid_columnconfigure(2, weight=1)
label_generar_pelota = Label(frame_generar_pelota, text="GENERAR GET THE BALL OUT",bg="lightgreen", font=("Helvetica", 16))
label_generar_pelota_extra = Label(frame_generar_pelota, text="Seleccione la dificultad del puzle generado",bg="lightgreen", font=("Helvetica", 12) )
button_menu_pelota = Button(frame_generar_pelota, image=img_back, command=lambda: show_frame(frame_pelota))
label_generar_pelota.grid(row=0, column=1, padx=10, pady=10, columnspan=2, sticky="nsew")
button_menu_pelota.grid(row=0, column=0)
label_generar_pelota_extra.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
dificultades_puzzles = ["Fácil", "Intermedio", "Difícil", "Muy difícil"]
dificultad_seleccionada_pelota = StringVar(frame_generar_pelota)
dificultad_seleccionada_pelota.set("Selecciona una opcion")
menu_dificultad = OptionMenu(frame_generar_pelota, dificultad_seleccionada_pelota, *dificultades_puzzles)
menu_dificultad.grid(row=2, column=1, padx=10,pady=10, sticky="nsew")
button_generar_pelota = Button(frame_generar_pelota, text="Generar Puzzle", command=lambda:generar_pelota(dificultad_seleccionada_pelota.get()))
button_generar_pelota.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")





########################################################################################################################
######################################   PUZZLE 8  #####################################################################
########################################################################################################################
frame_imagen.grid_columnconfigure(0, weight=0)
frame_imagen.grid_columnconfigure(1, weight=1)
frame_imagen.grid_columnconfigure(2, weight=1)

"""Añadimos contenido al frame de la opcion de imagen"""
label3 = Label(frame_imagen, text="8/16-PUZZLE", bg='lightyellow', font=("Helvetica", 16))
label_imagen = Label(frame_imagen,bg='lightyellow', wraplength=500,font=("Helvetica", 12), text="El puzle del 8 consiste en completar un tablero cuadrado de 9 celdas con 8 fichas numeradas del 1 al 8 y una celda vacía. En realidad, a nivel de usuario, se le suele sustituir los números por partes de una imagen, aunque internamente deben tener un orden. Se nos da un estado inicial y mediante el movimiento de las fichas, deslizamiento mediante el uso de la celda vacía, hay que ordenar las fichas numeradas. Existe también otra variante de este puzle llamado el puzle 15, donde la única diferencia es el tamaño del tablero que es de 4x4.")
label_imagen_puzzle_8 = Label(frame_imagen, bg='lightyellow',image=imagen_puzzle_8)
button_main_menu = Button(frame_imagen, image=img_back, command=lambda: show_frame(frame_main_menu))
button_resolver_imagen = Button(frame_imagen, text="Resolver", command=lambda: show_frame(frame_resolver_imagen))
button_generar_imagen = Button(frame_imagen, text="Generar", command=lambda: show_frame(frame_generar_imagen))
button_main_menu.grid(row=0, column=0)
label3.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
label_imagen.grid(row= 2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
label_imagen_puzzle_8.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
button_resolver_imagen.grid(row=3, column=1, pady=5,padx=5, sticky="nsew")
button_generar_imagen.grid(row=3, column=2, pady=5,padx=5, sticky="nsew")



"""Añadimos contenido al frame de resolver imagen"""
frame_resolver_imagen.grid_columnconfigure(0, weight=0)
frame_resolver_imagen.grid_columnconfigure(1, weight=1)
frame_resolver_imagen.grid_columnconfigure(2, weight=1)
label_resolver_imagen = Label(frame_resolver_imagen, text="RESOLVER 8/16-PUZZLE", font=("Helvetica", 16), bg="lightyellow")
button_menu_imagen = Button(frame_resolver_imagen, image=img_back, command=lambda: show_frame(frame_imagen))
estado_imagen_label = Label(frame_resolver_imagen,font=("Helvetica", 12), bg="lightyellow", text="Inserte con comas el estado en el que se encuentra el problema, siendo 0 el hueco:")
vcmd = (root.register(validate_image_input), '%P')
estado_imagen = Entry(frame_resolver_imagen, validate="key", validatecommand=vcmd)
estado_imagen_objetivo_label = Label(frame_resolver_imagen, text="Inserte con comas el estado objetivo, siendo 0 el hueco:", font=("Helvetica", 12), bg="lightyellow")
vcmd = (root.register(validate_image_input), '%P')
estado_imagen_objetivo = Entry(frame_resolver_imagen, validate="key", validatecommand=vcmd)
button_resolver_imagen = Button(frame_resolver_imagen, text="Resolver", command=resolver_imagen)
label_imagen_resolucion = Label(frame_resolver_imagen, text="",  font=("Helvetica", 12), bg="lightyellow")
label_imagen_resolucion_pasos = Label(frame_resolver_imagen, text="", font=("Helvetica", 12), bg="lightyellow")

button_menu_imagen.grid(row=0, column=0)
label_resolver_imagen.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
estado_imagen_label.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
estado_imagen.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
estado_imagen_objetivo_label.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
estado_imagen_objetivo.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
button_resolver_imagen.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
label_imagen_resolucion.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
label_imagen_resolucion_pasos.grid(row=7, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")


"""Añadimos contenido al frame de generar imagen"""
frame_generar_imagen.grid_columnconfigure(0, weight=0)
frame_generar_imagen.grid_columnconfigure(1, weight=1)
frame_generar_imagen.grid_columnconfigure(2, weight=1)

label_generar_imagen = Label(frame_generar_imagen, text="GENERAR 8/16-PUZZLE", font=("Helvetica", 16), bg="lightyellow")
button_menu_imagen = Button(frame_generar_imagen, image=img_back, command=lambda: show_frame(frame_imagen))
label_generar_imagen.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
button_menu_imagen.grid(row=0, column=0)
label_dificultad_imagen = Label(frame_generar_imagen, text="Seleccione la dificultad del puzzle a generar", font=("Helvetica", 12), bg="lightyellow")
label_dificultad_imagen.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
dificultades_puzzles = ["Fácil", "Intermedio", "Difícil", "Muy difícil"]
dificultad_seleccionada_puzzle8 = StringVar(frame_generar_imagen)
dificultad_seleccionada_puzzle8.set("Selecciona una opcion")
menu_dificultad = OptionMenu(frame_generar_imagen, dificultad_seleccionada_puzzle8, *dificultades_puzzles)
menu_dificultad.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
button_generar_imagen = Button(frame_generar_imagen, text="Generar Puzzle", command=lambda:generar_imagen(dificultad_seleccionada_puzzle8.get()))
button_generar_imagen.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")




########################################################################################################################
######################################   STOMP     #####################################################################
########################################################################################################################
frame_stomp.grid_columnconfigure(0, weight=0)
frame_stomp.grid_columnconfigure(1, weight=1)
frame_stomp.grid_columnconfigure(2, weight=1)


"""Añadimos contenido al frame de la opcion de stomp"""
label4 = Label(frame_stomp, text="STOMP ON IT: FLIP PANELS", bg='lightpink', font=("Helvetica", 16))
label_stomp = Label(frame_stomp,bg='lightpink', wraplength=500,font=("Helvetica", 12),text="Este tipo de puzle consiste en: dado un tablero donde las diferentes posiciones pueden tomar dos valores, dos colores, conseguir formar la configuración de colores que se da en el estado objetivo mediante la acción de pisar casillas.  Al pisar una casilla cambian de color sus cuatro casillas adyacentes y la misma.")
label_image_stomp = Label(frame_stomp,bg='lightpink', image=imagen_stomp)
button_main_menu = Button(frame_stomp, image=img_back, command=lambda: show_frame(frame_main_menu))
button_resolver_stomp = Button(frame_stomp, text="Resolver", command=lambda: show_frame(frame_resolver_stomp))
button_generar_stomp = Button(frame_stomp, text="Generar", command=lambda: show_frame(frame_generar_stomp))
button_main_menu.grid(row=0, column=0)
label4.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
label_image_stomp.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
label_stomp.grid(row= 2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
button_resolver_stomp.grid(row=3, column=1, pady=5,padx=5, sticky="nsew")
button_generar_stomp.grid(row=3, column=2, pady=5,padx=5, sticky="nsew")


"""Añadimos contenido al frame de resolver stomp"""
frame_resolver_stomp.grid_columnconfigure(0, weight=0)
frame_resolver_stomp.grid_columnconfigure(1, weight=1)
frame_resolver_stomp.grid_columnconfigure(2, weight=1)
frame_resolver_stomp.grid_columnconfigure(3, weight=1)
frame_resolver_stomp.grid_columnconfigure(4, weight=1)
frame_resolver_stomp.grid_columnconfigure(5, weight=1)
frame_resolver_stomp.grid_columnconfigure(6, weight=1)
frame_resolver_stomp.grid_columnconfigure(7, weight=1)
frame_resolver_stomp.grid_columnconfigure(8, weight=1)
frame_resolver_stomp.grid_columnconfigure(9, weight=1)
frame_resolver_stomp.grid_columnconfigure(10, weight=1)
frame_resolver_stomp.grid_columnconfigure(11, weight=1)

label_resolver_stomp = Label(frame_resolver_stomp, text="RESOLVER STOMP ON IT: FLIP PANELS", bg='lightpink', font=("Helvetica", 16))
button_menu_stomp= Button(frame_resolver_stomp, image=img_back, command=lambda: show_frame(frame_stomp))
filas_label = Label(frame_resolver_stomp, text="Numero de filas del tablero:",bg='lightpink', font=("Helvetica", 12))
vcmd = (root.register(validate_numeric_input), '%P')
numero_filas = Entry(frame_resolver_stomp, textvariable= StringVar(value="5"), validate="key", validatecommand=vcmd)
columnas_label = Label(frame_resolver_stomp, text="Numero de columnas del tablero:", bg='lightpink', font=("Helvetica", 12))
vcmd = (root.register(validate_numeric_input), '%P')
numero_columnas = Entry(frame_resolver_stomp, validate="key", validatecommand=vcmd)
button_generar_tablero = Button(frame_resolver_stomp, text="Dibujar tablero", command=dibujar_stomp)
label_stomp_resolucion = Label(frame_resolver_stomp, text="",bg='lightpink', font=("Helvetica", 12))
label_stomp_resolucion_pasos = Label(frame_resolver_stomp, text="",bg='lightpink', font=("Helvetica", 12))

button_menu_stomp.grid(row=0, column=0)
label_resolver_stomp.grid(row=0, column=1, columnspan=10, pady=10, padx=10, sticky="nsew")
filas_label.grid(row=1, column=1,columnspan=5, padx=10, pady=10, sticky="nsew")
numero_filas.grid(row=1, column=6, columnspan=5, padx=10, pady=10, sticky="nsew")
columnas_label.grid(row=2, column=1, columnspan=5, padx=10, pady=10, sticky="nsew")
numero_columnas.grid(row=2, column=6,columnspan=5, padx=10, pady=10, sticky="nsew")
button_generar_tablero.grid(row=3, column=1, columnspan=10, pady=10, padx=10, sticky="nsew")

calculo_fila = int(numero_filas.get()) + 7
label_stomp_resolucion.grid(row=calculo_fila +2, column=1, columnspan=10, padx=10, pady=10, sticky="nsew")
label_stomp_resolucion_pasos.grid(row=calculo_fila +3, column=1, columnspan=10, padx=10, pady=10, sticky="nsew")



"""Añadimos contenido al frame de generar stomp"""
frame_generar_stomp.grid_columnconfigure(0, weight=0)
frame_generar_stomp.grid_columnconfigure(1, weight=1)
frame_generar_stomp.grid_columnconfigure(2, weight=1)
label_generar_stomp = Label(frame_generar_stomp, text="GENERAR STOMP ON IT: FLIP PANELS", bg='lightpink', font=("Helvetica", 16))
button_menu_stomp = Button(frame_generar_stomp, image=img_back, command=lambda: show_frame(frame_stomp))
label_generar_stomp.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
button_menu_stomp.grid(row=0, column=0)
label_dificultad_stomp = Label(frame_generar_stomp, text="Seleccione la dificultad del puzzle a generar", bg='lightpink', font=("Helvetica", 12))
label_dificultad_stomp.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
dificultades_puzzles = ["Fácil", "Intermedio", "Difícil", "Muy difícil"]
dificultad_seleccionada_stomp = StringVar(frame_generar_stomp)
dificultad_seleccionada_stomp.set("Selecciona una opcion")
menu_dificultad = OptionMenu(frame_generar_stomp, dificultad_seleccionada_stomp, *dificultades_puzzles)
menu_dificultad.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
button_generar_imagen = Button(frame_generar_stomp, text="Generar Puzzle", command=lambda:generar_stomp(dificultad_seleccionada_stomp.get()))
button_generar_imagen.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")



########################################################################################################################
######################################  HATGRAM    ####################################################################
########################################################################################################################

frame_puzzle.grid_columnconfigure(0, weight=0)
frame_puzzle.grid_columnconfigure(1, weight=1)
frame_puzzle.grid_columnconfigure(2, weight=1)


"""Añadimos contenido al frame de la opcion de puzzle"""
label5 = Label(frame_puzzle, text="HATGRAM", bg='MediumPurple1', font=("Helvetica", 16))
label_puzzle = Label(frame_puzzle, bg='MediumPurple1', wraplength=500,font=("Helvetica", 12), text="Este tipo de puzle consiste en, dado un tablero con posiciones vacías y posiciones en las que no se pueden poner piezas, y una lista de piezas de diferentes tamaños y formas, llenar el tablero utilizando todas las piezas teniendo en cuenta que las piezas se pueden rotar y voltear.")
label_imagen_puzzle = Label(frame_puzzle,bg='MediumPurple1', image=imagen_hatgram)
button_main_menu = Button(frame_puzzle, image=img_back, command=lambda: show_frame(frame_main_menu))
button_resolver_puzzle = Button(frame_puzzle, text="Resolver",command=lambda: show_frame(frame_resolver_puzzle))

button_main_menu.grid(row=0, column=0)
label5.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
label_imagen_puzzle.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
label_puzzle.grid(row= 2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
button_resolver_puzzle.grid(row= 3, column=1, columnspan=2,pady=5,padx=5, sticky="nsew")


"""Añadimos contenido al frame de resolver puzzle"""
frame_puzzle.grid_columnconfigure(0, weight=0)
frame_puzzle.grid_columnconfigure(1, weight=1)
frame_puzzle.grid_columnconfigure(2, weight=1)
label_resolver_puzzle = Label(frame_resolver_puzzle, text="RESOLVER HATGRAM",bg='MediumPurple1', font=("Helvetica", 16))
label_resolver_puzzle.grid(row=0, column=1, columnspan=10, padx=10, pady=10, sticky="nsew")
button_menu_puzzle = Button(frame_resolver_puzzle, image=img_back, command=lambda: show_frame(frame_puzzle))

filas_label = Label(frame_resolver_puzzle, text="Número de filas del tablero:")
button_menu_puzzle.grid(row=0, column=0)
filas_label.grid(row=1, column=1, columnspan=5, padx=10, pady=10, sticky="nsew")

numero_filas_puzzle = Entry(frame_resolver_puzzle)
numero_filas_puzzle.grid(row=1, column=6, columnspan=5, padx=10, pady=10, sticky="nsew")

columnas_label =   Label(frame_resolver_puzzle, text="Número de columnas del tablero:")
columnas_label.grid(row=2, column=1, columnspan=5, padx=10, pady=10, sticky="nsew")
numero_columnas_puzzle =   Entry(frame_resolver_puzzle)
numero_columnas_puzzle.grid(row=2, column=6, columnspan=5, padx=10, pady=10, sticky="nsew")

boton_generar_tablero =   Button(frame_resolver_puzzle, text="OK", command=guardar_tablero)
boton_generar_tablero.grid(row=3, column=1, columnspan=10, padx=10, pady=10, sticky="nsew")
numero_piezas_entry =   Entry(frame_resolver_puzzle)
boton_piezas =   Button(frame_resolver_puzzle, text="OK", command=inicializar_piezas)
filas_pieza_label =   Label(frame_resolver_puzzle, text="Número de filas de la pieza:")
numero_filas_pieza =   Entry(frame_resolver_puzzle)
columnas_pieza_label =   Label(frame_resolver_puzzle, text="Número de columnas de la pieza:")
numero_columnas_pieza =   Entry(frame_resolver_puzzle)
boton_siguiente_pieza =   Button(frame_resolver_puzzle, text="Siguiente pieza", command=procesar_pieza)









########################################################################################################################
######################################   MAIN MENU    #####################################################################
########################################################################################################################
frame_main_menu.grid_columnconfigure(0, weight=1)
frame_main_menu.grid_columnconfigure(1, weight=1)
titulo = Label(frame_main_menu, text="Herramienta de generación y resolución de puzles", font=("Helvetica", 16), bg="lightyellow")
titulo.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")
label_menu = Label(frame_main_menu, text="Seleccione un tipo de puzzle:",font=("Helvetica", 12), bg="lightyellow")
label_menu.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")
button_opcion1 = Button(frame_main_menu, text="Jarras", command=lambda: show_frame(frame_jarras))
button_opcion1.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")
button_opcion2 = Button(frame_main_menu, text="Pelota", command=lambda: show_frame(frame_pelota))
button_opcion2.grid(row=2, column=1, pady=5, padx=5, sticky="nsew")
button_opcion3 = Button(frame_main_menu, text="8/16-Puzzle", command=lambda: show_frame(frame_imagen))
button_opcion3.grid(row=3, column=0, pady=5,padx=5, sticky="nsew")
button_opcion4 = Button(frame_main_menu, text="Stomp on it", command=lambda: show_frame(frame_stomp))
button_opcion4.grid(row=3, column=1, pady=5,padx=5, sticky="nsew")
button_opcion5 = Button(frame_main_menu, text="Hatgram", command=lambda: show_frame(frame_puzzle))
button_opcion5.grid(row=4, column=0, pady=5,padx=5, sticky="nsew")




show_frame(frame_main_menu)
root.mainloop()
