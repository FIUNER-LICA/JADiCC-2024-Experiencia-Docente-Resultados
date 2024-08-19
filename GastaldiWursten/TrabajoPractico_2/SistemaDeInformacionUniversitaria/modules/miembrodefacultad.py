class MiembroDeFacultad:
    """ Clase que modela un Miembro de Facultad
    -------------------------------------------
    Atributos:
    * Apellidoynombre: string
    * DNI: int
    * Fechadenacimiento: string
    """
    def __init__(self, p_apellidoynombre = "S/N", p_dni = 0, p_fechadenacimiento = "S/N"):
        self.__apellidoynombre = p_apellidoynombre
        self.__dni = p_dni
        self.__fechadenacimiento = p_fechadenacimiento
    
    @property
    def apellidoynombre (self):
        return self.__apellidoynombre
    
    @apellidoynombre.setter
    def apellidoynombre (self, p_apellidoynombre):
        
        self.__apellidoynombre = p_apellidoynombre

    @property
    def dni (self):
        return self.__dni
    
    @dni.setter
    def dni (self, p_dni):
        
        self.__dni = p_dni
    
    @property
    def fechadenacimiento (self):
        return self.__fechadenacimiento
    
    @fechadenacimiento.setter
    def fechadenacimiento (self, p_fechadenacimiento):
        
        self.__fechadenacimiento = p_fechadenacimiento


#Esta porcion de codigo la usariamos para probar la clase de manera local
#if __name__ == "__main__": 