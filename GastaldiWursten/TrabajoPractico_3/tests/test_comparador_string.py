import unittest
from modules.comparador_de_strings_en_español import ComparadorDeStrings
import random


class TestComparadorDeString(unittest.TestCase):
    def setUp(self):

        self.comparador_de_strings = ComparadorDeStrings()
    
    def test_comparar_strings_iguales(self):
        """ Se prueba la correcta comparación de dos strings iguales"""
        
        similitud = self.comparador_de_strings.comparar_strings("Prueba de comparacion de strings", 
                                                                "Prueba de comparacion de strings")
        self.assertEqual( similitud, 1 )
    
    def test_comparar_strings_muy_similares(self):
        """ Se prueba la correcta comparación de dos strings similares"""
        
        similitud = self.comparador_de_strings.comparar_strings("Prueba de comparacion de strings", 
                                                                "Test de comparacion de strings")
        
        self.assertGreaterEqual(similitud, 0.6, "El resultado no es mayor o igual a 0.6.")
    
if __name__ == '__main__':
    unittest.main()

