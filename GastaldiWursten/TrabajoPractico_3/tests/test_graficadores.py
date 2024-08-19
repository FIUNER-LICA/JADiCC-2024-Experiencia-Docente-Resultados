import unittest
from modules.graficadores import Graficador , GraficadorDeCategorias , GraficadorDeDiagramaCircular , GraficadorDeDiagramaDeBarras , GraficadorDeDiagramaCircularAnimado , GraficadorDeNubeDePalabras
from abc import ABC
import mimetypes
import os


class TestClasesDeGraficador(unittest.TestCase):
    
    def setUp(self):

        diccionario_palabras_frecuencia = {"palabras":23 , "espacio":15 , "baño": 10, "roto":5 , "anda":3}
        self.nube_de_palabras = GraficadorDeNubeDePalabras(diccionario_palabras_frecuencia,"tests/test_graficas/", "nube_test", "png" )

        self.diccionario_estado_frecuencia = {"En proceso":10 , "Resuelto": 5, "Pendiente": 3 , "Invalido":23}

        self.diagrama_circular = GraficadorDeDiagramaCircular(self.diccionario_estado_frecuencia, "Reclamos" , "Estados", "tests/test_graficas/",  "circular_test", "png" )
        self.diagrama_circular_animado = GraficadorDeDiagramaCircularAnimado(self.diccionario_estado_frecuencia, "Reclamos" , "Estados",  "tests/test_graficas/",  "circular_animado_test", "gif" )
        self.diagrama_de_barras = GraficadorDeDiagramaDeBarras(self.diccionario_estado_frecuencia, "Reclamos" , "Estados",  "tests/test_graficas/",  "diagrama_de_barras_test", "png" )


    def test_tipo_graficador(self):
        """Se comprueba la herencia de la clase graficador"""
        self.assertTrue(issubclass(Graficador, ABC))
        self.assertTrue(issubclass(GraficadorDeCategorias, Graficador))
        self.assertTrue(issubclass(GraficadorDeDiagramaCircular, Graficador))
        self.assertTrue(issubclass(GraficadorDeDiagramaDeBarras, Graficador))
        self.assertTrue(issubclass(GraficadorDeDiagramaCircularAnimado, Graficador))
        self.assertTrue(issubclass(GraficadorDeNubeDePalabras, Graficador))

    def test_tipo_graficador_de_categorias(self):
        """ Se comprueba la herencia de la clase graficador de categorias """

        self.assertTrue(issubclass(GraficadorDeDiagramaCircular, GraficadorDeCategorias))
        self.assertTrue(issubclass(GraficadorDeDiagramaDeBarras, GraficadorDeCategorias))
        self.assertTrue(issubclass(GraficadorDeDiagramaCircularAnimado, GraficadorDeCategorias))
    
    def test_graficador_de_nube_de_palabras(self):
        """ Se prueba la creación de la imagen con la nube de palabras y que el formato se corresponda con 
            el tipo de archivo solicitado """
        self.nube_de_palabras.graficar_y_guardar()

        ruta_imagen = "tests/test_graficas/nube_test.png"
        self.assertTrue(os.path.exists(ruta_imagen), "El archivo no existe en la ruta especificada.")

        tipo_mimetype, _ = mimetypes.guess_type(ruta_imagen)
        self.assertIsNotNone(tipo_mimetype) 
        self.assertEqual(tipo_mimetype, 'image/png') 

    
    def test_graficador_de_diagrama_circular(self):
        """ Se prueba la creación de la imagen con el diagrama circular y que el formato se corresponda con 
            el tipo de archivo solicitado """
        self.diagrama_circular.graficar_y_guardar()

        ruta_imagen = "tests/test_graficas/circular_test.png"
        self.assertTrue(os.path.exists(ruta_imagen), "El archivo no existe en la ruta especificada.")

        tipo_mimetype, _ = mimetypes.guess_type(ruta_imagen)
        self.assertIsNotNone(tipo_mimetype) 
        self.assertEqual(tipo_mimetype, 'image/png') 

    def test_graficador_de_diagrama_circular_animado(self):
        """ Se prueba la creación de la imagen con el diagrama circular animado y que el formato se corresponda con 
            el tipo de archivo solicitado """
        self.diagrama_circular_animado.graficar_y_guardar()

        ruta_imagen = "tests/test_graficas/circular_animado_test.gif"
        self.assertTrue(os.path.exists(ruta_imagen), "El archivo no existe en la ruta especificada.")

        tipo_mimetype, _ = mimetypes.guess_type(ruta_imagen)
        self.assertIsNotNone(tipo_mimetype) 
        self.assertEqual(tipo_mimetype, 'image/gif')

    def test_excepcion_formato_invalido_para_diagrama_circular_animado(self):
        """ Se prueba que se lance excepcion si se le pasa un formato invalido en la creación"""
        with self.assertRaises(ValueError):
            self.diagrama_circular_animado = GraficadorDeDiagramaCircularAnimado(self.diccionario_estado_frecuencia, "Reclamos" , "Estados",  "tests/test_graficas/",  "circular_animado_test", "png" )

    def test_graficador_de_diagrama_de_barras(self):
        """ Se prueba la creación de la imagen con el diagrama de barras y que el formato se corresponda con 
            el tipo de archivo solicitado """
        self.diagrama_de_barras.graficar_y_guardar()

        ruta_imagen = "tests/test_graficas/diagrama_de_barras_test.png"
        self.assertTrue(os.path.exists(ruta_imagen), "El archivo no existe en la ruta especificada.")

        tipo_mimetype, _ = mimetypes.guess_type(ruta_imagen)
        self.assertIsNotNone(tipo_mimetype) 
        self.assertEqual(tipo_mimetype, 'image/png') 


if __name__ == '__main__':
    unittest.main()
