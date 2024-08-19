import unittest
from modules.monticulo import Monticulo  # Asegúrate de ajustar el nombre del módulo según sea necesario

class TestMonticulo(unittest.TestCase):

    def test_insertar_sec_5381_min_es_1(self):
        monticulo = Monticulo('min')
        monticulo.insertar(5)
        monticulo.insertar(3)
        monticulo.insertar(8)
        monticulo.insertar(1)
        self.assertEqual(monticulo.raiz(), 1)
        #como cambia el tamaño 

    def test_eliminar_valor_min(self):
        monticulo = Monticulo('min')
        monticulo.insertar(5)
        monticulo.insertar(3)
        monticulo.insertar(8)
        monticulo.insertar(1)
        prim_val = monticulo.eliminar_valor()
        self.assertEqual(prim_val, 1)
        self.assertEqual(monticulo.raiz(), 3)


    def test_insertar_y_eliminar_valor_min(self):
        monticulo = Monticulo('min')
        valores = [10, 4, 5, 30, 3, 12]
        for valor in valores:
            monticulo.insertar(valor)
        self.assertEqual(monticulo.eliminar_valor(), 3)
        self.assertEqual(monticulo.eliminar_valor(), 4)
        self.assertEqual(monticulo.eliminar_valor(), 5)
        self.assertEqual(monticulo.raiz(), 10)

    def test_insertar_sec_5381_max_es_8(self):
            monticulo = Monticulo('max')
            monticulo.insertar(5)
            monticulo.insertar(3)
            monticulo.insertar(8)
            monticulo.insertar(1)
            self.assertEqual(monticulo.raiz(), 8)
            #como cambia el tamaño 

    def test_eliminar_valor_max(self):
        monticulo = Monticulo('max')
        monticulo.insertar(5)
        monticulo.insertar(3)
        monticulo.insertar(8)
        monticulo.insertar(1)
        prim_val = monticulo.eliminar_valor()
        self.assertEqual(prim_val, 8)
        self.assertEqual(monticulo.raiz(), 5)


    def test_insertar_y_eliminar_valor_max(self):
        monticulo = Monticulo('max')
        valores = [10, 4, 5, 30, 3, 12]
        for valor in valores:
            monticulo.insertar(valor)
        self.assertEqual(monticulo.eliminar_valor(), 30)
        self.assertEqual(monticulo.eliminar_valor(), 12)
        self.assertEqual(monticulo.eliminar_valor(), 10)
        self.assertEqual(monticulo.raiz(), 5)

if __name__ == '__main__':
    unittest.main()
