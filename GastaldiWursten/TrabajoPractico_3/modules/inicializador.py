from modules.gestor_de_base_de_datos import GestorDeBaseDeDatos
from modules.gestor_de_usuarios import GestorDeUsuarios

def inicializar(  gestor_usuarios ,  gestor_departamento ):
    """ Metodo que inicializa la base de datos con los usuarios jefes y sus depártamentos correspondientes
    """

    with open('data\datos_iniciales_PA_TPI.txt', 'r', encoding='utf-8') as file:
        
        lineas = file.readlines()

    for linea in lineas:
        # Divide la línea por comas
        campos = linea.strip().split(',')

        if len(campos) == 8:
            nombre, apellido, claustro, rol, nombre_de_usuario, email, password, nombre_departamento = campos
            print("nombre",nombre,"apellido", apellido, "claustro",claustro,"rol", rol, "nombre_de_usuario", nombre_de_usuario, "email", email, password, nombre_departamento)
            # Se utiliza los valores para crear un nuevo usuario
            if gestor_usuarios.obtener_usuario_por_atributo_unico("nombre_de_usuario", nombre_de_usuario) == None:
                gestor_usuarios.crear_nuevo_usuario(email, password, nombre_de_usuario, nombre, apellido, claustro, rol)

        usuario_jefe = gestor_usuarios.obtener_usuario_por_atributo_unico("email",email)
        if gestor_departamento.obtener_departamento_por_nombre(nombre_departamento) == None:
            gestor_departamento.crear_nuevo_departamento(nombre_departamento, usuario_jefe.id)