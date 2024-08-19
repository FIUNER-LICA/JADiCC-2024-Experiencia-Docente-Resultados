import unittest
from modules.detector_alimento import DetectorAlimento

class TestDetectordeAlimentos(unittest.TestCase):
        
        def setUp(self):

            self.detector = DetectorAlimento()
            
        def test_detector_alimento(self):
            """ Se comprueba que el detector de alimentos devuelva un diccionario con las etiquetas de alimento validas
        y que el peso esté dentro del rango """

            etiquetas = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]

            for _ in range(100):
                alimento_detectado = self.detector.detectar_alimento()
                self.assertTrue(alimento_detectado["alimento"] in etiquetas)
                self.assertTrue(alimento_detectado["peso"] <= 0.6)

if __name__ == '__main__':
    unittest.main()