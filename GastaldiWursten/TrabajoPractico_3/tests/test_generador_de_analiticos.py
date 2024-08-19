import unittest
from modules.gestor_de_reclamos import GestorDeReclamos
from modules.generador_de_analiticos import GeneradorDeAnaliticosDeReclamos
import random

from modules.clasificador import Clasificador
import pickle


class TestGeneradorDeAnaliticos(unittest.TestCase):
    
    def setUp(self):

        gestor_reclamos = GestorDeReclamos(None)

        self.lista_asuntos = ["Agua", "Acceso", "Programación Avanzada"]
        self.lista_de_contenidos = ["Quisiera que mejore la calidad", "Me sirve mucho", "Me preocupan mas las pirañas"]
        
        reclamo_1 = gestor_reclamos.crear_reclamo(1, random.choice(self.lista_asuntos) , "img.png", random.choice(self.lista_de_contenidos))
        reclamo_1.estado = "En Proceso"
        reclamo_2 = gestor_reclamos.crear_reclamo(2, random.choice(self.lista_asuntos) , "img.png", random.choice(self.lista_de_contenidos))
        reclamo_3 = gestor_reclamos.crear_reclamo(3, random.choice(self.lista_asuntos) , "img.png", random.choice(self.lista_de_contenidos))
        reclamo_3.estado = "Resuelto"

        self.lista_de_reclamos = [reclamo_1 , reclamo_2 , reclamo_3]

        self.generador_de_analiticos_de_reclamos = GeneradorDeAnaliticosDeReclamos(self.lista_de_reclamos)


    def test_diccionario_palabras_mas_frecuentes(self):
        """Se comprueba que se obtiene un diccionario no vacio con claves que son string y valores que son enteros"""

        diccionario_palabras_mas_frecuentes = self.generador_de_analiticos_de_reclamos.obtener_palabras_mas_frecuentes()

        self.assertTrue(diccionario_palabras_mas_frecuentes, "El diccionario está vacío.")

        for key in diccionario_palabras_mas_frecuentes.keys():
            self.assertTrue(isinstance(key, str), f"La clave {key} no es de tipo string.")

        for value in diccionario_palabras_mas_frecuentes.values():
            self.assertTrue(isinstance(value, int), f"El valor {value} no es de tipo entero.")


    def test_cantidad_reclamos_por_estado(self):
        """ Se prueba la correcta obtencion de la cantidad de reclamos por estado """
        
        estado_cantidad = self.generador_de_analiticos_de_reclamos.obtener_cantidad_de_reclamos_por_estado()

        self.assertEqual( estado_cantidad["En Proceso"], 1)
        self.assertEqual( estado_cantidad["Inválido"], 0)
        self.assertEqual( estado_cantidad["Resuelto"], 1)
        self.assertEqual( estado_cantidad["Pendiente"], 1)

        
    
    def test_porcentaje_reclamos_por_estado(self):
        """ Se prueba la correcta obtencion del porcentaje de reclamos por estado """
        
        estado_porcentaje = self.generador_de_analiticos_de_reclamos.obtener_porcentaje_de_reclamos_por_estado()

        self.assertAlmostEqual( estado_porcentaje["En Proceso"], 33.33, places=2)
        self.assertAlmostEqual( estado_porcentaje["Inválido"], 0.00, places=2)
        self.assertAlmostEqual( estado_porcentaje["Resuelto"], 33.33, places=2)
        self.assertAlmostEqual( estado_porcentaje["Pendiente"], 33.33, places=2)

        

if __name__ == '__main__':
    unittest.main()