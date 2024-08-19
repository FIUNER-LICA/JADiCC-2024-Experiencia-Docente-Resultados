from modules.repositorio import Repositorio
from modules.entidades import Reclamo, Usuario
class RepositorioFalso(Repositorio):

    def __init__(self):
        super().__init__()
        self.reclamos = []
        self.usuarios = []
        self.__tablas = ['TablaReclamos', 'TablaUsuarios']  # Simulación de tablas
    
    @property
    def tablas(self):
        return self.__tablas
    @property
    def session(self):
        return self  # Devuelve el propio objeto para simular la sesión de la base de datos


    def leer_reclamo(self, id: int) -> Reclamo:
        for reclamo in self.reclamos:
            if reclamo.id == id:
                return reclamo
        raise ValueError("No se encuentra un reclamo con el ID proporcionado")

    def guardar_reclamo(self, reclamo: Reclamo) -> None:
        self.reclamos.append(reclamo)

    def guardar_usuario(self, usuario: Usuario) -> None:
        self.usuarios.append(usuario)

    def get_lista_reclamos(self):
        return self.reclamos
#se prueba esto?
    def obtener_primer_coincidencia_en_tabla(self, p_nombre_tabla: str, p_nombre_columna: str, p_atributo_a_buscar) -> dict:
        if p_nombre_tabla == "TablaReclamos":
            for reclamo in self.reclamos:
                if getattr(reclamo, p_nombre_columna) == p_atributo_a_buscar:
                    return {**reclamo.__dict__, 'id': reclamo.id}
        elif p_nombre_tabla == "TablaUsuarios":
            for usuario in self.usuarios:
                if getattr(usuario, p_nombre_columna) == p_atributo_a_buscar:
                    return {**usuario.__dict__, 'id': usuario.id}
        return None

    def obtener_instancias_por_atributo(self, nombre_tabla: str, nombre_atributo: str, valor) -> list:
        resultados = []
        if nombre_tabla == "TablaReclamos":
            resultados = [reclamo for reclamo in self.reclamos if getattr(reclamo, nombre_atributo) == valor]
        elif nombre_tabla == "TablaUsuarios":
            resultados = [usuario for usuario in self.usuarios if getattr(usuario, nombre_atributo) == valor]
        return [{**instancia.__dict__, 'id': instancia.id} for instancia in resultados]

    def obtener_reclamo_por_id(self, id: int) -> Reclamo:
        return self.leer_reclamo(id)
#innesesario
    def obtener_instancias_por_usuario_adherido(self, nombre_tabla: str, usuario_id: int) -> list:
        if nombre_tabla == "TablaReclamos":
            return [{**reclamo.__dict__, 'id': reclamo.id} for reclamo in self.reclamos if usuario_id in reclamo.usuarios_adheridos]
        return []
#probas con otros atributos 2 y 3ro
    def actualizar_atributo_en_instancia_en_tabla(self, TablaReclamos, p_id_reclamo, nombre_atributo, nuevo_valor):
        reclamo = self.leer_reclamo(p_id_reclamo)
        if nombre_atributo == "estado":
            reclamo.set_estado(nuevo_valor)
        elif nombre_atributo == "tiempo_de_resolucion":
            reclamo.set_tiempo_de_resolucion(nuevo_valor)
        elif nombre_atributo == "fecha_inicio_proceso":
            reclamo.set_fecha_inicio_proceso(nuevo_valor)
        else:
            setattr(reclamo, nombre_atributo, nuevo_valor)
#borrar?
    def obtener_todas_las_instancias_de_la_tabla(self, p_nombre_tabla: str) -> list:
        if p_nombre_tabla == "TablaReclamos":
            return [{**reclamo.__dict__, 'id': reclamo.id} for reclamo in self.reclamos]
        elif p_nombre_tabla == "TablaUsuarios":
            return [{**usuario.__dict__, 'id': usuario.id} for usuario in self.usuarios]
        return []
