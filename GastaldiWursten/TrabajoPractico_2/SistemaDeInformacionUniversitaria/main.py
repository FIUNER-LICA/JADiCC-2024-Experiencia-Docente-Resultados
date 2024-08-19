from modules.estudiante import Estudiante
from modules.profesor import Profesor
from modules.facultad import Facultad

def main ():
    #Usado en la creacion de un objeto facultad
    p1 = Profesor ("Wursten, Augusto Gabriel", 41526873, "07/01/1998")

    #Usado en la prueba del metodo para cambiar jefe de departamento (de forma individual, sin contemplar la lista de profesores)
    p2 = Profesor ("Gonzales, Pepe", 14589361, "24/06/1963")

    #Usado en la prueba del metodo que agrega profesores al curso
    p3 = Profesor ("Lara, Ricardo", 25896741, "09/03/1967")

    #Usado para agregar profesor al departamento
    p4 = Profesor ("Villancico, Noelia", 35687412, "27/07/2007")

    #Usado en la prueba del metodo que agrega estudiantes al curso
    e1 = Estudiante ("Alonso, Muriel", 38957412, "01/01/2001")

    e2 = Estudiante("Augusto W", 34875123, "12/10/1990")
    #Estos objetos son independientes de la Facultad, y en consecuencia de los departamentos y cursos

    #Se crea Facultad
    f1 = Facultad ("Matematica", p1, "FIUNER", "Oro Verde")
    print ("Facultad creada:")
    print()
    print (f1)

    print("-------------------------------------------------")

    #Se crea nuevo departamento para la facultad (contencion: composicon)
    f1.crear_departamento( p3, "Biologia")

    print("Se añade nuevo departamento\n")
    print(f1)


    print("-------------------------------------------------")

    #Se agrega p2 a la lista de profesores del departamento,
    #Luego se pueda asignar como jefe sin que corra la excepcion

    f1.asociar_profesor_a_departamento("Matematica", p2)

    #Director de departamento que se encuentra en la clase departamento se cambia con un método

    f1.asociar_director_a_departamento("Matematica", p2)

    print("Se agrega nuevo profesor a Matematica y lo asigna como nuevo jefe \n")
    print(f1)

    print("-------------------------------------------------")

    #Agrega cursos al departamento correspondiente
 
    f1.crear_curso("Matematica","Ecuaciones", p1)

    print ("Se agrega curso a Dep Matematica")

    #Agrega profesores al departamento

    f1.asociar_profesor_a_departamento("Biologia", p4)

    print ("Se agrega profesor a Dep Biologia \n")

    print(f1)


    print("-------------------------------------------------")

    #Asociar profesores son asociados al curso

    f1.asociar_profesor_a_curso("Matematica","Ecuaciones",p3)

    print("Se agrega Profesor al curso de Ecuaciones")


    #Se agregan estudiantes a la Facultad
    f1.añadir_estudiante(e1)
    f1.añadir_estudiante(e2)

    print("Se agregan Estudiantes a la facultad")

    #Estudiantes son asociados a un curso
    f1.asociar_estudiante_a_curso("Matematica","Ecuaciones", e1)
    f1.asociar_estudiante_a_curso("Matematica", "Ecuaciones" , e2)


    print("Se agregan Estudiantes al curso Ecuaciones \n")

    print (f1)

    print("-------------------------------------------------")

    print ("Estudiantes de la facultad:")
    for estudiante in f1.estudiantes:
        print("•",estudiante.apellidoynombre)

    print ("\n")

#Código para evaluar las excepciones propuestas en las clases (que el profesor ya sea
#director de un departamento, que el profesor no este en la lista de profesores del departamento
#en cuestion o que ya tenga un curso asociado.
    try:
        f1.asociar_director_a_departamento("Biologia",p2)
    except Exception as msj:
        print ("Excepcion 1: referida a que el profesor ya es director")
        print(msj)
        print ("\n")

    try:
        f1.asociar_director_a_departamento("Matematica",p4)
    except Exception as msj:
        print ("Excepcion 2: referida a que el profesor no esta en la lista de profesores del departamento")
        print(msj)
        print ("\n")

    try:
        f1.crear_curso("Biologia","Fisiologia y biofisica",p1)
    except Exception as msj:
        print ("Excepcion 3: referida a que el profesor no esta agregado a la lista de profesores del departamento")
        print(msj)
        print ("\n")

    try:
        f1.asociar_profesor_a_departamento("Biologia",p1)
        f1.crear_curso("Biologia","Fisiologia y biofisica", p1)
    except Exception as msj:
         print ("Excepcion 4: referida a que el profesor ya tiene un curso asociado")
         print(msj)



if __name__ == "__main__": 
    main()