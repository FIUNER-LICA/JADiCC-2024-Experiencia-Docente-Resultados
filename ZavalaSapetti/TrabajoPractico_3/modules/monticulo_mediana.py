from modules.monticulo import Monticulo
class MonticuloMediana:

    def __init__(self, lista):
        self.__monticulo_max = Monticulo('max')  
        self.__monticulo_min = Monticulo('min')  
        self.__lista_de_valores = []
        self.mediana = 0
        self.agregar_valores(lista)
    
    def agregar_valores(self, lista):
       # print (lista)
        
        for valor in lista:
            self.__lista_de_valores.append(valor)
            if valor < self.mediana:
                self.__monticulo_max.insertar(valor)
            else:
                self.__monticulo_min.insertar(valor)

                # Balancear los montículos 
            if len(self.__monticulo_max) > len(self.__monticulo_min) + 1:
                self.__monticulo_min.insertar(self.__monticulo_max.eliminar_valor())
            elif len(self.__monticulo_min) > len(self.__monticulo_max) + 1:
                self.__monticulo_max.insertar(self.__monticulo_min.eliminar_valor())
            

            # Actualizar valor mediana
            if len(self.__monticulo_max) > len(self.__monticulo_min):
               self.mediana = self.__monticulo_max.raiz()
            elif len(self.__monticulo_min) > len(self.__monticulo_max):
               self.mediana = self.__monticulo_min.raiz()
            elif len(self.__monticulo_min) == len(self.__monticulo_max):
                self.mediana= (self.__monticulo_max.raiz()+self.__monticulo_min.raiz())/2



    def get_mediana(self):
        return self.mediana
    
    def actualizar_mediana(self,valor):
        self.agregar_valores([valor])
        self.get_mediana()
        
if __name__ == "__main__":
    lista= [1,2,-1,7,-2]
    mm = MonticuloMediana(lista)
    # mm.agregar_valores(lista)
    print(mm.get_mediana())
    mm.actualizar_mediana(3)
    print(mm.get_mediana())