
class Calculadora:
    """Clase que realiza cálculos relacionados con los alimentos"""
     
    def __init__(self, cajon):
        self.cajon = cajon

    def calcular_peso_total(self):
        """Calcula el peso total de los alimentos en el cajón"""
        return sum(alimento.peso for alimento in self.cajon)

    def cantidad_de_alimento_de_tipo(self, p_clase_de_alimento):
        """Devuelve la cantidad de alimentos de un tipo específico en el cajón
        Argumentos:
        * p_clase_de_alimento: Alimento class
        Returns:
        * int """
        
        return len([alimento for alimento in self.cajon if isinstance(alimento, p_clase_de_alimento)])

    def calcular_aw_prom_tipo(self, p_clase_de_alimento):
        """Devuelve el aw promedio de los alimentos presentes en el cajón del tipo de la clase indicada
        Argumentos:
         * p_clase_de_alimento: Alimento class
        
        Returns:
         * promedio: float """
        
        cantidad = self.cantidad_de_alimento_de_tipo(p_clase_de_alimento)
        if cantidad != 0:
            promedio = round(sum([alimento.obtener_aw() for alimento in self.cajon if isinstance(alimento, p_clase_de_alimento)]) / cantidad, 2)
            return promedio
        else:
            return 0
        
     
        
        
