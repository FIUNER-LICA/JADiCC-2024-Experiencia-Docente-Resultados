from modules.persona_facultativa import Persona_facultativa

class Profesor(Persona_facultativa):
    """ Clase que modela un Profesor
    --------------------------------
    Atributos:
    * Apellidoynombre: string
    * DNI: int
    * Edad: string
    * Es_director: Bool
    * Es_titular: Bool
    * Lista_Cursos: list [Cursos] 
    * Lista_de_departamentos: list [Departamento]
    * Departamento_dirigido: Departamento
    
    """

    def __init__(self, *args):
        super().__init__(*args) 
        self.__es_director = False  
        self.__es_titular = False
        self.__lista_cursos= []
        self.__lista_de_departamentos = []
        self.__departamento_dirigido = None
        self.__curso_dirigido = None

    @property
    def es_director (self):
        return self.__es_director
    @property
    def es_titular (self):
        return self.__es_titular
    @property
    def lista_cursos (self):
        return self.__lista_cursos
    @property
    def lista_departamentos (self):
        return self.__lista_de_departamentos
    @property
    def departamento_dirigido (self):
        return self.__departamento_dirigido
    @property
    def curso_dirigido (self):
        return self.__curso_dirigido
    
    #ambos hacen controles sobre es director, debería eliminar el control de una de los lados?

    def asociar_como_director_departamento(self,p_departamento_a_dirigir):
        """ Método que asocia el profesor como jefe del departamento luego de realizar las comprobaciones
        pertinentes
        Argumentos:
        * p_departamento_a_dirigir: Departamento
        """  

        self.asociar_a_departamento(p_departamento_a_dirigir)
        if not self.__es_director and p_departamento_a_dirigir in self.__lista_de_departamentos:
            self.__es_director = True
            self.__departamento_dirigido = p_departamento_a_dirigir
        elif self.__es_director:
            raise Exception(f"El profesor ya es director del departamento {self.__departamento_dirigido.nombre}")
        elif p_departamento_a_dirigir not in self.__lista_de_departamentos:
            raise Exception("El departamento a dirigir no esta en la lista de departamentos a los que pertenece el profesor")


    def asociar_a_departamento (self, p_departamento):
        """ Método que añade el profesor al departamento luego de hacer las comprobaciones pertinentes
        Argumentos:
        * p_nuevo_departamento: Departamento
        """    
        
        if self in p_departamento.lista_de_profesores:
            if p_departamento not in self.__lista_de_departamentos:
                self.__lista_de_departamentos.append(p_departamento)
        

    def asociar_como_titular_curso(self,p_curso_titular):
        """ Método que asocia el profesor como titular del curso luego de realizar las comprobaciones
        pertinentes
        Argumentos:
        * p_curso_titular: Curso
        """      

        if self.__es_titular is True:
            raise Exception(f"El profesor ya es titular del curso {self.__curso_dirigido.nombre}")
        
        else:
            self.__curso_dirigido = p_curso_titular
            self.__es_titular = True
        

    
    def asociar_a_curso (self, p_curso):
        """ Método que añade el profesor al curso luego de hacer las comprobaciones pertinentes
        Argumentos:
        * p_nuevo_curso: Curso
        """    
        if self in p_curso.lista_de_profesores:
            self.__lista_cursos.append(p_curso)
    
    #if __name__ == "__main__": 