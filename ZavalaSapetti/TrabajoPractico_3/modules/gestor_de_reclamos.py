import pickle
from modules.comparador_de_strings_en_español import ComparadorDeStrings
from datetime import datetime
from modules.models import TablaReclamos
from modules.entidades import Reclamo
from modules.classifier import ClaimsClassifier
from modules.clasificador_de_reclamos import ClasificadordeReclamos

class GestorDeReclamos ():
    """ Clase que modela un gestor de reclamos que interactua con un repositorio para obtener 
    y guardar los datos de reclamos, clasificandolos y realizando la comprobacion de existencia de reclamos similares.
    ------------------------------------------------
    Atributos:
    * clasificador: Clasificador
    * comparador_de_strings: ComparadorDeStrings
    * gestor_db: GestorDeBaseDeDatos
    * repositorio

    """
    def __init__(self ,  p_repositorio_concreto) -> None:

        self.__clasificador = ClasificadordeReclamos()
        self.__comparador_de_strings = ComparadorDeStrings()
        self.__repositorio = p_repositorio_concreto

#crear propia clase de clasificador 

    def crear_reclamo(self, p_id_creador, p_asunto, p_nombre_imagen, p_contenido, p_tiempo):
        """ Método que crea un Reclamo en Entidades y lo guarda en la base de datos""" 

        # Clasificar el reclamo para determinar el departamento correspondiente
        try:
            departamento_correspondiente = self.__clasificador.clasificar_reclamo(p_contenido)
            print("Departamento correspondiente: ", departamento_correspondiente)

        except Exception as e:
            print(e)
        

        # Crear el reclamo con los parámetros adecuados
        nuevo_reclamo = Reclamo({
            "id_creador" : p_id_creador,
            "asunto" : p_asunto,
            "contenido" : p_contenido,
            "imagen" : p_nombre_imagen, 
            "p_contenido" : p_contenido,
            "departamento" : departamento_correspondiente,
            "fecha" : datetime.now().replace(microsecond=0),
            "tiempo_de_resolucion":p_tiempo,
            "estado" : "Pendiente",
            "fecha_inicio_proceso" : 0  #nuevo parametro
        })

        self.__repositorio.guardar_reclamo(nuevo_reclamo)

        return nuevo_reclamo
    

    def cambiar_estado_de_reclamo(self, p_id_reclamo: int, p_nuevo_estado: str, p_tiempo_resolucion: int = None):
        """ Método que cambia el estado de un reclamo con id = p_id_reclamo en la base de datos
        a partir del respositorio concreto.
        """

        if p_nuevo_estado not in ['En Proceso','Resuelto', 'Pendiente', 'Inválido']:
            raise ValueError("El estado debe ser uno de los siguientes:'En Proceso','Resuelto', 'Pendiente', 'Inválido'.")

        # Actualizar el estado en la base de datos
        self.__repositorio.actualizar_atributo_en_instancia_en_tabla(TablaReclamos, p_id_reclamo, "estado", p_nuevo_estado)

        # Si el nuevo estado es 'En Proceso', también actualizar el tiempo de resolución
        if p_nuevo_estado == 'En Proceso' and p_tiempo_resolucion is not None:
            self.__repositorio.actualizar_atributo_en_instancia_en_tabla(TablaReclamos, p_id_reclamo, "tiempo_de_resolucion", p_tiempo_resolucion)
            self.__repositorio.actualizar_atributo_en_instancia_en_tabla(TablaReclamos, p_id_reclamo, "fecha_inicio_proceso", datetime.now())

        # Si el nuevo estado es 'Resuelto', calcular el tiempo real de resolución
        if p_nuevo_estado == 'Resuelto':
            reclamo = self.__repositorio.obtener_reclamo_por_id(p_id_reclamo)
            fecha_inicio_proceso = reclamo.fecha_inicio_proceso
            if fecha_inicio_proceso:
                dias_resolucion = (datetime.now() - fecha_inicio_proceso).days
                self.__repositorio.actualizar_atributo_en_instancia_en_tabla(TablaReclamos, p_id_reclamo, "tiempo_de_resolucion", dias_resolucion)


    def actualizar_atributo(self, p_id_reclamo: int, nombre_atributo: str, nuevo_valor):
        """Método genérico para actualizar cualquier atributo de un reclamo."""
        # Validar el nombre del atributo si es necesario
        if nombre_atributo not in TablaReclamos.__table__.columns.keys():
            raise ValueError(f"El atributo '{nombre_atributo}' no es válido para la tabla Reclamos.")

        # Se actualiza en base de datos
        self.__repositorio.actualizar_atributo_en_instancia_en_tabla(TablaReclamos, p_id_reclamo, nombre_atributo, nuevo_valor)


    def obtener_todos_los_reclamos(self):
        """Metodo que recupera datos de TablaReclamos desde self.__repositorio, crea instancias de Reclamo y las devuelve."""
        try:
            datos_reclamos = self.__repositorio.obtener_todas_las_instancias_de_la_tabla("TablaReclamos")

            reclamos = []
            for p_reclamo in datos_reclamos:
                #print(p_reclamo['departamento_correspondiente'])  
                usuarios_adheridos = self.obtener_usuarios_adheridos(p_reclamo['id'])
                reclamos.append(Reclamo({
                    "id": p_reclamo['id'],
                    "id_creador": p_reclamo['usuario_id'],
                    "asunto": p_reclamo['asunto'],
                    "contenido": p_reclamo['contenido'],
                    "imagen": p_reclamo['imagen'],
                    "departamento_correspondiente": p_reclamo['departamento_correspondiente'],
                    "fecha": p_reclamo['fecha'],
                    "estado": p_reclamo['estado'],
                    "tiempo_de_resolucion": p_reclamo['tiempo_de_resolucion'],
                    "usuarios_adheridos": usuarios_adheridos,
                    "fecha_inicio_proceso": p_reclamo['fecha_inicio_proceso']
                }))
            
            return reclamos
        
        except Exception as e:
            print(e)
            return []


    def obtener_reclamos_por_atributo(self, p_nombre_atributo, valor):

        if valor == "Maestranza" or valor == "Soporte Informático" or valor == "Secretaría Técnica":
            valor = valor.lower()

        datos_reclamos = self.__repositorio.obtener_instancias_por_atributo("TablaReclamos", p_nombre_atributo, valor)

        #print(datos_reclamos)

        reclamos = []
        for p_reclamo in datos_reclamos:
            usuarios_adheridos = self.obtener_usuarios_adheridos(p_reclamo['id'])
            reclamos.append(Reclamo({
                "id": p_reclamo['id'],
                "usuario_id": p_reclamo['usuario_id'],
                "asunto": p_reclamo['asunto'],
                "contenido": p_reclamo['contenido'],
                "imagen": p_reclamo['imagen'],
                "departamento_correspondiente": p_reclamo['departamento_correspondiente'],
                "fecha": p_reclamo['fecha'],
                "estado": p_reclamo['estado'],
                "tiempo_de_resolucion": p_reclamo['tiempo_de_resolucion'],
                "usuarios_adheridos": usuarios_adheridos,
                "fecha_inicio_proceso": p_reclamo['fecha_inicio_proceso']
            }))
        
        return reclamos
    
 
    def obtener_reclamos_similares_validos_para_adherir_a_creador(self, p_reclamo):
            """ Método que obtiene reclamos similares cuyo contenido sea similar al de p_reclamo. """
            reclamos_similares = []

            # Obtener todos los reclamos
            todos_los_reclamos = self.__repositorio.obtener_todas_las_instancias_de_la_tabla("TablaReclamos")

            # Filtrar los reclamos que cumplen con los criterios
            for reclamo_a_comparar in todos_los_reclamos:
                if self.__comparador_de_strings.comparar_strings(reclamo_a_comparar['contenido'], p_reclamo.contenido) > 0.2:
                    reclamos_similares.append(reclamo_a_comparar)

            return reclamos_similares

#useful?
    def obtener_ids_reclamos_adheridos_por_usuario(self, usuario_id):
        """ Método que obtiene todos los IDs de los reclamos adheridos por el usuario con id = usuario_id.
        """
        TablaUsuarios = self.__repositorio.tablas[1]  
        usuario = self.__repositorio.session.query(TablaUsuarios).filter_by(id=usuario_id).first() #identificar al creador 
          # Verificación de existencia de usuario
        if not usuario:
            raise ValueError(f"Usuario con id {usuario_id} no encontrado")
        return [reclamo.id for reclamo in usuario.reclamos_adheridos]

    def obtener_usuarios_adheridos(self, reclamo_id):
        """Método que obtiene todos los IDs de los usuarios adheridos a un reclamo con id = reclamo_id."""
        TablaReclamos = self.__repositorio.tablas[0]  
        reclamo = self.__repositorio.session.query(TablaReclamos).filter_by(id=reclamo_id).first()

        # Verificación de existencia de reclamo
        if not reclamo:
            raise ValueError(f"Reclamo con id {reclamo_id} no encontrado")
        
        # Devuelve una lista vacía si no hay usuarios adheridos
        return [usuario.id for usuario in reclamo.usuarios_adheridos] if reclamo.usuarios_adheridos else []
    

    def obtener_reclamos_adheridos_por_usuario(self, usuario_id):
        datos_reclamos = self.__repositorio.obtener_instancias_por_usuario_adherido("TablaReclamos", usuario_id)
        
        reclamos = []
        for p_reclamo in datos_reclamos:
            reclamo = Reclamo({
                "id": p_reclamo['id'],
                "id_creador": p_reclamo['usuario_id'],
                "asunto": p_reclamo['asunto'],
                "contenido": p_reclamo['contenido'],
                "imagen": p_reclamo['imagen'],
                "departamento_correspondiente": p_reclamo['departamento_correspondiente'],
                "fecha": p_reclamo['fecha'],
                "estado": p_reclamo['estado'],
                "tiempo_de_resolucion": p_reclamo['tiempo_de_resolucion'],
                "usuarios_adheridos": p_reclamo.get('usuarios_adheridos', [])
            })
            reclamos.append(reclamo)

        return reclamos


    def desadherir_usuario_de_reclamo(self, p_id_usuario, p_id_reclamo):
        try:
            reclamo = self.__repositorio.obtener_reclamo_por_id(p_id_reclamo)
            if reclamo:
                usuarios_adheridos = reclamo.get('usuarios_adheridos', [])
                if p_id_usuario in usuarios_adheridos:
                    usuarios_adheridos.remove(p_id_usuario)
                    self.__repositorio.actualizar_reclamo(p_id_reclamo, {'usuarios_adheridos': usuarios_adheridos})
                    return True
            return False
        except Exception as e:
            print(e)
            return False


    def adherir_usuario_a_reclamo(self, p_id_usuario, p_id_reclamo):
        """ Método que adhiere un usuario con id = p_id_usuario a un reclamo existente con id = p_id_reclamo
        y actualiza el numero de adheridos a dicho reclamo.
        
        Argumentos:
        * p_id_usuario: int
        * p_id_reclamo: int
        """
        # Obtener las tablas de usuarios y reclamos
        TablaUsuarios = self.__repositorio.tablas[1]
        TablaReclamos = self.__repositorio.tablas[0]

        # Obtener el usuario y el reclamo de la base de datos
        usuario = self.__repositorio.session.query(TablaUsuarios).filter_by(id=p_id_usuario).first()
        reclamo = self.__repositorio.session.query(TablaReclamos).filter_by(id=p_id_reclamo).first()

        if not usuario:
            raise ValueError(f"Usuario con id {p_id_usuario} no encontrado")
        if not reclamo:
            raise ValueError(f"Reclamo con id {p_id_reclamo} no encontrado")

        # Adherir el usuario al reclamo
        if usuario not in reclamo.usuarios_adheridos:
            reclamo.usuarios_adheridos.append(usuario)
            # Actualizar el número de adheridos
            reclamo.numero_adheridos = len(reclamo.usuarios_adheridos)
            self.__repositorio.session.commit()
        else:
            raise ValueError(f"Usuario con id {p_id_usuario} ya está adherido al reclamo con id {p_id_reclamo}")
        
        #nuevos cambios:
    
 

