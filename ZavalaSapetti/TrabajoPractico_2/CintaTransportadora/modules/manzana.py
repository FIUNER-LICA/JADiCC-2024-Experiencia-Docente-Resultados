from modules.fruta import Fruta

class Manzana(Fruta):
    """ Clase que modela una Manzana
    -------------------------------------------
    Atributos:
    * Peso: float
    * Constante_c: int
    """

    def __init__(self, p_peso) -> None:
        super().__init__(p_peso)
        self.constante_c = 15
           
    def obtener_aw(self):     
        """ Método que calcula la actividad acuosa de una manzana
        """   
        return (0.97*(((self.constante_c*self.peso)**2)/(1+(self.constante_c*self.peso)**2)))
       