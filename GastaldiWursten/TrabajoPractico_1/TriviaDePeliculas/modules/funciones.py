from random import randint, shuffle

def cargar_diccionario_frases_desde_archivo(nombre_archivo:str):
    """Función que lee las frases y sus respectivos tìtulos de las peliculas desde un archivo
    , los carga y devuelve en un diccionario donde la clave es la frase y el valor el título de la pelicula.
    """
    diccionario_frases = {}
    with open(nombre_archivo, "r", encoding="utf-8") as archi:
        for linea in archi:
            frase = linea.rstrip().split(';')
            diccionario_frases[frase[0]] = frase[1].title()
            
    return  diccionario_frases

def obtener_respuesta_triva_consola(p_frase_en_juego:str , p_lista_opciones:list):
    """Función que muestra por consola la frase en juego y tres opciones, devolviendo la elegida por el usuario.
    """


    OPCIONES = f"""
    #######################################
    #  {p_frase_en_juego}  #
    #######################################
    Elige una opción
    1 - {p_lista_opciones[0]}
    2 - {p_lista_opciones[1]}
    3 - {p_lista_opciones[2]}

    """
    opcion_elegida = int(input(OPCIONES))

    while not (opcion_elegida == 1  or opcion_elegida == 2 or opcion_elegida == 3):
        opcion_elegida = int(input("Ingrese opcion válida: "))
    

    return p_lista_opciones[opcion_elegida-1]

    

def obtener_partida_trivia_frases(pdiccionario_frases, pfrases_disponibles):
    """Función que elige una frase para jugar, la devuelve y además una lista de tres opciones.
    """

    #Se selecciona al azar una frase disponible
    frase_en_juego = pfrases_disponibles.pop(randint(0,len(pfrases_disponibles)-1))

    respuesta_correcta = pdiccionario_frases[frase_en_juego]

    #Se obbtiene una lista con las respuestas incorrectas
    respuestas_incorrectas = list(set(list(pdiccionario_frases.values())).difference(set([respuesta_correcta])))

    #Se mezclan para luego seleccionar 2 al azar
    shuffle(respuestas_incorrectas)

    lista_opciones = [respuesta_correcta , respuestas_incorrectas.pop() , respuestas_incorrectas.pop() ]

    #Se mezclan la opciones
    shuffle(lista_opciones)

    return frase_en_juego, lista_opciones

def guardar_puntaje_en_archivo(p_ruta_nombre_archivo:str, p_puntaje:str, p_nombre:str, p_fecha_hora_partida:str):
    """Función que guarda el puntaje de aciertos/total , el nombre del jugador y la fecha de la partida en
    un archivo de texto.
    """

    with open(p_ruta_nombre_archivo, "a") as archivo:
        archivo.write( p_nombre + " " + p_puntaje + " " +  p_fecha_hora_partida + "\n")

def cargar_resultados_historicos_de_archvio(p_ruta_nombre_archivo:str):
    """Función que carga los resultados desde un archivo de texto y devuelve cada linea
    en una lista.
    """
    resultados = []
    with open(p_ruta_nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            resultados.append(linea)
            
    return  resultados


                                 
                        




                                    





                    
