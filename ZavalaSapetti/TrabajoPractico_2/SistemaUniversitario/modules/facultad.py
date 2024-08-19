from modules.estudiante import Estudiante
from modules.profesor import Profesor
from modules.departamento import Departamento
from modules.curso import Curso

class Facultad:
    """ Clase que modela una Facultad
    ---------------------------------
    Atributos:
    * Nombre: string    
    * Departamentos: dic(departamentos) 
    * Estudiantes: list(estudiante)
    * Profesores Contratados: list(profesor)
    """
    def __init__(self, p_nombre_primer_departamento, p_profesor_jefe_primer_departamento, p_nombre = "S/N"):
        
        if not isinstance(p_profesor_jefe_primer_departamento, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")

        self.__nombre = p_nombre
        self.__profesores_contratados=[]
        self.__estudiantes=[]
        self.__departamentos = {} 
        self.__departamentos[p_nombre_primer_departamento] = Departamento( p_profesor_jefe_primer_departamento, p_nombre_primer_departamento)

        #self._cursos= Departamento._lista_cursos
    @property
    def nombre (self):
        return self.__nombre
    @property
    def estudiantes (self):
        return self.__estudiantes
    
    @property
    def len_estudiantes (self):
        return len(self.__estudiantes)
    
    @property
    def len_profesores (self):
        return len(self.__profesores_contratados)
    
    @property
    def departamentos (self):
        return self.__departamentos
    @property
    def profesores_contratados (self):
        return self.__profesores_contratados

    def inscribir_estudiante_a_facultad (self, p_estudiante):
        """ Método que añade el estudiante a la lista de estudiantes de la facultad
        Argumentos:
        * p_estudiante: Estudiante
        """    
        if not isinstance(p_estudiante, Estudiante):
            raise TypeError("El objeto recibido no es de tipo Estudiante")
        
        self.__estudiantes.append( p_estudiante )


    def contratar_profesor(self, p_profesor):

        if not isinstance(p_profesor, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
        
        elif p_profesor not in self.__profesores_contratados:
            if isinstance(p_profesor, Profesor):
                self.__profesores_contratados.append(p_profesor) 
        else:
            raise ValueError(f'El profesor ya esta contratado')
        
    
    def listar_profesores(self):
        """ Metodo que crea una lista de todos los profesores en una cadena de caracteres"""

        salida = ""
        for i,profesor in enumerate(self.__profesores_contratados):
            salida += f"{i+1}. {profesor.apellidoynombre}; DNI: {profesor.dni}; Edad: {profesor.edad}\n"
        return salida 

    def listar_estudiantes(self):
        """ Metodo que crea una lista de todos los estudiantes en una cadena de caracteres"""

        salida = ""
        for i,estudiante in enumerate(self.__estudiantes):
            salida += f"{i+1}. {estudiante.apellidoynombre}; DNI: {estudiante.dni}\n"
        return salida 
    
    def listar_departamentos(self):
        """ Metodo que crea una lista de todos los departamentos en una cadena de caracteres"""

        salida_departamentos = ""
        for i, (departamento, info) in enumerate(self.__departamentos.items(), 1):
            nombre_departamento = departamento
            director = info.director.apellidoynombre
            salida_departamentos += f"{nombre_departamento}. Director: {director}\n"
        return salida_departamentos
    
    def listar_un_departamento(self, p_departamento):
        """ Metodo que crea una lista de un departamento en una cadena de caracteres
        P_departamento: str
        """

        if p_departamento in self.__departamentos:
            ob_departamento = self.__departamentos[p_departamento]
            return str(ob_departamento)

    def listar_cursos(self, p_departamento):
        """ Metodo que crea una lista de todos los departamentos en una cadena de caracteres"""
        departamento = self.__departamentos[p_departamento]
        salida_nombre_curso = ""
        for i, (curso, _) in enumerate(departamento.cursos.items(), 1):
            salida_nombre_curso += f"{curso}\n"
        return salida_nombre_curso


    def crear_departamento_en_facultad(self, p_indice_director  , p_nombre_nuevo_departamento = "S/N"):
        """ Método que crea el departamento y le asigna su director/a
        Argumentos:
        * p_indice_director: int
        * p_nombre_nuevo_departamento: string
        """
        ob_director = self.__profesores_contratados[p_indice_director]
        if not isinstance(ob_director, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
        
        self.__departamentos[p_nombre_nuevo_departamento] =  Departamento( ob_director , p_nombre_nuevo_departamento ) 


    def crear_curso(self,p_nombre_departamento, p_nombre_nuevo_curso, p_indice_profesor):
        """ Método que busca el departamento solicitado y si lo encuentra le indica que cree el curso 
        con el nombre y profesor recibidos, luego de realizar las comprobaciones pertinentes.
        Argumentos:
        * p_nombre_departamento: string
        * p_nombre_curso: string
        * p_indice_profesor: int
        """  
        #Acá recibiendo un índice, ya obtengo el objeto Profesor 
        if p_nombre_departamento not in self.__departamentos.keys():
            raise Exception("El nombre no coincide con ningun departamento")
        
        ob_departamento = self.__departamentos[p_nombre_departamento]
        ob_profesor = self.__profesores_contratados[p_indice_profesor - 1]

        if not isinstance(ob_profesor, Profesor):
            raise TypeError("El objeto recibido no es de tipo Profesor")
    
        ob_departamento.asociar_profesor_departamento(ob_profesor)
        self.__departamentos[p_nombre_departamento].crear_curso_d(p_nombre_nuevo_curso, ob_profesor)


    def asociar_profesor_a_curso (self, p_nombre_departamento ,p_nombre_curso , p_profesor):
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
        
        self.__departamentos[p_nombre_departamento].asociar_profesor_a_curso(p_nombre_curso,p_profesor)
        

    
    def asociar_estudiante_a_curso(self, p_nombre_departamento ,p_nombre_curso, p_indice_estudiante):
        """ Método que busca el departamento solicitado y si lo encuentra le indica que asocie el estudiante 
        al curso, luego de realizar las comprobaciones pertinentes.
        Argumentos:
        * p_nombre_departamento: string
        * p_nombre_curso: string
        * p_indice_estudiante: int
        """ 
        ob_estudiante = self.__estudiantes[p_indice_estudiante]

        if p_nombre_departamento not in self.__departamentos.keys():
            raise Exception("El nombre no coincide con ningun departamento")
        
        self.__departamentos[p_nombre_departamento].asociar_estudiante_a_curso(p_nombre_curso, ob_estudiante)
        

    def __str__(self):
        salida = f"::: {self.__nombre} ::: \n"
        salida += "::: Departamentos:" + "\n"

        for departamento in self.__departamentos.keys():
            salida += str(self.__departamentos[departamento])
        return salida 


if __name__ == "__main__":
    prof = Profesor("Lauro Macias",35,96260532)
    prof1 = Profesor("Kevin Macias",36,96270532)
    prof2 = Profesor("Maria Garcia",35,96268532)

    facultad = Facultad("Matematica", prof, "UNER")
    facultad.contratar_profesor(prof)
    facultad.contratar_profesor(prof1)
    facultad.contratar_profesor(prof2)


    str_profesores = facultad.listar_profesores()
    print(str_profesores)

