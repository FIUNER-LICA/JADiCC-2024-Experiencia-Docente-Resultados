from modules.curso import Curso
from modules.profesor import Profesor
from modules.estudiante import Estudiante

class Departamento:
    """ Clase que modela un Departamento de Facultad
    ------------------------------------------------
    Atributos:
    * Nombre: string
    * Director: Profesor
    * Lista_de_profesores: list (Profesor)
    * Cursos: Dic (Curso)
    """
    def __init__(self, p_director_departamento, p_nombre_departamento):

        self.__nombre = p_nombre_departamento
        self.__director = p_director_departamento
        self.__lista_de_profesores = [p_director_departamento]
        self.__cursos = {}

        
    @property
    def nombre (self):
        return self.__nombre
    
    @nombre.setter
    def nombre (self, p_nombre_departamento):
        self.__nombre = p_nombre_departamento
    
    @property
    def director (self):
        return self.__director
    
    
    @property  
    def lista_de_profesores (self):
         return self.__lista_de_profesores
    
        
    def asociar_director_departamento(self, p_nuevo_director_departamento):
        """ Método que asocia el profesor a director del departamento luego de realizar las comprobaciones
        pertinentes (debe ocupar unsolo puesto de direccion y pertenecer a la lista de profesores del departamento)
        Argumentos:
        * p_nuevo_director_departamento: Profesor
        """

        if not isinstance(p_nuevo_director_departamento, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")


        if p_nuevo_director_departamento in self.__lista_de_profesores and not p_nuevo_director_departamento.es_director:
            self.__director = p_nuevo_director_departamento
            p_nuevo_director_departamento.asociar_como_director_departamento(self)
        
        elif p_nuevo_director_departamento not in self.__lista_de_profesores:
             raise Exception("El profesor no se encuentra en la lista de profesores")
        
        elif p_nuevo_director_departamento.es_director:
            raise Exception("El profesor ya es director de otro departamento")

    
    def crear_curso (self, p_nombre_curso , p_profesor):
         """ Método que crea el curso
        Argumentos:
        * p_nombre_curso: string
        * p_profesor: Profesor
        """    
         
         if not isinstance(p_profesor, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
         
         if p_profesor not in self.lista_de_profesores:
             raise Exception("El profesor no puede iniciar un curso porque no pertenece al departamento")
         
         self.__cursos[p_nombre_curso] = Curso(p_nombre_curso, p_profesor)
    
    
    
    def asociar_profesor_d (self, p_nuevo_profesor):
        """ Método que asocia el profesor al departamento luego de realizar las comprobaciones
        pertinentes
        Argumentos:
        * p_nuevo_profesor: Estudiante
        """    

        if p_nuevo_profesor in self.lista_de_profesores:
            p_nuevo_profesor.asociar_a_departamento(self)
        else:
            self.__lista_de_profesores.append(p_nuevo_profesor)
            p_nuevo_profesor.asociar_a_departamento(self)

    def asociar_profesor_a_curso(self,p_nombre_curso,p_nuevo_profesor):
        """ Método que busca el curso solicitado y si lo encuentra le indica que asocie el profesor, 
        luego de realizar las comprobaciones pertinentes.
        Argumentos:
        * p_nombre_curso: string
        * p_nuevo_profesor: Profesor
        """    
        
        if p_nombre_curso not in self.__cursos.keys():
            raise Exception("El nombre no coincide con ningun Curso")
        
        if not isinstance(p_nuevo_profesor, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
        
        self.__cursos[p_nombre_curso].asociar_profesor_c(p_nuevo_profesor)
        
    def asociar_estudiante_a_curso(self, p_nombre_curso, p_estudiante):
        """ Método que busca el curso solicitado y si lo encuentra le indica que asocie el estudiante,
        luego de realizar las comprobaciones pertinentes.
        Argumentos:
        * p_nombre_curso: string
        * p_estudiante: Estudiante
        """ 

        if p_nombre_curso not in self.__cursos.keys():
            raise Exception("El nombre no coincide con ningun curso")
        
        if not isinstance(p_estudiante, Estudiante):
            raise TypeError("El objeto recibido no es de tipo Estudiante")
        

        self.__cursos[p_nombre_curso].asociar_estudiante_c (p_estudiante)
    

    def __str__(self):
        salida = f"::: ::: ::: ◉ {self.nombre}; Jefe: {self.director.apellidoynombre} ; Nro Profesores: {len(self.__lista_de_profesores)} \n"
        salida += f"::: ::: ::: ::: Cursos:\n"
        
        if len(self.__cursos) < 1:
             salida += "::: ::: ::: ::: ::: ::: No hay cursos registrados \n"
        else:
            for cursos in self.__cursos.values():
                salida += f"{str(cursos)}" + "\n"

        return salida
    

#Esta porcion de codigo la usariamos para probar la clase de manera local
#if __name__ == "__main__": 

  
