class Monticulo:
    def __init__(self,tipo):
        self.__tipo= tipo
        self.__lista_monticulo = [0]
        self.tamano_actual = 0

   
    def __infiltrar_arriba(self,i): 
        if self.__tipo == "min":
            while i // 2 > 0:   # El padre del nodo actual se puede calcular dividiendo el índice del nodo actual por 2.
                if self.__lista_monticulo[i] < self.__lista_monticulo[i // 2]:
                    tmp = self.__lista_monticulo[i // 2]
                    self.__lista_monticulo[i // 2] = self.__lista_monticulo[i]
                    self.__lista_monticulo[i] = tmp
                i = i // 2
        else:
            while i // 2 > 0:   
                if self.__lista_monticulo[i] > self.__lista_monticulo[i // 2]:
                    tmp = self.__lista_monticulo[i // 2]
                    self.__lista_monticulo[i // 2] = self.__lista_monticulo[i]
                    self.__lista_monticulo[i] = tmp
                i = i // 2
        

    def insertar(self,k):
        self.__lista_monticulo.append(k)
        self.tamano_actual = self.tamano_actual + 1
        self.__infiltrar_arriba(self.tamano_actual)
    
    def __infiltar_abajo(self,i):
        if self.__tipo == "min":
            while (i * 2) <= self.tamano_actual:
                hm = self.__hijo_min(i)
                if self.__lista_monticulo[i] > self.__lista_monticulo[hm]:
                    tmp = self.__lista_monticulo[i]
                    self.__lista_monticulo[i] = self.__lista_monticulo[hm]
                    self.__lista_monticulo[hm] = tmp
                i = hm
        else:
            while (i * 2) <= self.tamano_actual:
                hm = self.__hijo_max(i)
                if self.__lista_monticulo[i] < self.__lista_monticulo[hm]:
                    tmp = self.__lista_monticulo[i]
                    self.__lista_monticulo[i] = self.__lista_monticulo[hm]
                    self.__lista_monticulo[hm] = tmp
                i = hm



    def __hijo_min(self,i):
        if i * 2 + 1 > self.tamano_actual:
            return i * 2
        else:
            if self.__lista_monticulo[i*2] < self.__lista_monticulo[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1
            
    def __hijo_max(self,i):
        if i * 2 + 1 > self.tamano_actual:
            return i * 2 
        else:
            if self.__lista_monticulo[i*2] > self.__lista_monticulo[i*2+1]:
                return i * 2 
            else:
                return i * 2 + 1
            
    def eliminar_valor(self):
        """Elimina y devuelve el valor de la raíz del montículo"""
        valor_sacado = self.__lista_monticulo[1]
        self.__lista_monticulo[1] = self.__lista_monticulo[self.tamano_actual]
        self.tamano_actual = self.tamano_actual - 1
        self.__lista_monticulo.pop()
        self.__infiltar_abajo(1)
        return valor_sacado

    def raiz(self):
        return self.__lista_monticulo[1]

    def _comparar(self, a, b):
        if self.__tipo == 'min':
            return a < b
        else:
            return a > b

    def __len__(self):
        return len(self.__lista_monticulo)

if __name__ == "__main__":
    monticulo = Monticulo('min')
    monticulo.insertar(5)
    monticulo.insertar(3)
    monticulo.insertar(8)
    monticulo.insertar(1)
    print(monticulo.raiz())