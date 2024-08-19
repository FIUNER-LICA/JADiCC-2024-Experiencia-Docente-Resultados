import unittest
from modules.alimento import Alimento
from modules.fruta import Fruta
from modules.verdura import Verdura
from modules.kiwi import Kiwi
from modules.manzana import Manzana
from modules.papa import Papa
from modules.zanahoria import Zanahoria

from random import uniform

class TestTipodeAlimento(unittest.TestCase):
        
    def setUp(self):

        self.kiwi1 = Kiwi(0.400)
        self.manzana1 = Manzana(0.350)
        self.papa1 = Papa(0.300)
        self.zanahoria1 = Zanahoria(0.250)

    def test_calculo_aw_de_los_alimentos(self):
        " Prueba que el valor obtenido de aw para cada alimento sea correcto y el valor sea entre 0 y 1"
    
        #  se compara el valor calculado por el objeto con el resultado  
        #  obtenido del calculo utilizando calculadora para
        #  la formula dada y con el peso otorgado en la inicializacion

        self.assertAlmostEqual( self.kiwi1.obtener_aw(), 0.96 , places = 2)
        self.assertAlmostEqual( self.manzana1.obtener_aw(), 0.94, places=2)
        self.assertAlmostEqual( self.papa1.obtener_aw(), 0.92, places=2)
        self.assertAlmostEqual( self.zanahoria1.obtener_aw(), 0.88, places=2)

        #Se prueba que los valores calculados estén entre 0 y 1 para pesos entre 0 y 0.6 
        for _ in range(10000):
             self.kiwi = Kiwi(uniform(0, 0.6))
             self.manzana = Manzana(uniform(0, 0.6))
             self.papa = Papa(uniform(0, 0.6))
             self.zanahoria = Zanahoria(uniform(0, 0.6))

             self.assertTrue( 0 < self.kiwi.obtener_aw() < 1)
             self.assertTrue(  0 < self.manzana.obtener_aw() < 1)
             self.assertTrue( 0 < self.papa.obtener_aw() < 1 )
             self.assertTrue( 0 < self.zanahoria.obtener_aw() < 1 )


    def test_tipo_de_alimento(self):
        " Se comprueba la herencia entre tipos de alimento"

        self.assertTrue(issubclass(Kiwi,Alimento))
        self.assertTrue(issubclass(Manzana,Alimento))
        self.assertTrue(issubclass(Papa,Alimento))
        self.assertTrue(issubclass(Zanahoria,Alimento))
        self.assertTrue(issubclass(Fruta,Alimento))
        self.assertTrue(issubclass(Verdura,Alimento))

        self.assertTrue(issubclass(Kiwi,Fruta))
        self.assertTrue(issubclass(Manzana,Fruta))

        self.assertTrue(issubclass(Papa,Verdura))
        self.assertTrue(issubclass(Zanahoria,Verdura))

if __name__ == '__main__':
    unittest.main()