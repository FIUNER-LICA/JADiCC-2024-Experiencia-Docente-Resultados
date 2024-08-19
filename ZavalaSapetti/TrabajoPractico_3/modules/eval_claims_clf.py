import pickle

def clasificar(departamento):
  # Abrir el archivo con el clasificador y guardarlo en la variable clf
  with open('./data/claims_clf.pkl', 'rb') as archivo:
    clf  = pickle.load(archivo)

  # Ahora en clf tenemos el clasificador entrenado

  reclamo = [departamento]

  # Clasificar los reclamos
  return clf.clasificar(reclamo)[0]