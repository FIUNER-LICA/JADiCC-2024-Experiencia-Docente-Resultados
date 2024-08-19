import unittest
from modules.cajon import Cajon
from modules.alimento import Alimento
from modules.fruta import Fruta
from modules.verdura import Verdura
from modules.kiwi import Kiwi
from modules.manzana import Manzana
from modules.papa import Papa
from modules.zanahoria import Zanahoria

class TestCajon(unittest.TestCase):
    def setUp(self):

        self.cajon = Cajon()
       
        self.kiwi1 = Kiwi(0.400)
        self.manzana1 = Manzana(0.350)
        self.papa1 = Papa(0.300)
        self.zanahoria1 = Zanahoria(0.250)


    def test_añadir_alimento_a_cajon(self):
        """ Se comprueba que los alimentos se encuentren en el cajon cuando se los añade y 
        se compara aw_prom con los valores esperados"""

        # se añaden alimentos
        self.cajon.añadir_alimento(self.kiwi1)
        self.cajon.añadir_alimento(self.manzana1)
        self.cajon.añadir_alimento(self.papa1)
        self.cajon.añadir_alimento(self.zanahoria1)

        # se comprueba que esten en el cajón
        self.assertTrue(self.kiwi1 in self.cajon)
        self.assertTrue(self.manzana1 in self.cajon)
        self.assertTrue(self.papa1 in self.cajon)
        self.assertTrue(self.zanahoria1 in self.cajon)

       
if __name__ == '__main__':
    unittest.main()