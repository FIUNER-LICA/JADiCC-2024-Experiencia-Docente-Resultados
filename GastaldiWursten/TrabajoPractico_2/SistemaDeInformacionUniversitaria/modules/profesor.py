from modules.miembrodefacultad import MiembroDeFacultad



#Clase Estudiante que hereda de la clase base MiembroDeFacultad atributos y metodos
class Profesor (MiembroDeFacultad):
    """ Clase que modela un Profesor
    --------------------------------
    Atributos:
    * Apellidoynombre: string
    * DNI: int
    * Fechadenacimiento: string
    * Curso_asociado: Curso
    * Lista_de_departamentos: list [Departamento]
    * Departamento_en_direccion: Departamento
    * Es_director: Bool
    """
    def __init__(self, p_apellidoynombre="S/N", p_dni=0, p_fechadenacimiento="S/N"):
        super().__init__(p_apellidoynombre, p_dni, p_fechadenacimiento)
        self.__curso_asociado = None
        self.__lista_de_departamentos = []
        self.__departamento_en_direccion = None
        self.__es_director = False

    @property
    def es_director (self):
        return self.__es_director
    
    @es_director.setter
    def es_director(self, p_director):
        self.__es_director = p_director

    @property
    def departamento_en_direccion (self):
        return self.__departamento_en_direccion
    
    @departamento_en_direccion.setter
    def departamento_en_direccion(self, p_departamento_en_direccion):
            self.__departamento_en_direccion = p_departamento_en_direccion

    @property
    def curso_asociado(self):
        return self.__curso_asociado


    def asociar_como_director_departamento(self,p_departamento_a_dirigir):
        """ Método que asocia el profesor como jefe del departamento luego de realizar las comprobaciones
        pertinentes
        Argumentos:
        * p_departamento_a_dirigir: Departamento
        """    
        if not self.es_director and p_departamento_a_dirigir in self.__lista_de_departamentos:
            if p_departamento_a_dirigir.director != self:
                p_departamento_a_dirigir.asociar_director_departamento(self)
            else:
                self.departamento_en_direccion = p_departamento_a_dirigir
                self.es_director = True

        elif self.es_director:
            raise Exception("El profesor ya es director")
        elif p_departamento_a_dirigir not in self.__lista_de_departamentos:
            raise Exception("El departamento a dirigir no esta en la lista de departamentos a los que pertenece el profesor")


    def asociar_a_departamento (self, p_nuevo_departamento):
        """ Método que añade el profesor al departamento luego de hacer las comprobaciones pertinentes
        Argumentos:
        * p_nuevo_departamento: Departamento
        """    
        
        if self in p_nuevo_departamento.lista_de_profesores:
            self.__lista_de_departamentos.append(p_nuevo_departamento)
        else:
            p_nuevo_departamento.asociar_profesor_d(self)
            self.__lista_de_departamentos.append(p_nuevo_departamento)
    
    def asociar_a_curso (self, p_nuevo_curso):
        """ Método que añade el profesor al curso luego de hacer las comprobaciones pertinentes
        Argumentos:
        * p_nuevo_curso: Curso
        """    

        if self.__curso_asociado == None:

            if self not in p_nuevo_curso.lista_de_profesores:
                p_nuevo_curso.asociar_profesor_c(self)
            else:
                self.__curso_asociado = p_nuevo_curso

        else:
            raise Exception ("El profesor ya tiene un curso asociado")

    
    
    def __str__(self):
        salida = f"::: {self.apellidoynombre},  {self.dni}, {self.fechadenacimiento} ::: \n"
        return salida

#Esta porcion de codigo la usariamos para probar la clase de manera local
#if __name__ == "__main__": 
