from modules.alimento import Alimento

class Fruta(Alimento):
    """ Clase que modela una Fruta
    -------------------------------------------
    """
    def __init__(self, p_peso) -> None:
        super().__init__(p_peso)
        