from abc import ABC, abstractmethod
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import matplotlib.colors as mcolors
from PIL import Image
import numpy as np

class Graficador(ABC):
    """ Clase que modela un graficador que guarda la grafica en un archivo en una ruta.
    ------------------------------------------------
    Atributos:
    * ancho: int
    * alto: int
    * ruta: String
    * nombre: String
    * formato: String

    """
    def __init__(self,p_ancho, p_alto, p_ruta, p_nombre, p_formato) -> None:
        self.__ancho = p_ancho
        self.__alto = p_alto
        self.__ruta = p_ruta
        self.__nombre= p_nombre
        self.__formato = p_formato

    @property
    def ancho(self):
        return self.__ancho
    
    @ancho.setter
    def ancho (self, p_ancho):
        self.__ancho = p_ancho
    
    @property
    def alto(self):
        return self.__alto
    
    @alto.setter
    def alto (self, p_alto):
        self.__alto= p_alto

    @property
    def ruta(self):
        return self.__ruta
    
    @ruta.setter
    def ruta (self, p_ruta):
        self.__ruta= p_ruta

    @property
    def ruta(self):
        return self.__ruta
    
    @ruta.setter
    def ruta (self, p_ruta):
        self.__ruta= p_ruta
    
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre (self, p_nombre):
        self.__nombre = p_nombre

    @property
    def formato(self):
        return self.__formato
    
    @formato.setter
    def formato (self, p_formato):
        self.__formato = p_formato
    

    @abstractmethod   
    def graficar_y_guardar(self):
        """Metodo que crea la gráfica y la guarda en un archivo de self.formato con el nombre de self.nombre 
        en la ruta de self.ruta"""
        pass


class GraficadorDeNubeDePalabras(Graficador):
    """ Clase que modela un graficador de nubes de palabras
    ------------------------------------------------
    Atributos:
    * ancho: int
    * alto: int
    * ruta: String
    * nombre: String
    * formato: String
    * dict_palabras_frecuencias: dict(keys: String ,values: int) // Representa las palabras y las frecuencias asociadas

    """
    def __init__(self, p_dict_palabras_frecuencias, p_ruta , p_nombre,  p_formato , p_ancho = 1200 , p_alto= 400) -> None:
        super().__init__(p_ancho = p_ancho , p_alto = p_alto, p_ruta = p_ruta , p_formato = p_formato, p_nombre = p_nombre)
        self.__dict_palabras_frecuencias = p_dict_palabras_frecuencias 
    
    @property
    def dict_palabras_frecuencias(self):
        return self.__dict_palabras_frecuencias
    
    @dict_palabras_frecuencias.setter
    def dict_palabras_frecuencias(self, p_dict_palabras_frecuencias):
        self.__dict_palabras_frecuencias = p_dict_palabras_frecuencias
    
    def graficar_y_guardar(self):
        """Metodo que crea la gráfica de la nube de palabras, con el tamaño de las palabras proporcionales a su frecuencia
        y la guarda en un archivo de self.formato con el nombre de self.nombre en la ruta de self.ruta"""
            
        # Crear la nube de palabras
        nube_de_palabras = WordCloud(background_color="white", width=self.ancho, height=self.alto, random_state=75,
                                        contour_width=3, contour_color='steelblue', colormap='inferno', prefer_horizontal=1)

        # Generar la nube de palabras con las frecuencias correspondientes
        nube_de_palabras.generate_from_frequencies(self.dict_palabras_frecuencias)

        nube_de_palabras.to_file(self.ruta + self.nombre + "." + self.formato)

class GraficadorDeCategorias(Graficador):
    """ Clase que modela un graficador de categorias
    ------------------------------------------------
    Atributos:
    * ancho: int
    * alto: int
    * ruta: String
    * nombre: String
    * formato: String
    * dict_etiquetas_frecuencias: dict(keys: String ,values: int) // Representa las  etiquetas de las categorias y las frecuencias asociadas
    * nombre_categorias: String
    * nombre_elementos: String
    * etiquetas = list(String)
    * cantidades = list(String)
    * total = int
    """
    def __init__(self, p_dict_etiquetas_frecuencias, p_nombre_elementos,  p_nombre_categorias, p_ruta , p_nombre,  p_formato , p_ancho = 400  , p_alto= 400 ) -> None:
        super().__init__( p_ancho = p_ancho , p_alto = p_alto, p_ruta = p_ruta , p_formato = p_formato, p_nombre = p_nombre)
        
        self.__dict_etiquetas_frecuencias = p_dict_etiquetas_frecuencias
        self.__nombre_categorias = p_nombre_categorias
        self.__nombre_elementos = p_nombre_elementos

        #datos:
        self._etiquetas = []
        self._cantidades = []
        self._total = None

        self.__actualizar_datos()

    @property
    def dict_etiquetas_frecuencias(self):
        return self.__dict_etiquetas_frecuencias
    
    @dict_etiquetas_frecuencias.setter
    def dict_etiquetas_frecuencias(self, p_dict_etiquetas_frecuencias):
        self.__dict_etiquetas_frecuencias = p_dict_etiquetas_frecuencias
        self.__actualizar_datos()

    @property
    def nombre_elementos(self):
        return self.__nombre_elementos
    
    @nombre_elementos.setter
    def nombre_elementos(self, p_nombre_elementos):
        self.__nombre_elementos = p_nombre_elementos

    @property
    def nombre_categorias(self):
        return self.__nombre_categorias
    
    @nombre_categorias.setter
    def nombre_categorias(self, p_nombre_categorias):
        self.__nombre_categorias = p_nombre_categorias

    def __actualizar_datos(self):
        """Metodo que actualiza la lista de etiquetas, la lista de cantidad y la suma total 
        a partir del diccionario self.dict_etiquetas_frecuencias"""
         

        for etiqueta, cantidad in self.dict_etiquetas_frecuencias.items():
            self._etiquetas.append( etiqueta + " (" +str(cantidad) +")" )
            self._cantidades.append(cantidad)

            self._total = sum(self._cantidades)

        #Ordeno alfabeticamente
        etiquetas_ordenadas, cantidades_ordenadas = zip(*sorted(zip(self._etiquetas, self._cantidades)))
        self._etiquetas = etiquetas_ordenadas
        self._cantidades = cantidades_ordenadas




class GraficadorDeDiagramaCircular(GraficadorDeCategorias):
    """ Clase que modela un graficador de diagrma circular
    ------------------------------------------------
    Atributos:
    * ancho: int
    * alto: int
    * ruta: String
    * nombre: String
    * formato: String
    * dict_etiquetas_frecuencias: dict(keys: String ,values: int) // Representa las  etiquetas de las categorias y las frecuencias asociadas
    * nombre_categorias: String
    * nombre_elementos: String
    * etiquetas = list(String)
    * cantidades = list(String)
    * total = int
    """
    def __init__(self, p_dict_etiquetas_frecuencias,p_nombre_elementos, p_nombre_categorias, p_ruta, p_nombre, p_formato, p_ancho=400, p_alto=400) -> None:
        super().__init__(p_dict_etiquetas_frecuencias, p_nombre_elementos, p_nombre_categorias, p_ruta, p_nombre, p_formato, p_ancho, p_alto)

    def graficar_y_guardar(self):
            """Metodo que crea la gráfica de diagrama circular y la guarda en un archivo de self.formato
              con el nombre de self.nombre en la ruta de self.ruta"""
          
            #Grafíca        
            fig, ax = plt.subplots()
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            ax.set_title("ESTADISTICA: " + self.nombre_elementos)
            ax.set_xlabel("TOTAL DE "  + self.nombre_elementos.upper() + "= " + str(self._total))

            colors = list(mcolors.XKCD_COLORS.values())
            colors.insert(0, '#8c92ac')
            colors.insert(1, '#3adb76')

            wedges, texts, autotexts = ax.pie(self._cantidades, labels=self._etiquetas, autopct='%1.1f%%',
                                 colors=colors, pctdistance=0.72, wedgeprops={"linewidth": 1, "edgecolor": "white"},
                                 )

            centre_circle = Circle((0, 0), 0.5, color="white")
            ax.add_artist(centre_circle)

            #Guarda
            plt.savefig(self.ruta + self.nombre + "." + self.formato)
            
            
class GraficadorDeDiagramaCircularAnimado(GraficadorDeCategorias):
    """ Clase que modela un graficador de un diagrma circular animado
    ------------------------------------------------
    Atributos:
    * ancho: int
    * alto: int
    * ruta: String
    * nombre: String
    * formato: String
    * dict_etiquetas_frecuencias: dict(keys: String ,values: int) // Representa las  etiquetas de las categorias y las frecuencias asociadas
    * nombre_categorias: String
    * nombre_elementos: String
    * etiquetas = list(String)
    * cantidades = list(String)
    * total = int
    """
    def __init__(self, p_dict_etiquetas_frecuencias, p_nombre_elementos , p_nombre_categorias, p_ruta, p_nombre, p_formato, p_ancho=400, p_alto=400) -> None:
        
        if p_formato != "gif":
            raise ValueError("El formato para guardar la animacion debe ser de tipo gif")
        super().__init__(p_dict_etiquetas_frecuencias, p_nombre_elementos , p_nombre_categorias, p_ruta, p_nombre, p_formato, p_ancho, p_alto)


    def graficar_y_guardar(self):
            """Metodo que crea la gráfica de diagrama circular animado y la guarda en un archivo de self.formato
              con el nombre de self.nombre en la ruta de self.ruta"""

            #Grafíca 
            fig, ax = plt.subplots()

            def update(frame):
                ax.clear()
                ax.set_xlim(-1.5, 1.5)
                ax.set_ylim(-1.5, 1.5)
                ax.set_title("ESTADISTICA: " + self.nombre_elementos)
                ax.set_xlabel("TOTAL DE "  + self.nombre_elementos.upper() + "= " + str(self._total))

                colors = list(mcolors.XKCD_COLORS.values())
                colors.insert(0, '#8c92ac')
                colors.insert(1, '#3adb76')

                wedges, texts, autotexts = ax.pie(self._cantidades, labels=self._etiquetas, autopct='%1.1f%%',
                                 colors= colors, pctdistance=0.72, wedgeprops={"linewidth": 1, "edgecolor": "white"},
                                 startangle=frame)

                centre_circle = Circle((0, 0), 0.5, color="white")
                ax.add_artist(centre_circle)

            anim = FuncAnimation(fig, update, frames=range(0, 360, 20), interval=8000, repeat=True)

            #Guarda
            anim.save(self.ruta + self.nombre + "." + self.formato , writer='pillow', fps=1, dpi=80)

class GraficadorDeDiagramaDeBarras(GraficadorDeCategorias):
    """ Clase que modela un graficador de un diagrma de barras
    ------------------------------------------------
    Atributos:
    * ancho: int
    * alto: int
    * ruta: String
    * nombre: String
    * formato: String
    * dict_etiquetas_frecuencias: dict(keys: String ,values: int) // Representa las  etiquetas de las categorias y las frecuencias asociadas
    * nombre_categorias: String
    * nombre_elementos: String
    * etiquetas = list(String)
    * cantidades = list(String)
    * total = int
    """
    def __init__(self, p_dict_etiquetas_frecuencias, p_nombre_elementos, p_nombre_categorias, p_ruta, p_nombre, p_formato, p_ancho=400, p_alto=400) -> None:
        super().__init__(p_dict_etiquetas_frecuencias, p_nombre_elementos, p_nombre_categorias, p_ruta, p_nombre, p_formato, p_ancho, p_alto)
    
    def graficar_y_guardar(self):
        """Metodo que crea la gráfica de diagrama de barras y la guarda en un archivo de self.formato
           con el nombre de self.nombre en la ruta de self.ruta"""
        
        #Grafica

        fig, ax = plt.subplots()

        colors = list(mcolors.XKCD_COLORS.values())
        colors.insert(0, '#8c92ac')     
        colors.insert(1, '#ff004d')
        colors.insert(2, '#ffc30b')
        colors.insert(3, '#3adb76')
        
        # Crear el diagrama de barras
        ax.bar(self._etiquetas, self._cantidades, color=colors)

        # Personalizar el gráfico
        ax.set_title(f"Cantidad de {self.nombre_elementos} por {self.nombre_categorias} (Total: {self._total})")
        ax.set_xlabel(self.nombre_categorias)
        ax.set_ylabel("Cantidad")
        ax.set_ylim(0, max(self._cantidades) * 1.2)  
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Mostrar valores enteros en el eje y
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

        #guarda
        plt.savefig(self.ruta + self.nombre + "." + self.formato)


if __name__== "__main__":  
    pass

