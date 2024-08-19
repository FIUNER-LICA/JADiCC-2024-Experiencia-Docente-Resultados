from modules.profesor import Profesor
from modules.estudiante import Estudiante

class Curso:
    """ Clase que modela un curso universitario
    -------------------------------------------
    Atributos:
    * Nombre: string
    * Lista_de_profesores: list [Profesor]
    * Lista_de_estudiantes: list [Estudiante]
    """
    def __init__(self, p_nombre , p_titular_profesor):
        self.__nombre = p_nombre
        self.__titular= p_titular_profesor
        self.__lista_de_profesores = []
        self.__lista_de_estudiantes = []
        if p_titular_profesor is not None:
            self.__lista_de_profesores = [p_titular_profesor]
            p_titular_profesor.asociar_como_titular_curso(self)
        else:
            self.__lista_de_profesores = []

    @property
    def nombre (self):
        return self.__nombre
    
    @property
    def titular (self):
        return self.__titular
    
    @property
    def lista_de_profesores (self):
        return self.__lista_de_profesores
    
    @property
    def lista_de_estudiantes (self):
        return self.__lista_de_estudiantes

    def asignar_titular_curso(self, p_titular_curso):
        """ Método que asocia el profesor a titular del curso luego de realizar las comprobaciones
        pertinentes (debe pertenecer a la lista de profesores del departamento)
        Argumentos:
        * p_titular_curso: Profesor
        """

        if not isinstance(p_titular_curso, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
        
        if p_titular_curso in self.__lista_de_profesores:  #en la funcion de profesor ya se de el valor true
        # if p_titular_curso in self.__lista_de_profesores and not p_titular_curso._es_titular:
            self._titular = p_titular_curso
            p_titular_curso._curso_dirigido = self
            # p_titular_curso._es_titular = True
        else:
            raise Exception("El profesor no se encuentra en la lista de profesores del curso o ya es titular de otro curso")

    def asociar_profesor_curso (self, p_nuevo_profesor):
        """ Método que asocia el profesor al curso luego de realizar las comprobaciones 
        pertinentes
        Argumentos:
        * p_nuevo_profesor: Profesor
        """    
        if not isinstance(p_nuevo_profesor, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
        
        if p_nuevo_profesor not in self.lista_de_profesores:
                self.__lista_de_profesores.append(p_nuevo_profesor)
                p_nuevo_profesor.asociar_a_curso(self)
    
        

    def asociar_estudiante_c (self, p_nuevo_estudiante):
        """ Método que asocia el estudiante al curso luego de realizar las comprobaciones 
        pertinentes
        Argumentos:
        * p_nuevo_estudiante: Estudiante
        """ 
        
        if not isinstance(p_nuevo_estudiante, Estudiante):
            raise TypeError("El objeto recibido no es de tipo Estudiante")

        self.__lista_de_estudiantes.append(p_nuevo_estudiante)
        p_nuevo_estudiante.inscribirse_a_curso(self)


    def __str__(self):

        salida = f"::: ::: ➢ {self.__nombre}; "
        salida += f"Nro Profesores: {len(self.__lista_de_profesores)}; "
        salida += f"Nro Estudiantes: {len(self.__lista_de_estudiantes)}"
        return salida

#Esta porcion de codigo la usariamos para probar la clase de manera local
#if __name__ == "__main__":
        