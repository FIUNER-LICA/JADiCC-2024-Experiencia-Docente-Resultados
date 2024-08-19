import nltk
from abc import ABC, abstractmethod
import os 
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter


class Graficador(ABC):

    def __init__(self, p_nombre, p_formato, p_ruta):
        self.__nombre= p_nombre
        self.__formato= p_formato
        self.__ruta= p_ruta
    
    @abstractmethod
    def graficar_y_guardar(self, lista):
        pass


class GraficadorPastelYBarras (Graficador):

    def __init__(self, p_nombre, p_formato,p_lista_datos, p_ruta=None):
       super().__init__(p_nombre, p_formato, p_ruta)
       self.__lista= p_lista_datos
       self.__formato= p_formato
       if p_ruta is None:
            self.__ruta = os.path.join("static\estadistica", f"{p_nombre}.png")
       else:
            self.__ruta = os.path.join("static\estadistica", p_ruta)
       self.graficar_y_guardar()

    def graficar_y_guardar(self):
       lista_porcentajes=[]
       lista_estados=[]
       for n in range(len(self.__lista)):
          lista_porcentajes.append(self.__lista[n][1])
          lista_estados.append(self.__lista[n][0])
       y = np.array(lista_porcentajes)
       plt.figure()          # Crea una nueva figura para evitar solapamientos
       if self.__formato=="pastel":
            plt.pie(y, labels=[f"Reclamos en estado:{i}" for i in lista_estados], autopct='%1.1f%%')
       if self.__formato=="barras":
            plt.hist(y, bins=10)
            plt.xlabel('Reclamos')
            plt.ylabel('Frecuencia')
            plt.title('Distribución')
            plt.grid()
       plt.savefig(self.__ruta)
       
    #    plt.show()
       plt.close()


class GraficadorNubeDePalabras(Graficador):

    def __init__(self, p_nombre, p_palabras_frecuentes, p_ruta=None):
        super().__init__(p_nombre, "nube", p_ruta)
        self.__palabras_frecuentes = p_palabras_frecuentes
        if p_ruta is None:
            self.__ruta = os.path.join("static", "estadistica", f"{p_nombre}.png")
        else:
            self.__ruta = os.path.join("static", "estadistica", p_ruta)
        self.graficar_y_guardar()

    def graficar_y_guardar(self):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(self.__palabras_frecuentes)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(self.__ruta, format='png')
        plt.close()

# if __name__ == "__main__":
#    lista= [["en proceso",23],["pendiente",56],["invalido", 34], ["resuelto",10]]
#    GraficadorPastelYBarras("grafico", "pastel",lista)

