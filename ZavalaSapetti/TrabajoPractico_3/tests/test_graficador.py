import unittest
import os
from modules.graficador import GraficadorPastelYBarras 

class TestGraficadorPastelYBarras(unittest.TestCase):

    def setUp(self):
        self.nombre = 'test_grafico'
        self.formato_pastel = 'pastel'
        self.formato_barras = 'barras'
        self.lista_datos = [('Pendiente', 10), ('En Proceso', 20), ('Cerrado', 70)]
        self.ruta = 'test_grafico.png'
        
        # Asegurarse de que el directorio de destino existe
        if not os.path.exists('static/estadistica'):
            os.makedirs('static/estadistica')

    def tearDown(self):
        # Eliminar el archivo de prueba después de cada test
        if os.path.exists(os.path.join('static/estadistica', self.ruta)):
            os.remove(os.path.join('static/estadistica', self.ruta))

    def test_graficar_pastel(self):
        graficador = GraficadorPastelYBarras(self.nombre, self.formato_pastel, self.lista_datos, self.ruta)
        # Verifica que el archivo se haya creado
        self.assertTrue(os.path.exists(os.path.join('static/estadistica', self.ruta)))

    def test_graficar_barras(self):
        graficador = GraficadorPastelYBarras(self.nombre, self.formato_barras, self.lista_datos, self.ruta)
        # Verifica que el archivo se haya creado
        self.assertTrue(os.path.exists(os.path.join('static/estadistica', self.ruta)))

if __name__ == '__main__':
    unittest.main()
