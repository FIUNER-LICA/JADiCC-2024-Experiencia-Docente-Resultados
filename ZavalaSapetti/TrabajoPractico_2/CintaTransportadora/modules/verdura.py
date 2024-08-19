from modules.alimento import Alimento

class Verdura(Alimento):
    """ Clase que modela una Verdura
    -------------------------------------------
    """

    def __init__(self, p_peso) -> None:
        super().__init__(p_peso)