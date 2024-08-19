import matplotlib
matplotlib.use('Agg')
from PIL import Image
from modules.graficadores import Graficador
import os
from PIL import Image, ImageDraw, ImageFont
from modules.graficadores import GraficadorDeDiagramaCircular , GraficadorDeDiagramaDeBarras , GraficadorDeDiagramaCircularAnimado , GraficadorDeNubeDePalabras

class GraficadorDeDatosDeReclamo(Graficador):
    """ Clase que modela un graficador de datos de reclamos
    ------------------------------------------------
    Atributos:
    * ancho: int
    * alto: int
    * ruta: String
    * nombre: String
    * formato: String
    * generador_de_analiticos_de_reclamos: GeneradorDeAnaliticosDeReclamos

    """
    def __init__(self, p_generador_de_analiticos_de_reclamos) -> None:
        self.__generador_de_analiticos_de_reclamos = p_generador_de_analiticos_de_reclamos
        
    @property
    def generador_de_analiticos_de_reclamos(self):
        return self.__generador_de_analiticos_de_reclamos
    
    @generador_de_analiticos_de_reclamos.setter
    def generador_de_analiticos_de_reclamos(self, p_generador_de_analiticos_de_reclamos):
        self.__generador_de_analiticos_de_reclamos = p_generador_de_analiticos_de_reclamos
    
    
    
class GraficadorDeNubeDePalabrasDeReclamos(GraficadorDeDatosDeReclamo, GraficadorDeNubeDePalabras):
    """ Clase que modela un graficador de nubes de palabras
    ------------------------------------------------
    Atributos:
    * ancho: int
    * alto: int
    * ruta: String
    * nombre: String
    * formato: String
    * dict_palabras_frecuencias: dict(keys: String ,values: int) // Representa las palabras y las frecuencias asociadas
    * generador_de_analiticos_de_reclamos: GeneradorDeAnaliticosDeReclamos
    """
    def __init__(self,p_generador_de_analiticos_de_reclamos, p_ruta) -> None:
        GraficadorDeDatosDeReclamo.__init__(self, p_generador_de_analiticos_de_reclamos)       
        p_dict_palabras_frecuencias = p_generador_de_analiticos_de_reclamos.obtener_palabras_mas_frecuentes()
        GraficadorDeNubeDePalabras.__init__(self, p_dict_palabras_frecuencias , p_ruta , "nube", "png", p_ancho=1200, p_alto=400)

    def graficar_y_guardar(self):
        """Metodo que crea la gráfica de nube de palabras con las palabras mas frecuentes de los reclamos y
          la guarda en un archivo de self.formato con el nombre de self.nombre en la ruta de self.ruta, 
          en caso de que no haya palabras para graficar crea una imagen avisando sobre la situacion"""

        if len(self.dict_palabras_frecuencias) == 0:
            img = Image.new('RGB', (self.ancho, self.alto), color='white')
            d = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", 40)
            d.text((160, 160), "Su departamento aún no ha recibido reclamos", fill=(225, 184, 82), font=font)
            img.save(self.ruta + self.nombre + "." + self.formato)
        else:            
            super().graficar_y_guardar()

class GraficadorDeDiagramaCircularDeReclamos(GraficadorDeDatosDeReclamo , GraficadorDeDiagramaCircular):
    """ Clase que modela un graficador de diagrma circular de datos de reclamos
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
    * generador_de_analiticos_de_reclamos: GeneradorDeAnaliticosDeReclamos
    """
    def __init__(self, p_generador_de_analiticos_de_reclamos, p_ruta) -> None:
        GraficadorDeDatosDeReclamo.__init__(self, p_generador_de_analiticos_de_reclamos)
        
        dict_estado_cantidad = {estado: cantidad for estado, cantidad in self.generador_de_analiticos_de_reclamos.obtener_cantidad_de_reclamos_por_estado().items() 
                                  if estado in ["En Proceso", "Resuelto"]}
        
        GraficadorDeDiagramaCircular.__init__(self, dict_estado_cantidad, "Reclamos", "Estado", p_ruta, "grafica_circular", "png", p_ancho = 400, p_alto = 400)
    
    def graficar_y_guardar(self):
        """Metodo que crea la gráfica de diagrama circular con los las cantidades de reclamos en estado "En Proceso" y "Resuelto"
        y la guarda en un archivo de self.formato con el nombre de self.nombre en la ruta de self.ruta, 
        en caso de que no haya cantidades para graficar crea una imagen avisando sobre la situacion"""
        
        if sum(self.dict_etiquetas_frecuencias.values()) == 0:
 
            image = Image.new("RGB", (self.ancho, self.alto), "white")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("arial.ttf", 30)  
            draw.text((200, 100), "Sin Reclamos Resueltos", fill='green', anchor="mm", font=font)
            draw.text((200, 250), "Sin Reclamos En Proceso", fill='gray', anchor="mm", font=font)
            image.save(self.ruta + self.nombre + "." + self.formato)
        else:
            super().graficar_y_guardar()

class GraficadorDeDiagramaCircularAnimadoDeReclamos(GraficadorDeDatosDeReclamo, GraficadorDeDiagramaCircularAnimado):
    """ Clase que modela un graficador de diagrma circular animado de datos de reclamos
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
    * generador_de_analiticos_de_reclamos: GeneradorDeAnaliticosDeReclamos
    """
    def __init__(self, p_generador_de_analiticos_de_reclamos, p_ruta) -> None:
        GraficadorDeDatosDeReclamo.__init__(self, p_generador_de_analiticos_de_reclamos)
        dict_estado_cantidad = {estado: cantidad for estado, cantidad in self.generador_de_analiticos_de_reclamos.obtener_cantidad_de_reclamos_por_estado().items() 
                                  if estado in ["En Proceso", "Resuelto"]}
        
        GraficadorDeDiagramaCircularAnimado.__init__(self, dict_estado_cantidad, "Reclamos En Proceso y Resuelto", "Estado", p_ruta, "circular_animado", "gif", p_ancho = 400, p_alto = 400)
    
    
    def graficar_y_guardar(self):
        """ Metodo que crea la gráfica de diagrama circular animado con los las cantidades de reclamos en estado 
        "En Proceso" y "Resuelto" y la guarda en un archivo de self.formato con el nombre de self.nombre en la ruta
        de self.ruta, en caso de que no haya cantidades para graficar crea una imagen avisando sobre la situacion"""
        
        if sum(self.dict_etiquetas_frecuencias.values()) == 0:
 
            image = Image.new("RGB", (self.ancho, self.alto), "white")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("arial.ttf", 30)  
            draw.text((200, 100), "Sin Reclamos Resueltos", fill='green', anchor="mm", font=font)
            draw.text((200, 250), "Sin Reclamos En Proceso", fill='gray', anchor="mm", font=font)
            image.save(self.ruta + self.nombre + "." + self.formato)
        else:
            super().graficar_y_guardar()

class GraficadorDeDiagramaDeBarrasDeReclamos(GraficadorDeDatosDeReclamo, GraficadorDeDiagramaDeBarras):
    """ Clase que modela un graficador de diagrma de barras de datos de reclamos
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
    * generador_de_analiticos_de_reclamos: GeneradorDeAnaliticosDeReclamos
    """
    def __init__(self, p_generador_de_analiticos_de_reclamos, p_ruta) -> None:
        GraficadorDeDatosDeReclamo.__init__(self, p_generador_de_analiticos_de_reclamos)
        GraficadorDeDiagramaDeBarras.__init__(self, self.generador_de_analiticos_de_reclamos.obtener_cantidad_de_reclamos_por_estado(), "Reclamos", "Estado", p_ruta, "diagrama_de_barras", "png", p_ancho = 400, p_alto = 400)
 
    def graficar_y_guardar(self):
        """ Metodo que crea la gráfica de diagrama de barras con los las cantidades de reclamos segun su estado 
        y la guarda en un archivo de self.formato con el nombre de self.nombre en la ruta de self.ruta, en caso 
        de que no haya cantidades para graficar crea una imagen avisando sobre la situacion"""     
        super().graficar_y_guardar()
