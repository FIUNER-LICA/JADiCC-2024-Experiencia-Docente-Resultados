import unittest
from modules.gestor_de_reclamos import GestorDeReclamos
from modules.graficadores import  GraficadorDeDiagramaCircular , GraficadorDeDiagramaDeBarras , GraficadorDeDiagramaCircularAnimado , GraficadorDeNubeDePalabras
from modules.graficadores_de_datos_de_reclamo import GraficadorDeDatosDeReclamo, GraficadorDeDiagramaCircularDeReclamos , GraficadorDeDiagramaCircularAnimadoDeReclamos , GraficadorDeNubeDePalabrasDeReclamos , GraficadorDeDiagramaDeBarrasDeReclamos
from modules.generador_de_analiticos import GeneradorDeAnaliticosDeReclamos
import mimetypes
import random
import os
from modules.clasificador import Clasificador
import pickle


class TestClasesDeGraficadorDeDatosDeReclamo(unittest.TestCase):
    
    def setUp(self):

        gestor_reclamos = GestorDeReclamos(None)

        self.lista_asuntos = ["Agua", "Acceso", "Programación Avanzada"]
        self.lista_de_contenidos = ["Quisiera que mejore la calidad", "Me sirve mucho", "Me preocupan mas las pirañas"]
        
        reclamo_1 = gestor_reclamos.crear_reclamo(1, random.choice(self.lista_asuntos) , "img.png", random.choice(self.lista_de_contenidos))
        reclamo_2 = gestor_reclamos.crear_reclamo(2, random.choice(self.lista_asuntos) , "img.png", random.choice(self.lista_de_contenidos))
        reclamo_3 = gestor_reclamos.crear_reclamo(3, random.choice(self.lista_asuntos) , "img.png", random.choice(self.lista_de_contenidos))

        self.lista_de_reclamos = [reclamo_1 , reclamo_2 , reclamo_3]

        self.generador_de_analiticos_de_reclamos = GeneradorDeAnaliticosDeReclamos(self.lista_de_reclamos)

        self.nube_de_palabras = GraficadorDeNubeDePalabrasDeReclamos(self.generador_de_analiticos_de_reclamos,"tests/test_graficas/")
        self.nube_de_palabras.nombre = "reclamo_nube_test"

        self.diagrama_circular = GraficadorDeDiagramaCircularDeReclamos(self.generador_de_analiticos_de_reclamos, "tests/test_graficas/" )
        self.diagrama_circular.nombre = "reclamo_circular_test"

        self.diagrama_circular_animado = GraficadorDeDiagramaCircularAnimadoDeReclamos(self.generador_de_analiticos_de_reclamos, "tests/test_graficas/" )
        self.diagrama_circular_animado.nombre = "reclamo_circular_animado_test"

        self.diagrama_de_barras = GraficadorDeDiagramaDeBarrasDeReclamos(self.generador_de_analiticos_de_reclamos,"tests/test_graficas/")
        self.diagrama_de_barras.nombre = "reclamo_diagrama_de_barras_test"



    def test_tipo_graficador_de_reclamos(self):
        """Se comprueba la herencia de las clases con graficador de datos de reclamo y tambien de su correspondiente
        graficador general"""
        self.assertTrue(issubclass(GraficadorDeNubeDePalabrasDeReclamos, GraficadorDeDatosDeReclamo))
        self.assertTrue(issubclass(GraficadorDeNubeDePalabrasDeReclamos, GraficadorDeNubeDePalabras))

        self.assertTrue(issubclass(GraficadorDeDiagramaCircularDeReclamos, GraficadorDeDatosDeReclamo))
        self.assertTrue(issubclass(GraficadorDeDiagramaCircularDeReclamos, GraficadorDeDiagramaCircular))

        self.assertTrue(issubclass(GraficadorDeDiagramaCircularAnimadoDeReclamos, GraficadorDeDatosDeReclamo))
        self.assertTrue(issubclass(GraficadorDeDiagramaCircularAnimadoDeReclamos, GraficadorDeDiagramaCircularAnimado))

        self.assertTrue(issubclass(GraficadorDeDiagramaDeBarrasDeReclamos, GraficadorDeDatosDeReclamo))
        self.assertTrue(issubclass(GraficadorDeDiagramaDeBarrasDeReclamos, GraficadorDeDiagramaDeBarras))

    def test_graficador_de_nube_de_palabras(self):
        """ Se prueba la creación de la imagen con la nube de palabras de datos de reclamos y que el formato se corresponda con 
            el tipo de archivo solicitado """
        self.nube_de_palabras.graficar_y_guardar()

        ruta_imagen = "tests/test_graficas/reclamo_nube_test.png"
        self.assertTrue(os.path.exists(ruta_imagen), "El archivo no existe en la ruta especificada.")

        tipo_mimetype, _ = mimetypes.guess_type(ruta_imagen)
        self.assertIsNotNone(tipo_mimetype) 
        self.assertEqual(tipo_mimetype, 'image/png') 

    
    def test_graficador_de_diagrama_circular(self):
        """ Se prueba la creación de la imagen con el diagrama circular  de datos de reclamos y que el formato se corresponda con 
            el tipo de archivo solicitado """
        self.diagrama_circular.graficar_y_guardar()

        ruta_imagen = "tests/test_graficas/reclamo_circular_test.png"
        self.assertTrue(os.path.exists(ruta_imagen), "El archivo no existe en la ruta especificada.")

        tipo_mimetype, _ = mimetypes.guess_type(ruta_imagen)
        self.assertIsNotNone(tipo_mimetype) 
        self.assertEqual(tipo_mimetype, 'image/png') 

    def test_graficador_de_diagrama_circular_animado(self):
        """ Se prueba la creación de la imagen con el diagrama circular animado  de datos de reclamos y que el formato se corresponda con 
            el tipo de archivo solicitado """
        self.diagrama_circular_animado.graficar_y_guardar()

        ruta_imagen = "tests/test_graficas/reclamo_circular_animado_test.gif"
        self.assertTrue(os.path.exists(ruta_imagen), "El archivo no existe en la ruta especificada.")

        tipo_mimetype, _ = mimetypes.guess_type(ruta_imagen)
        self.assertIsNotNone(tipo_mimetype) 
        self.assertEqual(tipo_mimetype, 'image/gif')

    def test_graficador_de_diagrama_de_barras(self):
        """ Se prueba la creación de la imagen con el diagrama de barras  de datos de reclamos y que el formato se corresponda con 
            el tipo de archivo solicitado """
        self.diagrama_de_barras.graficar_y_guardar()

        ruta_imagen = "tests/test_graficas/reclamo_diagrama_de_barras_test.png"
        self.assertTrue(os.path.exists(ruta_imagen), "El archivo no existe en la ruta especificada.")

        tipo_mimetype, _ = mimetypes.guess_type(ruta_imagen)
        self.assertIsNotNone(tipo_mimetype) 
        self.assertEqual(tipo_mimetype, 'image/png') 

if __name__ == '__main__':
    unittest.main()