import pickle
from modules.classifier import ClaimsClassifier


class ClasificadordeReclamos:
    def __init__(self):
        with open('./data/claims_clf.pkl', 'rb') as archivo:
            self.__clasificador = pickle.load(archivo)

    def clasificar_reclamo(self, contenido):
        """Método para clasificar un reclamo y devolver el departamento correspondiente"""
        try:
            departamento_correspondiente = self.__clasificador.clasificar([contenido])[0]
            return departamento_correspondiente
        except Exception as e:
            print(e)
            return None
