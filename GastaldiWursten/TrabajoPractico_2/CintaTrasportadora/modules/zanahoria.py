from modules.verdura import Verdura
from math import exp

class Zanahoria(Verdura):
    """ Clase que modela una Zanahoria
    -------------------------------------------
    Atributos:
    * Peso: float
    * Constante_c: int
    """

    def __init__(self, p_peso) -> None:
        super().__init__(p_peso)
        self.constante_c = 10
        
    def obtener_aw(self):
        """ Método que calcula la actividad acuosa de una zanahoria
        """
        return 0.96*(1-exp(-self.constante_c*self.peso))
      