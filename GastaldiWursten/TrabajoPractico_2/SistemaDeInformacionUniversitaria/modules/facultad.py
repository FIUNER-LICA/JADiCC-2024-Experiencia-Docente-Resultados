from modules.departamento import Departamento
from modules.estudiante import Estudiante
from modules.profesor import Profesor

class Facultad:
    """ Clase que modela una Facultad
    ---------------------------------
    Atributos:
    * Nombre: string    
    * Ubicacion: string
    * Departamentos: dic(departamentos) 
    * Estudiantes: list(estudiante)
    """
    def __init__(self, p_nombre_primer_departamento , p_profesor_jefe_primer_departamento , p_nombre = "S/N", p_ubicacion = "Sin ubicacion" ):
        
        if not isinstance(p_profesor_jefe_primer_departamento, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")

        self.__nombre = p_nombre
        self.__ubicacion = p_ubicacion
        self.__departamentos = {}
        self.__estudiantes = []

        self.__departamentos[p_nombre_primer_departamento] = Departamento( p_profesor_jefe_primer_departamento, p_nombre_primer_departamento)

    @property
    def nombre (self):
        return self.__nombre
    
    @nombre.setter
    def nombre (self, p_nombre):
        
        self.__nombre = p_nombre

    @property
    def ubicacion (self):
        return self.__ubicacion
    
    @ubicacion.setter
    def ubicacion (self, p_ubicacion):   
        self.__ubicacion = p_ubicacion

    
    @property
    def estudiantes (self):
        return self.__estudiantes

    
    def crear_departamento(self, p_profesor_jefe_nuevo_departamento , p_nombre_nuevo_departamento = "S/N"):
        """ Método que crea el departamento y le asigna su director/a
        Argumentos:
        * p_profesor_jefe_nuevo_departamento: Profesor
        * p_nombre_nuevo_departamento: string
        """

        if not isinstance(p_profesor_jefe_nuevo_departamento, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
        
        self.__departamentos[p_nombre_nuevo_departamento]= ( Departamento( p_profesor_jefe_nuevo_departamento , p_nombre_nuevo_departamento ) )

    
    def añadir_estudiante(self, p_estudiante ):
        """ Método que añade el estudiante a la lista de estudiantes de la facultad
        Argumentos:
        * p_estudiante: Estudiante
        """    
        if not isinstance(p_estudiante, Estudiante):
            raise TypeError("El objeto recibido no es de tipo Estudiante")
        
        self.__estudiantes.append( p_estudiante )

    def asociar_profesor_a_departamento(self,p_nombre_departamento, p_profesor):
        """ Método que busca el departamento solicitado y si lo encuentra le indica que asocie 
        al profesor, luego de realizar las comprobaciones pertinentes.
        Argumentos:
        * p_nombre_departamento: String
        * p_nuevo_profesor: Estudiante
        """

        if not isinstance(p_profesor, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")

        if p_nombre_departamento not in self.__departamentos.keys():
            raise Exception("El nombre no coincide con ningun departamento")

        self.__departamentos[p_nombre_departamento].asociar_profesor_d(p_profesor)

    def asociar_director_a_departamento(self,p_nombre_departamento,p_nuevo_director_departamento):

        """ Método que busca el departamento solicitado y si lo encuentra le indica que asocie el profesor 
        como director del departamento, luego de realizar las comprobaciones pertinentes.
        Argumentos:
        * p_nombre_departamento: String
        * p_nuevo_director_departamento: Profesor
        """

        if p_nombre_departamento not in self.__departamentos.keys():
            raise Exception("El nombre no coincide con ningun departamento")

        if not isinstance(p_nuevo_director_departamento, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")


        self.__departamentos[p_nombre_departamento].asociar_director_departamento(p_nuevo_director_departamento)



    def crear_curso(self,p_nombre_departamento, p_nombre_nuevo_curso, p_profesor):
        """ Método que busca el departamento solicitado y si lo encuentra le indica que cree el curso 
        con el nombre y profesor recibidos, luego de realizar las comprobaciones pertinentes.
        Argumentos:
        * p_nombre_departamento: string
        * p_nombre_curso: string
        * p_profesor: Profesor
        """  

        if p_nombre_departamento not in self.__departamentos.keys():
            raise Exception("El nombre no coincide con ningun departamento")

        if not isinstance(p_profesor, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
        
        self.__departamentos[p_nombre_departamento].crear_curso(p_nombre_nuevo_curso,p_profesor)
        
    def asociar_profesor_a_curso (self, p_nombre_departamento ,p_nombre_nuevo_curso , p_profesor):
        """ Método que busca el departamento solicitado y si lo encuentra le indica que asocie el profesor 
        recibido al curso requerido, luego de realizar las comprobaciones pertinentes.
        Argumentos:

        * p_nombre_departamento: string
        * p_nombre_curso: string
        * p_profesor: Profesor

        """    

        if p_nombre_departamento not in self.__departamentos.keys():
            raise Exception("El nombre no coincide con ningun departamento")
        
        if not isinstance(p_profesor, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
        
        self.__departamentos[p_nombre_departamento].asociar_profesor_a_curso(p_nombre_nuevo_curso,p_profesor)
        
    def asociar_estudiante_a_curso(self, p_nombre_departamento ,p_nombre_curso, p_estudiante):
        """ Método que busca el departamento solicitado y si lo encuentra le indica que asocie el estudiante 
        al curso, luego de realizar las comprobaciones pertinentes.
        Argumentos:
        * p_nombre_departamento: string
        * p_nombre_curso: string
        * p_estudiante: Estudiante
        """ 

        if p_estudiante not in self.estudiantes:
            raise Exception("El estudiante no pertenece a la facultad")
            
        if p_nombre_departamento not in self.__departamentos.keys():
            raise Exception("El nombre no coincide con ningun departamento")
        
        if not isinstance(p_estudiante, Estudiante):
            raise TypeError("El objeto recibido no es de tipo Estudiante")
        

        self.__departamentos[p_nombre_departamento].asociar_estudiante_a_curso(p_nombre_curso, p_estudiante)
        

    def __str__(self):
        salida = f"::: {self.__nombre},  {self.__ubicacion} ::: \n"
        salida += "::: ::: Departamentos:" + "\n"

        for departamento in self.__departamentos.keys():
            salida += str(self.__departamentos[departamento])
        return salida

if __name__ == "__main__": 

    pass

