import unittest
from modules.calculadora import Calculadora
from modules.cajon import Cajon
from modules.alimento import Alimento
from modules.fruta import Fruta
from modules.verdura import Verdura
from modules.kiwi import Kiwi
from modules.manzana import Manzana
from modules.papa import Papa
from modules.zanahoria import Zanahoria

class TestCalculadora(unittest.TestCase):
    def setUp(self):
        
        self.cajon = Cajon()
        self.calculadora = Calculadora(self.cajon)

       
        self.cajon.añadir_alimento(Kiwi(0.400))
        self.cajon.añadir_alimento(Manzana(0.350))
        self.cajon.añadir_alimento(Papa(0.300))
        self.cajon.añadir_alimento(Zanahoria(0.250))

    def test_calcular_peso_total(self):
        # Verificamos que el peso total calculado sea correcto
        self.assertAlmostEqual(self.calculadora.calcular_peso_total(), 1.30)

    def test_calcular_aw_prom_tipo(self):
        # se calcula promedios
        aw_prom_kiwi = 0.958
        aw_prom_manzana = 0.936
        aw_prom_papa = 0.916
        aw_prom_zanahoria = 0.881
        aw_prom_frutas = (aw_prom_manzana + aw_prom_kiwi) / 2
        aw_prom_verduras = (aw_prom_papa + aw_prom_zanahoria) / 2
        aw_prom_alimentos = (aw_prom_frutas + aw_prom_verduras) / 2

        # se compara el promedio con el calculado por el cajón
        self.assertAlmostEqual( self.calculadora.calcular_aw_prom_tipo(Kiwi), aw_prom_kiwi , places = 2)
        self.assertAlmostEqual( self.calculadora.calcular_aw_prom_tipo(Manzana), aw_prom_manzana, places=2)
        self.assertAlmostEqual( self.calculadora.calcular_aw_prom_tipo(Papa), aw_prom_papa, places=2)
        self.assertAlmostEqual( self.calculadora.calcular_aw_prom_tipo(Zanahoria), aw_prom_zanahoria, places=2)
        self.assertAlmostEqual( self.calculadora.calcular_aw_prom_tipo(Fruta), aw_prom_frutas, places=2)
        self.assertAlmostEqual( self.calculadora.calcular_aw_prom_tipo(Verdura), aw_prom_verduras, places=2)
        self.assertAlmostEqual( self.calculadora.calcular_aw_prom_tipo(Alimento), aw_prom_alimentos, places=2) 

    def test_cantidad_de_alimento_de_tipo(self):
        """ Se comprueba que la cantidad de alimentos por tipo informada por el cajon coincida 
        con la cantidad de alimentos añadidos """

        # self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Kiwi), 1)
        # self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Manzana), 1)
        # self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Papa), 1)
        # self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Zanahoria, 1))
        
        cant_kiwi = 14
        cant_manzana= 15 
        cant_papa = 16
        cant_zanahoria = 17
        cant_fruta = cant_kiwi + cant_manzana
        cant_verdura = cant_papa + cant_zanahoria
        cant_alimento = cant_fruta + cant_verdura

        # se añaden alimentos
        for _ in range(cant_kiwi):
            self.cajon.añadir_alimento(Kiwi(0.100))

        for _ in range(cant_manzana):
            self.cajon.añadir_alimento(Manzana(0.100))
        
        for _ in range(cant_papa):
            self.cajon.añadir_alimento(Papa(0.100))
        
        for _ in range(cant_zanahoria):
            self.cajon.añadir_alimento(Zanahoria(0.100))

        # se compara la cantidad con la informada por el cajon

        self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Kiwi), cant_kiwi+1)
        self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Manzana), cant_manzana+1 )
        self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Papa), cant_papa+1)
        self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Zanahoria), cant_zanahoria+1)
        self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Fruta), cant_fruta+2)
        self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Verdura), cant_verdura+2)
        self.assertEqual(self.calculadora.cantidad_de_alimento_de_tipo(Alimento), 66)

    

if __name__ == '__main__':
    unittest.main()
                         
                        