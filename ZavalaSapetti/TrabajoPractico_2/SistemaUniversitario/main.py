from modules.estudiante import Estudiante
from modules.profesor import Profesor
from modules.facultad import Facultad, Departamento, Curso

def main():

    profesores=[]
    estudiantes=[]
    with open("./data/DATOS.txt", "r", encoding= "utf-8") as archi:
       for i in archi:
           nombreyapellido, dni, edad, tipo = i.strip().split(";")
           if tipo == "profesor":
              profesor = Profesor(nombreyapellido, dni, edad)
              profesores.append(profesor)
           elif tipo == "estudiante":
              estudiante = Estudiante(nombreyapellido, dni, edad)
              estudiantes.append(estudiante)    
    archi.close()
    
    #Se crea Facultad
    facultad = Facultad ("Matematica", profesores[0], "FIUNER")
    print ("Facultad creada:")
    print()
    print (facultad)

    for profesor in profesores:
        facultad.contratar_profesor(profesor)
    for estudiante in estudiantes:
        facultad.inscribir_estudiante_a_facultad(estudiante)
   
    while True:
        print("\n")
        print("|************************************************|")
        print("|**|     Sistema de Informacion Educativa     |**|")
        print("|**|                   Menu                   |**|")
        print("|************************************************|")
        print("")
        print("1.- Inscribir a Estudiante")
        print("2.- Contratar Profesor")
        print("3.- Crear departamento nuevo")
        print("4.- Crear curso nuevo")
        print("5.- Inscribir estudiante a un curso")
        print("6.- Salir")

        opcion = int(input("Opcion: "))

        if opcion == 1:
            input("A continuación pulse enter para ingresar los datos: \n")
            nombreyapellido = input("Nombre y apellido: ")
            edad = int(input("DNI: "))
            dni = int(input("Edad: "))

            estudiante = Estudiante(nombreyapellido, dni, edad)
            facultad.inscribir_estudiante_a_facultad(estudiante)

            print("\nEl estudiante ha sido cargado al sistema")

        elif opcion == 2:
            input("A continuación pulse enter para ingresar los datos:\n")
            nombreyapellido = input("Nombre y apellido: ")
            edad = int(input("DNI: "))
            dni = int(input("Edad: "))

            profesor = Profesor(nombreyapellido, dni, edad)
            facultad.contratar_profesor(profesor)

            print("\nEl docente ha sido cargado al sistema")

        elif opcion == 3:  
            nombre_departamento = input("Ingrese el nombre del nuevo departamento: ")
            print("Profesores en la facultad:")
            str_profesores = facultad.listar_profesores()
            print(str_profesores)
            
            # Solicitar al usuario que elija al director del departamento
            opcion_director = int(input("Seleccione al director del departamento: ")) - 1
            
            if opcion_director >= 0 and opcion_director < facultad.len_profesores:
                try:
                    # Crear el departamento con el director seleccionado
                    facultad.crear_departamento_en_facultad(opcion_director , nombre_departamento)  
                except Exception as e:
                    print(e)
                else:
                    print(" ")
                    print("\nLista de departamentos existentes:\n")
                    str_departamentos = facultad.listar_departamentos()
                    print(str_departamentos)
                    
            else:
                print("Opción inválida. Seleccione un profesor válido como director.")

        elif opcion == 4:
            nombre_curso = input("Ingrese el nombre del nuevo curso: ")

            print("Profesores en la facultad:")
            str_profesores = facultad.listar_profesores()
            print(str_profesores)
            
            opcion_titular = int(input("Seleccione al titular del curso: ")) - 1 
            if opcion_titular >= 0 and opcion_titular < facultad.len_profesores:
                
                #Ahora se elijirá el departamento en el que se quiere crear el curso:
                print("\nDepartamentos disponibles:")
                str_departamentos = facultad.listar_departamentos()
                print(str_departamentos)
                departamento_seleccionado = input("Indique el departamento: ")
                
                #Creacion del curso:
                try:
                    facultad.crear_curso(departamento_seleccionado, nombre_curso , opcion_titular)  
                    
                except Exception as e:
                    print(e)

                else:
                     print(f"\nLista de cursos existentes en {departamento_seleccionado}:")
                     print(facultad.listar_un_departamento(departamento_seleccionado)) 
                    
            else:
                print("Opción inválida. Seleccione un profesor válido como titular.")

            
        elif opcion == 5:
            print("Estudiantes en la facultad:")
            str_estudiantes = facultad.listar_estudiantes()
            print(str_estudiantes)
            
            opcion_estudiante = int(input("Seleccione al estudiante: ")) - 1
            
            if opcion_estudiante >= 0 and opcion_estudiante < facultad.len_estudiantes: 

                print("\nDepartamentos disponibles:")
                str_departamentos = facultad.listar_departamentos()
                print(str_departamentos)
                departamento_seleccionado = input("Indique el departamento: ")

                # Mostrar los cursos disponibles en el departamento seleccionado
                print(f"Cursos en el departamento {departamento_seleccionado}:")
                str_cursos = facultad.listar_cursos(departamento_seleccionado)
                print(str_cursos)
                curso_seleccionado = input("Ingrese el nombre del curso que desea seleccionar: ")
                
                try:
                    facultad.asociar_estudiante_a_curso(departamento_seleccionado, curso_seleccionado, opcion_estudiante)
                    print("El estudiante ha sido inscrito")
                except Exception as e:
                    print(e)
               
            else:
                print("Opción inválida. Seleccione un estudiante valido.")

            
        elif opcion == 6:
            print("Ha salido del sistema")
            break
        else:
            print("Opción inválida. Por favor, ingrese una opción válida.")


if __name__ == "__main__":
    main()