import unittest
from modules.cajon import Cajon
from modules.cinta_transportadora import CintaTransportadora
from modules.alimento import Alimento


#Separar los test por las clases correspondientes   
class TestCintaTransportadora(unittest.TestCase):

    def setUp(self):

        self.cinta_transportadora = CintaTransportadora()
        
        self.cajon = Cajon()

        

    def test_cargar_caja_mediante_cinta_transportadora(self):
        " Prueba que se cargue la cantidad indicada de alimentos en la caja"
    #Raro
        cantidad = 100
        self.cinta_transportadora.cargar_alimentos(self.cajon , cantidad)

        # se comprueba la cantidad
        self.assertEqual( len(self.cajon), cantidad)
        



    
if __name__ == '__main__':
    unittest.main()