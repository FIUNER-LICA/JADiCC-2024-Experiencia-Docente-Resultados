from modules.verdura import Verdura
from math import atan
class Papa(Verdura):
    """ Clase que modela una Papa
    -------------------------------------------
    Atributos:
    * Peso: float
    * Constante_c: int
    """

    def __init__(self, p_peso) -> None:
        super().__init__(p_peso)
        self.constante_c = 18
        
    def obtener_aw(self):
        """ Método que calcula la actividad acuosa de una papa
        """
        return 0.66*atan(self.constante_c*self.peso)
         