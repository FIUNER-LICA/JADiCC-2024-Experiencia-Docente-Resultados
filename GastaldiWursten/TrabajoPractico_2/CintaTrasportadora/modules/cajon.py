from modules.alimento import Alimento


class Cajon():
    """ Clase que modela un Cajon
    -------------------------------------------
    Atributos:
    * alimentos: list [Alimento]
    """

    def __init__(self) -> None:
        self.__alimentos = []

    
    def añadir_alimento(self, p_alimento):
        """ Método que evalúa si el objeto recibido es del tipo Alimento
        y lo agrega a una lista en caso de que sea afirmativo
        Argumentos:
        * p_alimento: Alimento
        """
        if not isinstance (p_alimento, Alimento):
            raise TypeError ("El objeto no es de tipo Alimento")
        self.__alimentos.append(p_alimento)

    
    def cantidad_de_alimento_de_tipo(self , p_clase_de_alimento):
        """ Método que devuelve la cantidad de alimentos presentes en el cajón 
        del tipo de la clase indicada
        Argumentos:
        * p_clase_de_alimento: Alimento class
        
        Returns:
        * int        
        """     
        if not issubclass (p_clase_de_alimento, Alimento):
            raise TypeError ("La clase no es de tipo Alimento")

        return len([alimento for alimento in self if isinstance(alimento, p_clase_de_alimento)])
   
    
    def calcular_aw_prom_tipo(self, p_clase_de_alimento):
        """ Método que devuelve el aw promedio de los alimentos presentes en el cajón 
        del tipo de la clase indicada
        Argumentos:
        * p_clase_de_alimento: Alimento class
        
        Returns:
        * promedio: float        
        """
        if not issubclass (p_clase_de_alimento, Alimento):
            raise TypeError ("La clase no es de tipo Alimento")

        promedio = 0

        cantidad = self.cantidad_de_alimento_de_tipo(p_clase_de_alimento)

        if cantidad != 0:
            promedio = round(sum([alimento.obtener_aw() for alimento in self if isinstance(alimento, p_clase_de_alimento)]) / cantidad,2)
        
        return promedio

    def __iter__(self):
        """" Sobrecarga para poder iterar sobre los alimentos del cajón"""
        return ( alimento for alimento in self.__alimentos)
    
    def __len__(self):
        """" Sobrecarga para que al usar len() se pueda obtener la cantidad de alimentos en el cajón"""
        return len(self.__alimentos)
