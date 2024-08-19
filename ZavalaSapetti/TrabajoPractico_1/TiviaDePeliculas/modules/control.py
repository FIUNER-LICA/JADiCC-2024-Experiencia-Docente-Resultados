import os
import random
from datetime import datetime


def cargar_lista_desde_archivo(archivo):
    """Función que lee las frases y peliculas desde un archivo
    y lo carga a una lista.
    """
    frases_peliculas = []
    peliculas = []
    with open (archivo,'r', encoding='utf-8') as file:
        lineas = file.readlines()
        for linea in lineas:
            frase, movie = linea.strip().split(";")
            if not [frase,movie] in frases_peliculas:
                frases_peliculas.append([frase,movie])
            if not movie in peliculas:
                peliculas.append(movie)
    peliculas.sort()
    print("PELICULAS CARGADAS")
    return frases_peliculas, peliculas

def obtener_trivia(n : int, frases_peliculas):
    """
    La función genera una trivia de n preguntas sobre películas. 
    La trivia se compone de una pregunta y tres opciones, 
    una de las cuales es la respuesta correcta.

    Parámetros:
    - n (int): El número de rondas de trivia que se desea generar.
    #Que tambien reciba frases_peliculas

    Retorna:
    Una lista de listas que contiene la trivia generada.
    Cada sublista representa una ronda de trivia y contiene la pregunta
    seguida de tres opciones de respuesta y la respuesta correcta.
    """
    trivia = []
    usadas = []
    for i in range(n):
        print(f"RONDA {i+1}")
        posiciones = [] #guarda los índices de las preguntas seleccionadas
        pos = random.randint(0, len(frases_peliculas)-1)

        while len(posiciones) < 3:
            if pos not in usadas:
                posiciones.append(pos)
                usadas.append(pos)
            pos = random.randint(0, len(frases_peliculas)-1) 

        pos = posiciones[random.randint(0, len(posiciones))-1] #se selecciona aleatoriamente una de las preguntas para ser la pregunta principal de esta ronda

        ronda = [] #La pregunta principal se agrega a esta lista y se imprime en la consola

        ronda.append(frases_peliculas[pos][0])
        print(frases_peliculas[pos][0])

        for i in posiciones:
            ronda.append(frases_peliculas[i][1])
            print(f"{frases_peliculas[i][1]} OPCION {i+1}")
        print(f"{frases_peliculas[pos][1]} RESPUESTA")
        ronda.append(frases_peliculas[pos][1])
        trivia.append(ronda)

    return trivia

def getTime():
    """
    Obtiene la fecha y hora actual. Y retorna Una cadena de texto que representa 
    la fecha y hora actual en el formato "dd/mm/yy HH:MM".
    """
    
    now = datetime.now()
    return  now.strftime("%d/%m/%y %H:%M")

def getEstadisticasGlobales(registro):
    """
    Calcula las estadísticas globales de la trivia.
    
    Parámetros:
    Registros

    Retorna:
    Una tupla con dos enteros: el número total de aciertos y el número
    total de intentos realizados en la trivia.
    """
    aciertos = 0
    intentos = 0
    for r in registro:
        a = r[1].split('/')
        aciertos += int(a[0])
        intentos += int(a[1])

    return aciertos,intentos-aciertos



def getEstadistiicasPorFecha(registro):
    """
    Calcula las estadísticas de aciertos e intentos por fecha.

    Argumentos:
    Registros

    Retorna:
    Una lista de tres listas:
    La primera lista contiene las fechas en las que se registraron
    intentos de trivia en formato dd/mm/yy.
    La segunda lista contiene el número total de aciertos para cada fecha.
    La tercera lista contiene el número total de intentos menos aciertos
    para cada fecha.
    """
    fechas = {}

    for r in registro:
        a = r[1].split('/') #Así obtenemos número de aciertos a[0] y el número total de intentos a[1]
        fecha = r[2].split(' ')[0]
        if not fecha in fechas.keys():
            fechas[fecha] = []
            fechas[fecha].append(int(a[0])) #aciertos para esa fecha 
            fechas[fecha].append(int(a[1]) - int(a[0])) #desaciertos para esa fecha





        else:
            fechas[fecha][0]+=int(a[0])
            fechas[fecha][1]+=(int(a[1]) - int(a[0]))

    f = []
    a = []
    d = []

    for fecha,valor in fechas.items():
        f.append([int(i) for i in fecha.split('/')])
        a.append(valor[0])
        d.append(valor[1])

    return f,a,d

def guardar_registro_en_archivo(nombre_archivo, usuario,respuesta,date): 
    """Guarda la información de cada jugada en archivo
    """  
    ruta_completa = os.path.join('data', nombre_archivo)
 
    with open(ruta_completa, "a") as archi:
        archi.write(f"{usuario},{respuesta},{date}\n")

def cargar_registro_desde_archivo(nombre_archivo):
    """Función que lee la información de los libros desde un archivo
    y lo carga a una lista.
    """
    with open(nombre_archivo, "r") as archi:
        lista_registros = []
        for linea in archi:
            lineas = linea.rstrip().split(',') 
            lista_registros.append(lineas)
    
    return lista_registros



if __name__ == "__main__":
    b = cargar_registro_desde_archivo("jugadas_historicas")
    print(b)




