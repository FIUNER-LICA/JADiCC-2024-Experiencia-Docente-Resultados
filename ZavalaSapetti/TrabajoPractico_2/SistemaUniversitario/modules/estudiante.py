from modules.persona_facultativa import Persona_facultativa

class Estudiante(Persona_facultativa):
    """ Clase que modela un Estudiante
    ----------------------------------
    Atributos:
    * Apellidoynombre: string
    * DNI: int 
    * Fechadenacimiento: string
    """
    def __init__(self, *args):
        super().__init__(*args) 
        self.__lista_de_cursos=[]


    
    def inscribirse_a_curso(self,p_curso):
        """ Método que asocia el curso al estudiante luego de hacer las comprobaciones pertinentes
        Argumentos:
        * p_curso: Curso
        """ 

        if self in p_curso.lista_de_estudiantes:
            self.__lista_de_cursos.append (p_curso)


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        salida = f"::: {self.apellidoynombre},  {self.dni}, {self.edad} ::: \n"
        return salida
    


if __name__ == "__main__":
    est = Estudiante('Tamara', 'Zavala', 96260531, 21)

    print(est)


