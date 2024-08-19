import unittest
from modules.comparador_de_strings_en_español import ComparadorDeStrings  # Ajusta el nombre del módulo según sea necesario

class TestComparadorDeStrings(unittest.TestCase):

    def setUp(self):
        self.comparador = ComparadorDeStrings()

    def test_comparar_strings_iguales(self):
        string1 = "El gato está en la casa"
        string2 = "El gato está en la casa"
        resultado = self.comparador.comparar_strings(string1, string2)
        self.assertAlmostEqual(resultado, 1.0, places=2)

    def test_comparar_strings_diferentes(self):
        string1 = "El gato está en la casa"
        string2 = "El perro está en el jardín"
        resultado = self.comparador.comparar_strings(string1, string2)
        self.assertAlmostEqual(resultado, 0.0, places=2)  

    def test_comparar_strings_parcialmente_similares(self):
        string1 = "El gato está en la casa"
        string2 = "El gato duerme en la casa"
        resultado = self.comparador.comparar_strings(string1, string2)
        self.assertAlmostEqual(resultado, 0.67, places=2)  

    def test_comparar_strings_con_stopwords(self):
        string1 = "Este ni que y es un ejemplo de una oración con muchas palabras comunes"
        string2 = "Un ejemplo que lo que común de oración con muchas palabras"
        resultado = self.comparador.comparar_strings(string1, string2)
        self.assertAlmostEqual(resultado, 1.0, places=2)  

if __name__ == '__main__':
    unittest.main()
