from modules.fruta import Fruta
from math import exp

class Kiwi(Fruta):
    """ Clase que modela un Kiwi
    -------------------------------------------
    Atributos:
    * Peso: float
    * Constante_c: int
    """
    def __init__(self, p_peso) -> None:
        super().__init__(p_peso)
        self.constante_c = 18

    def obtener_aw(self):
        """ Método que calcula la actividad acuosa de un kiwi
        """
        return 0.96*((1-exp(-self.constante_c*self.peso))/(1+exp(-self.constante_c*self.peso)))
        