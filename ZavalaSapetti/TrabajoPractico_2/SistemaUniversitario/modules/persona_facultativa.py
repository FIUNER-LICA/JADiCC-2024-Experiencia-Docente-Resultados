from abc import ABC


class Persona_facultativa():
    """ Clase que modela un Miembro de Facultad
    -------------------------------------------
    Atributos:
    * Apellidoynombre: string
    * DNI: int
    * Fechadenacimiento: string
    """

    def __init__ (self, p_apellidoynombre = "S/N", p_dni=0, p_edad =0 ):
        self.__apellidoynombre = p_apellidoynombre
        self.__edad = p_edad 
        self.__dni = p_dni 
        
    
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
    def edad (self):
        return self.__edad
    
    @edad.setter
    def edad (self, p_edad):
        
        self.__edad = p_edad


#Esta porcion de codigo la usariamos para probar la clase de manera local
#if __name__ == "__main__": 
   

        
    
        

        