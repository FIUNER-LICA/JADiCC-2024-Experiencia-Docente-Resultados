class Usuario:

    def __init__(self, parametros_usuario):
        self.__id = parametros_usuario.get('id')
        self.__nombre = parametros_usuario.get('nombre')
        self.__apellido = parametros_usuario.get('apellido')
        self.__usuario = parametros_usuario.get('nombre_de_usuario')
        self.__email = parametros_usuario.get('email')
        self.__password = parametros_usuario.get('password')
        self.__rol = parametros_usuario.get('rol')


     # getters
    @property
    def id(self):
        return self.__id
    @property
    def nombre(self):
        return self.__nombre
    @property
    def apellido(self):
        return self.__apellido
    @property
    def username(self):
        return self.__usuario
    @property
    def email(self):
        return self.__email
    @property
    def password(self):
        return self.__password
    @property
    def rol(self):
        return self.__rol
# Flask-Login necesita implementar las propiedades: is_authenticated, is_active, is_anonymous y get_id
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__id)

    
    # setters
    def set_id(self, p_id):
        self.__id = p_id
    def set_nombre(self, p_nombre):
        self.__nombre = p_nombre 
    def set_apellido(self, p_apellido):
        self.__apellido = p_apellido
    def set_usuario(self, p_usuario):
        self.__usuario = p_usuario
    def set_email(self, p_email):
        self.__email = p_email
    def set_rol(self, p_rol):
        self.__rol = p_rol
    

class Reclamo:

    def __init__(self, parametros_usuario):
        self.__id = parametros_usuario.get('id')  # Mantenemos el id como None en la inicialización
        self.__usuario_id = parametros_usuario.get('usuario_id')
        self.__asunto = parametros_usuario.get('asunto')
        self.__contenido = parametros_usuario.get('contenido')
        self.__imagen = parametros_usuario.get('imagen')
        self.__departamento_correspondiente = parametros_usuario.get('departamento')
        self.__fecha = parametros_usuario.get('fecha')
        self.__estado = parametros_usuario.get('estado')
        self.__tiempo_de_resolucion = parametros_usuario.get('tiempo_de_resolucion', 0)
        self.__usuarios_adheridos = parametros_usuario.get("usuarios_adheridos", [])
        self.__fecha_inicio_proceso = parametros_usuario.get('fecha_inicio_proceso')

     # getters
    @property
    def id(self):
        return self.__id

    @property
    def usuario_id(self):
        return self.__usuario_id

    @property
    def asunto(self):
        return self.__asunto

    @property
    def contenido(self):
        return self.__contenido

    @property
    def imagen(self):
        return self.__imagen

    @property
    def departamento_correspondiente(self):
        return self.__departamento_correspondiente

    @property
    def fecha(self):
        return self.__fecha

    @property
    def estado(self):
        return self.__estado

    @property
    def tiempo_de_resolucion(self):
        return self.__tiempo_de_resolucion

    @property
    def usuarios_adheridos(self):
        return self.__usuarios_adheridos
    
    @property
    def fecha_inicio_proceso(self):
        return self.__fecha_inicio_proceso
   
    # setters
    def set_id(self, p_id):
        self.__id = p_id
    def set_usuario(self, p_usuario):
        self.__usuario_id = p_usuario
    def set_asunto(self, p_asunto):
        self.__asunto = p_asunto
    def set_usuarios_adheridos(self, p_usuarios_adheridos):
        self.__usuarios_adheridos = p_usuarios_adheridos
    def set_contenido(self, p_contenido):
        self.__contenido = p_contenido
    def set_departamento_correspondiente(self, p_departamento_correspondiente):
        self.__departamento_correspondiente = p_departamento_correspondiente
    def set_fecha(self, p_fecha):
        self.__fecha = p_fecha
    def set_estado(self, p_estado):
        self.__estado = p_estado
    def set_tiempo_de_resolucion(self, p_fecha_resolucion):
        self.__tiempo_de_resolucion = p_fecha_resolucion
    def set_fecha_inicio_proceso(self, p_fecha_inicio_proceso):
        self.__fecha_inicio_proceso = p_fecha_inicio_proceso