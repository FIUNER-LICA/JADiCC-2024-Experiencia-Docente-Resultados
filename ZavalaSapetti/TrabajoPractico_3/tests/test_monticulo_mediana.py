import unittest
from modules.monticulo import Monticulo
from modules.monticulo_mediana import MonticuloMediana  # Ajusta el nombre del módulo si es necesario

class TestMonticuloMediana(unittest.TestCase):

    def setUp(self):
        lista = [1,2,3,4,5]
        self.monticulo_mediana = MonticuloMediana(lista)


    def test_insertar_y_actualizar_mediana(self):
        self.monticulo_mediana.actualizar_mediana(0)
        self.assertEqual(self.monticulo_mediana.get_mediana(), 2.5)
        self.monticulo_mediana.actualizar_mediana(1)
        self.assertEqual(self.monticulo_mediana.get_mediana(), 2)
        self.monticulo_mediana.actualizar_mediana(2)
        self.assertEqual(self.monticulo_mediana.get_mediana(), 2)
        self.monticulo_mediana.actualizar_mediana(3)
        self.assertEqual(self.monticulo_mediana.get_mediana(), 2)
        self.monticulo_mediana.actualizar_mediana(4)
        self.assertEqual(self.monticulo_mediana.get_mediana(), 2.5)

    def test_insertar_desordenado(self):
        self.monticulo_mediana.actualizar_mediana(2)
        self.monticulo_mediana.actualizar_mediana(0)
        self.monticulo_mediana.actualizar_mediana(3)
        self.monticulo_mediana.actualizar_mediana(1)
        self.assertEqual(self.monticulo_mediana.get_mediana(), 2)
        self.monticulo_mediana.actualizar_mediana(4)
        self.assertEqual(self.monticulo_mediana.get_mediana(), 2.5)


if __name__ == '__main__':
    unittest.main()
