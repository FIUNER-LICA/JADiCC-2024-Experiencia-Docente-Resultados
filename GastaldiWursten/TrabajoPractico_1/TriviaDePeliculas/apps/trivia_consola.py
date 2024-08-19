# -*- coding: utf-8 -*-
"""
Created on Thu Mar 9 13:12:19 2023

@author: je_su
"""

from modules.funciones import cargar_diccionario_frases_desde_archivo , obtener_partida_trivia_frases , obtener_respuesta_triva_consola
import datetime

OPCIONES = """
#######################################
#  Películas: Preguntas y respuestas  #
#######################################
Elige una opción
1 - Mostrar lista de películas.
2 - ¡Trivia de película!
3 - Mostrar secuencia de opciones seleccionadas previamente.
4 - Borrar historial de opciones.
5 - Salir

"""

RUTA = "./data/"
ARCHIVO = "frases_de_peliculas.txt"

def main():

    diccionario_frases = {}
    historial_actual = ""
    salir = False

    # cargar_lista_desde_archivo(RUTA + ARCHIVO, lista_libros) 
    try:
        diccionario_frases = cargar_diccionario_frases_desde_archivo(RUTA + ARCHIVO)            
    except FileNotFoundError:
        with open(RUTA + ARCHIVO, "w") as archi:
            pass
    
       
      
    while not salir:

        opcion = input(OPCIONES)
        
        historial_actual = historial_actual + str(opcion) + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M\n')

        if opcion == "1":
            if len(diccionario_frases) == 0:
                print("No hay frases de peliculas alamacenadas")
            else:
                print("\n# Peliculas Disponibles: \n")
                for indice,pelicula in enumerate(sorted(set(list(diccionario_frases.values())))):
                    print(str(indice + 1), "-" , pelicula ,"\n")

        elif opcion == "2":
            
            frases_disponibles = list(diccionario_frases.keys())

            nro_frases_a_jugar = int(input("Ingrese el numero de frases de la trivia:"))

            while 3 > nro_frases_a_jugar or  nro_frases_a_jugar > 10:
                print("Numero invalido!")
                nro_frases_a_jugar = int(input("Ingrese el numero de frases de la trivia:"))

            for _ in range(nro_frases_a_jugar):

                frase_en_juego, lista_opciones = obtener_partida_trivia_frases(diccionario_frases , frases_disponibles)

                respuesta = obtener_respuesta_triva_consola(frase_en_juego, lista_opciones)

                if respuesta != diccionario_frases[frase_en_juego]:
                 print(f"    !!! Mal - Respuesta Incorrecta !!! - La respuesta era: {diccionario_frases[frase_en_juego]}")
                else:
                 print("     !!! Muy bien - Respuesta Correcta !!!")

        elif opcion == "3":

            #Se carga el historial de las ejecuciones anteriores
            historial_anterior = ""
            try:
                with open(RUTA+ "historial.txt", "r") as archi_historial:
                    historial_anterior = archi_historial.read()           
            except FileNotFoundError:
                with open(RUTA + "historial.txt", "w") as archi_historial:
                    pass
            
            print("\nHistorial de opciones: ")
            print(historial_anterior + historial_actual)

        elif opcion == "4":

            with open(RUTA + "historial.txt", "w") as archi_historial:
                    pass
            
            historial_actual = ""
            
            print("\n!!! Se ha borrado el historial !!!")
        
        elif opcion == "5":

            with open(RUTA + "historial.txt", "a", encoding="utf-8") as archi_historial:
                archi_historial.write(historial_actual)

            print("\n!!!  Ha salido del juego , buena suerte !!!")
            salir = True
        
        else:
            print("\nLa opción ingresada no es correcta")




if __name__ == "__main__":
    main()