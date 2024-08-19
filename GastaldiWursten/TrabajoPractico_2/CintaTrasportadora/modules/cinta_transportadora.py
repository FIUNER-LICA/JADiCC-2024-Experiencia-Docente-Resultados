from modules.detector_alimento import DetectorAlimento
from modules.kiwi import Kiwi
from modules.manzana import Manzana
from modules.papa import Papa
from modules.zanahoria import Zanahoria
from modules.cajon import Cajon

class CintaTransportadora():

    """ Clase que modela una Cinta Transportadora
    -------------------------------------------
    Atributos:
    * Detector: DetectorAlimento
    """

    def __init__(self) -> None:
        self.__detector = DetectorAlimento()

    def cargar_alimentos( self, p_cajon , p_numero_alimentos):
        """Método que carga en un objeto cajon la cantidad objetos de tipo alimento indicada
        Argumentos:
        * p_cajon: Cajon
        * p_numero_alimentos: int
        """
        #Comprobacion del tipo de p_cajon
        if not isinstance (p_cajon, Cajon):
            raise TypeError ("El objeto no es de tipo Cajon")

        #Comprobacion de que p_numero_alimentos no sea un valor igualado a 0 o negativo
        if p_numero_alimentos<1:
            raise ValueError ("El numero de alimentos debe ser igual o mayor a 1")
        
        alimentos_detectados_correctamente = 0

        while alimentos_detectados_correctamente < p_numero_alimentos:

            alimento_detectado = self.__detector.detectar_alimento()

            if alimento_detectado["alimento"] == "kiwi":
                alimento = Kiwi(alimento_detectado["peso"])
                p_cajon.añadir_alimento(alimento)
                alimentos_detectados_correctamente +=1
            
            if alimento_detectado["alimento"] == "manzana":
                alimento = Manzana(alimento_detectado["peso"])
                p_cajon.añadir_alimento(alimento)
                alimentos_detectados_correctamente +=1

            if alimento_detectado["alimento"] == "papa":
                alimento = Papa(alimento_detectado["peso"])
                p_cajon.añadir_alimento(alimento)
                alimentos_detectados_correctamente +=1

            if alimento_detectado["alimento"] == "zanahoria":
                alimento = Zanahoria(alimento_detectado["peso"])
                p_cajon.añadir_alimento(alimento)
                alimentos_detectados_correctamente +=1

            

            
