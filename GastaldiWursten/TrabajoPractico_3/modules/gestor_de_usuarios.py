from modules.gestor_de_base_de_datos import GestorDeBaseDeDatos
from modules.models import Usuario
from werkzeug.security import generate_password_hash


class ErrorUsuarioExistenteConMismoAtributoUnico(Exception):
    """ Clase que modela una exception relacionada a la presencia de usuarios con mismo atributo único
    """
    def __init__(self, mensaje):
        super().__init__(mensaje)

class GestorDeUsuarios():
    """ Clase que modela un gestor de usuario que interactua con un gestor de base de datos para obtener 
    y guardar los datos.
    ------------------------------------------------
    Atributos:
    * gestor_db: GestorDeBaseDeDatos
    """

    def __init__(self, p_gestor_base_de_datos) -> None:
        self.__gestor_db = p_gestor_base_de_datos

    def crear_nuevo_usuario(self, p_email, p_password, p_nombre_de_usuario, p_nombre, p_apellido, p_claustro, p_rol):
        """ Método que crea un nuevo usuario guardando sus datos en una base de datos a partir del gestor de base de datos
        , comprobando previamente la unicidad de los atributos que lo requieren.
        
        Argumentos:
        * p_email: String
        * p_password: String
        * p_nombre_de_usuario: String
        * p_nombre: String
        * p_claustro: String
        * p_rol: String        
        """ 
        if self.obtener_usuario_por_atributo_unico("nombre_de_usuario" , p_nombre_de_usuario) != None:
            raise ErrorUsuarioExistenteConMismoAtributoUnico("Ya existe un usuario registrado con el nombre de usuario ingresado")
        
        if self.obtener_usuario_por_atributo_unico("email", p_email) != None:
            raise ErrorUsuarioExistenteConMismoAtributoUnico("Ya existe un usuario registrado con el email ingresado")
        

        parametros_usuario = {
                  "email" : p_email,
                  "password" : generate_password_hash( password= p_password, method= 'pbkdf2:sha256', salt_length=8), 
                  "nombre_de_usuario" : p_nombre_de_usuario,
                  "nombre" : p_nombre,
                  "apellido" :  p_apellido,
                  "claustro" :  p_claustro,
                  "rol": p_rol}
        
        self.__gestor_db.guardar_fila_en_tabla("Usuarios", parametros_usuario)
        

    def obtener_usuario_por_atributo_unico(self, p_nombre_atributo, valor):
        """ Método que obtiene los datos de un usuario de una base de datos a partir de un atributo único 
        , utilizando del gestor de base de datos, y crea un objeto Usuario con estos para luego retornarlo.
        
        Argumentos:
        * p_nombre_atributo: String
        * valor: AnyType
        
        Returns:
        * Usuario or None        
        """ 

        if p_nombre_atributo not in ['id', 'email', 'nombre_de_usuario']:
            raise ValueError("El p_nombre_atributo debe ser 'id' ,'email' o 'nombre_de_usuario' .")

        usuario = None

        parametros_usuario = self.__gestor_db.obtener_primer_coincidencia_en_tabla("Usuarios", p_nombre_atributo, valor)
        
        if parametros_usuario != None:
            usuario = Usuario(**parametros_usuario)
        
        return usuario

    def modificar_atributo_usuario(self, p_usuario, p_nombre_atributo, p_nuevo_valor):

        """ Método que modifíca un atributo de un usuario tanto en su instancia actual pasada por parametro
        como tambien en la base de datos a haciendo uso del gestor de base de datos.

        Argumentos:
        * p_usuario: Usuario
        * p_nombre_atributo: String
        * p_nuevo_valor: AnyType
      
        """ 
        try:
            self.__gestor_db.actualizar_atributo_en_instancia_en_tabla("Usuarios", p_usuario.id , p_nombre_atributo , p_nuevo_valor)
        except:
            raise ErrorUsuarioExistenteConMismoAtributoUnico("Ya existe un usuario registrado con mismo " + p_nombre_atributo + " ingresado")
        #Modifico valores en instancia actual
        setattr(p_usuario, p_nombre_atributo, p_nuevo_valor)
        
    def cambiar_password_de_usuario(self, p_usuario , p_nuevo_password):
        
        """ Método que modifíca la contraseña de un usuario tanto en su instancia actual pasada por parametro
        como tambien en la base de datos a haciendo uso del gestor de base de datos.

        Argumentos:
        * p_usuario: Usuario
        * p_nuevo_password: String
      
        """ 
             
        nuevo_password = generate_password_hash( password= p_nuevo_password, method= 'pbkdf2:sha256', salt_length=8)

        #Se actualiza en usuario activo
        p_usuario.password = nuevo_password 

        #Se actualiza en la base de datos
        self.__gestor_db.actualizar_atributo_en_instancia_en_tabla("Usuarios", p_usuario.id , "password" , nuevo_password)

        
    