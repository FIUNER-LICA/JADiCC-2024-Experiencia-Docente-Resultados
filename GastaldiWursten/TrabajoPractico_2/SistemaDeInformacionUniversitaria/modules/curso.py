
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
    def __init__(self, p_nombre , p_profesor):
        self.__nombre = p_nombre
        self.__lista_de_profesores = []
        self.__lista_de_estudiantes = []

        self.asociar_profesor_c(p_profesor)

    @property
    def nombre (self):
        return self.__nombre
    
    @property
    def lista_de_profesores (self):
        return self.__lista_de_profesores
    
    @property
    def lista_de_estudiantes (self):
        return self.__lista_de_estudiantes

    def asociar_profesor_c (self, p_nuevo_profesor):
        """ Método que asocia el profesor al curso luego de realizar las comprobaciones 
        pertinentes
        Argumentos:
        * p_nuevo_profesor: Profesor
        """    
        if not isinstance(p_nuevo_profesor, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
        
        if p_nuevo_profesor.curso_asociado == None:

            if p_nuevo_profesor not in self.lista_de_profesores:
                self.__lista_de_profesores.append(p_nuevo_profesor)
                p_nuevo_profesor.asociar_a_curso(self)
        else:
            raise Exception ("El profesor ya tiene un curso asociado")

        

    def asociar_estudiante_c (self, p_nuevo_estudiante):
        """ Método que asocia el estudiante al curso luego de realizar las comprobaciones 
        pertinentes
        Argumentos:
        * p_nuevo_estudiante: Estudiante
        """ 
        
        if not isinstance(p_nuevo_estudiante, Estudiante):
            raise TypeError("El objeto recibido no es de tipo Estudiante")

        if p_nuevo_estudiante in self.lista_de_estudiantes:
            p_nuevo_estudiante.asociar_a_curso(self)
        else:
            self.__lista_de_estudiantes.append(p_nuevo_estudiante)
            p_nuevo_estudiante.asociar_a_curso(self)


    def __str__(self):

        salida = f"::: ::: ::: ::: ::: ::: ➢ {self.__nombre}; "
        salida += f"Nro Profesores: {len(self.__lista_de_profesores)}; "
        salida += f"Nro Estudiantes: {len(self.__lista_de_estudiantes)}"
        return salida

#Esta porcion de codigo la usariamos para probar la clase de manera local
#if __name__ == "__main__":
        
        
