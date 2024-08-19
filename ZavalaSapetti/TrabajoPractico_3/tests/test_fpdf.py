import unittest
import os
from modules.generador_informe import GeneradorPDF, GeneradorHTML  # Ajusta el nombre del módulo según sea necesario
from modules.graficador import GraficadorPastelYBarras  # Asegúrate de importar el graficador

class TestGeneradorInforme(unittest.TestCase):

    def setUp(self):
        self.datos = {
            'cantidad_reclamos': 100,
            'mediana_resueltos': 5.5,
            'mediana_en_proceso': 3.2
        }
        self.pdf_file = 'informe.pdf'
        self.html_file = 'informe.html'
        
        if not os.path.exists('static/estadistica'):
            os.makedirs('static/estadistica')
        
        # Crear un gráfico válido para la prueba utilizando GraficadorPastelYBarras
        self.image_path = 'static/estadistica/graficopastel.png'
        self.create_valid_graphic(self.image_path)

    def tearDown(self):
        # Eliminar los archivos de prueba después de cada test
        if os.path.exists(self.pdf_file):
            os.remove(self.pdf_file)
        if os.path.exists(self.html_file):
            os.remove(self.html_file)

        try:
            os.remove(self.image_path)
        except PermissionError:
            pass

    def create_valid_graphic(self, path):
        # Crear un gráfico válido utilizando GraficadorPastelYBarras
        lista_datos = [('Pendiente', 10), ('En Proceso', 20), ('Cerrado', 70)]
        graficador = GraficadorPastelYBarras('graficopastel', 'pastel', lista_datos)
        # Mover el archivo generado a la ruta esperada en el test
        if os.path.exists('static/estadistica/graficopastel.png'):
            os.rename('static/estadistica/graficopastel.png', path)

    def test_generar_pdf(self):
        generador_pdf = GeneradorPDF()
        generador_pdf.generar_informe(self.datos)
        # Verifica que el archivo PDF se haya creado
        self.assertTrue(os.path.exists(self.pdf_file))

    def test_generar_html(self):
        generador_html = GeneradorHTML()
        generador_html.generar_informe(self.datos)
        # Verifica que el archivo HTML se haya creado
        self.assertTrue(os.path.exists(self.html_file))

if __name__ == '__main__':
    unittest.main()
