from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

class GeneradorDeAnaliticosDeReclamos():
    """ Clase que modela un generador de analiticos de raclamos.
    ------------------------------------------------
    Atributos:
    * lista_de_reclamos: list(Reclamo)
    * estados_posibles: list(String)

    """
    def __init__(self, p_lista_de_reclamos, p_estados_posibles = ["En Proceso", "Pendiente", "Inválido", "Resuelto"]) -> None:

        self.__lista_de_reclamos = p_lista_de_reclamos
        self.__estados_posibles = p_estados_posibles

    @property
    def lista_de_reclamos(self):
        return self.__lista_de_reclamos
    
    @lista_de_reclamos.setter
    def lista_de_reclamos(self, p_lista_de_reclamos):
        self.__lista_de_reclamos = p_lista_de_reclamos
    
    @property
    def estados_posibles(self):
        return self.__estados_posibles
    
    @estados_posibles.setter
    def estados_posibles(self, p_estados_posibles):
        self.__estados_posibles = p_estados_posibles

    def obtener_palabras_mas_frecuentes(self):
        """ Método que devuelve las 15 palabras mas frecuentes (o menos si no hay 15) del total de los 
        contenidos de los reclamos.
        
        Returns:
        * dict(keys:String, values: int)) or {}       
        """ 

        # Obtener las palabras de las listas de reclamo
        strings_contenidos = [reclamo.contenido for reclamo in self.lista_de_reclamos]
        string_total = ' '.join(strings_contenidos)

        # Stopwords
        spanish_stopwords = set(stopwords.words('spanish') + ["."])

        # Convertir a minúsculas y separar las palabras
        words = word_tokenize(string_total.lower())

        # Eliminar los stopwords
        filtered_words = [word for word in words if word not in spanish_stopwords]


        frecuencias = Counter(filtered_words)
        palabras_mas_frecuentes = frecuencias.most_common(15)
        diccionario_15_plabras_mas_frecuentes_frecuencia = {palabra: frecuencia for palabra, frecuencia in palabras_mas_frecuentes}

        return diccionario_15_plabras_mas_frecuentes_frecuencia
    
    def obtener_cantidad_de_reclamos_por_estado(self):
        """ Método que devuelve la cantidad de reclamos por estados posibles
        
        Returns:
        * dict(keys:String, values: int))       
        """ 

        estados_reclamos = [reclamo.estado for reclamo in self.lista_de_reclamos]
        cantidad_de_reclamos_por_estado = dict(Counter(estados_reclamos))

        for estado in self.estados_posibles:
            if estado not in cantidad_de_reclamos_por_estado:
                cantidad_de_reclamos_por_estado[estado] = 0

        return cantidad_de_reclamos_por_estado
    
    def obtener_porcentaje_de_reclamos_por_estado(self):
        """ Método que devuelve el porcetaje de reclamos por estados posibles
        
        Returns:
        * dict(keys:String, values: int))       
        """ 

        cantidad_de_reclamos_por_estado = self.obtener_cantidad_de_reclamos_por_estado()
        total_reclamos = sum(cantidad_de_reclamos_por_estado.values())
        porcentaje_de_reclamos_por_estado = {}

        if total_reclamos != 0:
            for estado, cantidad in cantidad_de_reclamos_por_estado.items():
                porcentaje_de_reclamos_por_estado[estado] = round((cantidad / total_reclamos) * 100 , 2)
        else:
            porcentaje_de_reclamos_por_estado = {estado: 0 for estado in self.estados_posibles}

        return porcentaje_de_reclamos_por_estado



if __name__== "__main__":  
    
    estados_reclamos = []
    cantidad_de_reclamos_por_estado = dict(Counter(estados_reclamos))

    print(len(cantidad_de_reclamos_por_estado))