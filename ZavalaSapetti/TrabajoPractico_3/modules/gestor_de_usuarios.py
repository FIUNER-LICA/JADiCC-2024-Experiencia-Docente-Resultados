from modules.repositorio_concreto import RepositorioSQL
from modules.entidades import Usuario
from modules.models import TablaUsuarios, TablaReclamos
from werkzeug.security import generate_password_hash


class ErrorUsuarioExistenteConMismoAtributoUnico(Exception):
    """ Clase que modela una exception relacionada a la presencia de usuarios con mismo atributo único
    """
    def __init__(self, mensaje):
        super().__init__(mensaje)

class GestorUsuarios():
    """ Clase que modela un gestor de usuario que interactua con un gestor de base de datos para obtener 
    y guardar los datos.
    ------------------------------------------------
    Atributos:
    * gestor_db: RepositorioSQL
    """

    def __init__(self, p_repositorio_concreto) -> None:
        self.__repositorio = p_repositorio_concreto

    def crear_nuevo_usuario(self, parametros_usuario):
        """ Método que crea un nuevo usuario guardando sus datos en una base de datos a partir del gestor de base de datos
        , comprobando previamente la unicidad de los atributos que lo requieren.     
        """ 
        email = parametros_usuario["email"]
        nombre_de_usuario = parametros_usuario["nombre_de_usuario"]

        if self.obtener_usuario_por_atributo_unico("nombre_de_usuario" , nombre_de_usuario) != None:
            raise ErrorUsuarioExistenteConMismoAtributoUnico("Ya existe un usuario registrado con el nombre de usuario ingresado")
        
        if self.obtener_usuario_por_atributo_unico("email", email) != None:
            raise ErrorUsuarioExistenteConMismoAtributoUnico("Ya existe un usuario registrado con el email ingresado")
        
        parametros_usuario["password"] = generate_password_hash(password=parametros_usuario["password"], method='pbkdf2:sha256', salt_length=8)
        nuevo_usuario = Usuario(parametros_usuario)
        
        self.__repositorio.guardar_usuario(nuevo_usuario)
        

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

        parametros_usuario = self.__repositorio.obtener_primer_coincidencia_en_tabla("TablaUsuarios", p_nombre_atributo, valor)
        
        if parametros_usuario != None:
            usuario = Usuario(parametros_usuario)
        
        return usuario
    
    def adherir_usuario_a_reclamo(self, p_id_usuario, p_id_reclamo):
        with self.__repositorio.session() as session:
            usuario = session.query(TablaUsuarios).filter_by(id=p_id_usuario).first()
            reclamo = session.query(TablaReclamos).filter_by(id=p_id_reclamo).first()
            if not usuario or not reclamo:
                raise ValueError("Usuario o Reclamo no encontrado")
            if reclamo not in usuario.reclamos:
                usuario.reclamos.append(reclamo)
                reclamo.usuarios_adheridos.append(usuario)
                session.commit()
        
    