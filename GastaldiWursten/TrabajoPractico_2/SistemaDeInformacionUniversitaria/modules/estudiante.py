#Esta porcion de codigo comentada la usariamos en caso de querer correr el 
#programa desde este archivo
#Usaremos preferentemente el main.py
#if __name__ == "__main__": 
#   from miembrodefacultad import MiembroDeFacultad
#else:
from modules.miembrodefacultad import MiembroDeFacultad


#Clase Estudiante que hereda de la clase base MiembroDeFacultad atributos y metodos
class Estudiante (MiembroDeFacultad):
    """ Clase que modela un Estudiante
    ----------------------------------
    Atributos:
    * Apellidoynombre: string
    * DNI: int 
    * Fechadenacimiento: string
    """
    def __init__(self, p_apellidoynombre="S/N", p_dni=0, p_fechadenacimiento="S/N"):
        super().__init__(p_apellidoynombre, p_dni, p_fechadenacimiento)
        self.__lista_de_cursos = []

    def asociar_a_curso (self, p_nuevo_curso):
        """ Método que asocia el curso al estudiante luego de hacer las comprobaciones pertinentes
        Argumentos:
        * p_nuevo_curso: Curso
        """ 

        if self in p_nuevo_curso.lista_de_estudiantes:
            self.__lista_de_cursos.append (p_nuevo_curso)
        else:
            p_nuevo_curso.asociar_estudiante_c(self)
            self.__lista_de_cursos.append (p_nuevo_curso)

  
    
    def __str__(self):
        salida = f"::: {self.apellidoynombre},  {self.dni}, {self.fechadenacimiento} ::: \n"
        return salida
    



#Esta porcion de codigo la usariamos para probar la clase de manera local
#if __name__ == "__main__": 
#    e2 = Estudiante ("Audicio Gastaldi, Marcelo Gaston", 35569187, "03/12/1990")
#    print (e2.apellidoynombre, e2.dni, e2.fechadenacimiento)