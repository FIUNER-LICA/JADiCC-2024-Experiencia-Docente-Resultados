import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from modules.gestor_de_reclamos import GestorDeReclamos
from modules.monticulo_mediana import MonticuloMediana
from modules.models import TablaReclamos
from modules.repositorio_concreto import RepositorioSQL
import logging #registros de depuración para verificar los datos en diferentes etapas del flujo
import datetime

nltk.download('punkt')
nltk.download('stopwords')

class GeneradorDeEstadisticas():
    """ Clase que modela un generador de estadisticas de reclamos.
    ------------------------------------------------
    Atributos:
    * lista_de_reclamos: list(Reclamo)
    * estados_posibles: list(String)

    """
    def __init__(self) -> None:
        self.__repositorio = RepositorioSQL()
        self.__gestor_reclamos = GestorDeReclamos(self.__repositorio)
        self.__estados_posibles = ["En Proceso", "Pendiente", "Inválido", "Resuelto"]


    @property
    def estados_posibles(self):
        return self.__estados_posibles
    


    def calcular_estadisticas(self, p_departamento):
        lista_reclamos = self.__gestor_reclamos.obtener_reclamos_por_atributo(p_departamento)
        estadisticas = {
            'total_reclamos': len(lista_reclamos),
            'estado_pendiente': sum(1 for reclamo in lista_reclamos if reclamo.estado == 'Pendiente'),
            'estado_en_proceso': sum(1 for reclamo in lista_reclamos if reclamo.estado == 'En Proceso'),
            'estado_resuelto': sum(1 for reclamo in lista_reclamos if reclamo.estado == 'Resuelto'),
            'estado_invalido': sum(1 for reclamo in lista_reclamos if reclamo.estado == 'Inválido')
        }
        return estadisticas    

    def obtener_media_reclamos_resueltos(self):
        """tiempo de resolucion de estimado de los que estan en proceso. levantas ese dato y lo pones en la mediana
        filtrar los reclamos por estado, ya que pendiente o resuelto tenran distintos tiempos
        tiene que ver el atributo de timepo estimado de resolución"""
        reclamos_resueltos = [reclamo for reclamo in self.gestor_reclamos.devolver_reclamos() if reclamo.estado == 'Resuelto']
        tiempos_resolucion = [reclamo.tiempo_de_resolucion for reclamo in reclamos_resueltos if reclamo.tiempo_de_resolucion is not None]
        if not tiempos_resolucion:
            return None
        monticulo_mediana = MonticuloMediana(tiempos_resolucion)
        return monticulo_mediana.get_mediana()



    def obtener_palabras_mas_frecuentes(self, departamento):
        """ Método que devuelve las palabras mas frecuentes (o menos si no hay 15) del total de los 
        contenidos de los reclamos.
        
        Returns:
        * dict(keys:String, values: int)) or {}       
        """ 

        # Obtener las palabras de las listas de reclamo
        reclamos = self.__gestor_reclamos.obtener_reclamos_por_atributo("departamento_correspondiente", departamento)
        strings_contenidos = [reclamo.contenido for reclamo in reclamos]
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
    

    def porcentajes_de_estado_reclamos(self, p_departamento):
        """
        Calcula los porcentajes de reclamos por estado para un departamento dado.

        Retorna:
            Una lista de tuplas, cada una con un estado y su porcentaje correspondiente de reclamos
            en ese estado dentro del departamento.
        """
   
        estados_posibles = ['En Proceso','Resuelto', 'Pendiente', 'Inválido' ]
        reclamos_totales = self.__gestor_reclamos.obtener_reclamos_por_atributo("departamento_correspondiente", p_departamento)
        #logging.debug(f"Reclamos obtenidos para departamento {p_departamento}: {reclamos_totales}")
        total_reclamos = len(reclamos_totales)

        if total_reclamos == 0:
            return [(estado, 0) for estado in estados_posibles]
        
        conteo_estados = {estado: 0 for estado in estados_posibles}
        for reclamo in reclamos_totales:
            if reclamo.estado in conteo_estados:
                conteo_estados[reclamo.estado] += 1
        
        porcentajes = [(estado, (conteo_estados[estado] / total_reclamos) * 100) for estado in estados_posibles]
        #logging.debug(f"Porcentajes calculados: {porcentajes}")
        return porcentajes
    
    def tiempo_resolucion_por_estado(self, departamento, estado):
        """
        Calcula los tiempos de resolución de reclamos por estado para un departamento dado.

        Args:
            departamento (str): El nombre del departamento para el cual se calculan los tiempos de resolución.
            estado (str): El estado de los reclamos para los cuales se calculan los tiempos de resolución.

        Returns:
            Una lista de tiempos de resolución en días para los reclamos en el estado especificado dentro del departamento.
            Si el estado es 'Resuelto', se calcula el tiempo de resolución desde el inicio del proceso hasta la resolución.
            Si el estado es 'En Proceso', se calcula el tiempo desde el inicio del proceso hasta la fecha actual.
        """
        reclamos = self.__gestor_reclamos.obtener_reclamos_por_atributo("departamento_correspondiente", departamento)
        logging.debug(f"Reclamos obtenidos para departamento {departamento} y estado {estado}: {reclamos}")
        tiempos = []
        for reclamo in reclamos:
                    if reclamo.estado == estado:
                        if estado == 'Resuelto':
                            tiempo_resolucion = reclamo.tiempo_de_resolucion
                            logging.debug(f"Reclamo {reclamo.id} - Tiempo de resolución: {tiempo_resolucion}")
                            if tiempo_resolucion is not None:
                                tiempos.append(tiempo_resolucion)
                        elif estado == 'En Proceso':
                            fecha_inicio = reclamo.fecha_inicio_proceso
                            if fecha_inicio:
                                tiempo_en_proceso = (datetime.datetime.now() - fecha_inicio).total_seconds() / (3600*24)  # multiplico por 24 para calcularlo en dias; sino lo calculo en horas
                                logging.debug(f"Reclamo {reclamo.id} - Tiempo en proceso: {tiempo_en_proceso} días")
                                tiempos.append(tiempo_en_proceso)
        logging.debug(f"Tiempos calculados para estado {estado}: {tiempos}")
        return tiempos
    
    
#if __name__== "__main__":  
