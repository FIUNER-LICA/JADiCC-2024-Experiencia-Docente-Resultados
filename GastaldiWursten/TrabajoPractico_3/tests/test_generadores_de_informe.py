import unittest
from modules.gestor_de_reclamos import GestorDeReclamos
from modules.generadores_de_informes_de_departamento import GeneradorDeInformeDeDepartamento, GeneradorDeInformeHTML , GeneradorDeInformePDF
from modules.generador_de_analiticos import GeneradorDeAnaliticosDeReclamos
import mimetypes
import random
import os

from modules.clasificador import Clasificador
import pickle


class TestClasesDeGeneradorDeInforme(unittest.TestCase):
    
    def setUp(self):

        gestor_reclamos = GestorDeReclamos(None)

        self.lista_asuntos = ["Agua", "Acceso", "Programación Avanzada"]
        self.lista_de_contenidos = ["Quisiera que mejore la calidad", "Me sirve mucho", "Me preocupan mas las pirañas"]
        
        reclamo_1 = gestor_reclamos.crear_reclamo(1, random.choice(self.lista_asuntos) , "img.png", random.choice(self.lista_de_contenidos))
        reclamo_2 = gestor_reclamos.crear_reclamo(2, random.choice(self.lista_asuntos) , "img.png", random.choice(self.lista_de_contenidos))
        reclamo_3 = gestor_reclamos.crear_reclamo(3, random.choice(self.lista_asuntos) , "img.png", random.choice(self.lista_de_contenidos))

        self.lista_de_reclamos = [reclamo_1 , reclamo_2 , reclamo_3]

        self.generador_de_analiticos_de_reclamos = GeneradorDeAnaliticosDeReclamos(self.lista_de_reclamos)

        self.informe_html = GeneradorDeInformeHTML(self.generador_de_analiticos_de_reclamos, "tests/test_informes/", "Secretaria Tecnica" )
        self.informe_pdf = GeneradorDeInformePDF(self.generador_de_analiticos_de_reclamos, "tests/test_informes/", "Secretaria Tecnica" )


    def test_tipo_generador_de_informe_de_departamento(self):
        """Se comprueba la herencia de las clases con generador de informe de departamento"""
        self.assertTrue(issubclass(GeneradorDeInformeHTML, GeneradorDeInformeDeDepartamento))
        self.assertTrue(issubclass(GeneradorDeInformePDF, GeneradorDeInformeDeDepartamento))


    def test_generador_informe_html(self):
        """ Se prueba la creación del informe y que el formato se corresponda con 
            el tipo de archivo solicitado """
        self.informe_html.generar_informe()

        ruta_informe = "tests/test_informes/reporte_reclamos.html"
        self.assertTrue(os.path.exists(ruta_informe), "El archivo no existe en la ruta especificada.")

        tipo_mimetype, _ = mimetypes.guess_type(ruta_informe)
        self.assertIsNotNone(tipo_mimetype) 
        self.assertEqual(tipo_mimetype, 'text/html') 

    
    def test_generador_informe_pdf(self):
        """ Se prueba la creación del informe y que el formato se corresponda con 
            el tipo de archivo solicitado """
        self.informe_pdf.generar_informe()

        ruta_informe = "tests/test_informes/reporte_reclamos.pdf"
        self.assertTrue(os.path.exists(ruta_informe), "El archivo no existe en la ruta especificada.")

        tipo_mimetype, _ = mimetypes.guess_type(ruta_informe)
        self.assertIsNotNone(tipo_mimetype) 
        self.assertEqual(tipo_mimetype, 'application/pdf') 

if __name__ == '__main__':
    unittest.main()