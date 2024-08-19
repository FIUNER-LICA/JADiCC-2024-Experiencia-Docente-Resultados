from abc import ABC, abstractmethod

class Alimento(ABC):

    """ Clase que modela un Alimento
    -------------------------------------------
    Atributos:
    * Peso: float
    * Constante_c: int
    """

    def __init__(self, p_peso) -> None:
        super().__init__()
        self.__peso = p_peso
        self.__constante_c = None

    
    @property
    def peso(self):
        return self.__peso
    
    @property
    def constante_c(self):
        return self.__constante_c
    
    
    @peso.setter
    def peso (self, p_peso):
        self.__peso = p_peso

    @constante_c.setter
    def constante_c (self, p_constante_c):
        self.__constante_c = p_constante_c

    @abstractmethod
    def obtener_aw(self):
        pass
    