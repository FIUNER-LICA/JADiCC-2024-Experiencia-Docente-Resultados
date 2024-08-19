from modules.alimento import Alimento
from modules.fruta import Fruta
from modules.kiwi import Kiwi
from modules.manzana import Manzana
from modules.papa import Papa
from modules.verdura import Verdura
from modules.zanahoria import Zanahoria


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


    def __iter__(self):
        """" Sobrecarga para poder iterar sobre los alimentos del cajón"""
        return ( alimento for alimento in self.__alimentos)
    
    def __len__(self):
        """" Sobrecarga para que al usar len() se pueda obtener la cantidad de alimentos en el cajón"""
        return len(self.__alimentos)
    
if __name__ == "__main__":
    
    cajon = Cajon()
       
    kiwi1 = Kiwi(0.400)
    manzana1 = Manzana(0.350)
    papa1 = Papa(0.300)
    zanahoria1 = Zanahoria(0.250)
    cajon.añadir_alimento(kiwi1)
    cajon.añadir_alimento(manzana1)
    cajon.añadir_alimento(papa1)
    cajon.añadir_alimento(zanahoria1)

    print(cajon)
    print(cajon.__iter__)
    print(next(cajon.__iter__()))