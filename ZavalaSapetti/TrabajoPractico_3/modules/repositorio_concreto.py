from modules.repositorio import Repositorio
from modules.entidades import Reclamo, Usuario
from modules.models import TablaReclamos, TablaUsuarios, asociacion_usuarios_reclamos
from modules.config import app, db, login_manager
from datetime import datetime

#podrias probar un repositorio fake
#testear reclamos similares del gestor u probar la logica de otros metodos de gestores, el repo me daría una lista de reclamos

class RepositorioSQL(Repositorio):

    def __init__(self):
        super().__init__()
        with app.app_context():
            db.create_all()
        self.__tablas = [TablaReclamos, TablaUsuarios]

    @property
    def tablas(self):
        return self.__tablas
    @property
    def session(self):
        return db.session()
    
   
    def leer_reclamo(self, id: int) -> Reclamo:
        # Leer el reclamo de la base de datos
        modelo_reclamo = db.session.query(TablaReclamos).filter_by(id=id).first()
        if modelo_reclamo is None:
            raise ValueError("No se encuentra un reclamo con el ID proporcionado")
        reclamo = Reclamo({
            "id_creador": modelo_reclamo.usuario_id,
            "asunto": modelo_reclamo.asunto,
            "contenido": modelo_reclamo.contenido,
            "imagen": modelo_reclamo.imagen,
            "departamento_correspondiente": modelo_reclamo.departamento_correspondiente,
            "fecha": modelo_reclamo.fecha,
            "estado": modelo_reclamo.estado,
            "tiempo_de_resolucion": modelo_reclamo.tiempo_de_resolucion,
            "usuarios_adheridos": [usuario.id for usuario in modelo_reclamo.usuarios_adheridos]
        })

        return reclamo
            
    
    def guardar_reclamo(self, reclamo: Reclamo) -> None:

        modelo_reclamo_de_la_BD = db.session.query(TablaReclamos).order_by(TablaReclamos.id.desc()).first() # Se accede al regitro con mayor ID
        if modelo_reclamo_de_la_BD is not None:
            # Si lo hay, entonces, se debe tomar un ID igual al último de la tabla y sumarle 1
            reclamo.set_id(modelo_reclamo_de_la_BD.id + 1)
        else:
            # Caso contrario, establecer el id a 1.
            reclamo.set_id(1)

        # Se mapea un Libro a un ModeloLibro
        modelo_reclamo = self.__convertir_Reclamo_a_TablaReclamos(reclamo)

        # Se almacena el ModeloLibro
        db.session.add(modelo_reclamo)
        db.session.commit()

    def guardar_usuario(self, usuario: Usuario) -> None:
        #with self.session as session:
        modelo_usuario_de_la_BD = db.session.query(TablaUsuarios).order_by(TablaUsuarios.id.desc()).first() # Se accede al regitro con mayor ID
        if modelo_usuario_de_la_BD is not None:
            usuario.set_id(modelo_usuario_de_la_BD.id + 1)
        else:
            usuario.set_id(1)

        # Se mapea un Libro a un ModeloLibro
        modelo_usuario = self.__convertir_Usuario_a_TablaUsuarios(usuario)

        db.session.add(modelo_usuario)
        db.session.commit()


    def get_lista_reclamos(self):
        lista_de_reclamos = []
        # levantar todos los libros de la BD
        #with self.session as session:
        modelos_reclamos = db.session.query(TablaReclamos).all() # Equivale a: modelos_libros = ModeloLibro.query.all()
        mr = modelos_reclamos[0]
        for modelo_reclamo in modelos_reclamos:        
            libro = self.__convertir_TablaReclamos_a_Reclamo(modelo_reclamo)
            # añadir cada libro a la lista de libros
            lista_de_reclamos.append(libro)

        return lista_de_reclamos

    def __convertir_Reclamo_a_TablaReclamos(self, reclamo: Reclamo) -> None:
        modelo_reclamo = TablaReclamos(
            id=reclamo.id,
            usuario_id=reclamo.usuario_id,
            asunto=reclamo.asunto,
            contenido=reclamo.contenido,
            imagen=reclamo.imagen,
            departamento_correspondiente=reclamo.departamento_correspondiente,
            fecha=reclamo.fecha if isinstance(reclamo.fecha, datetime) else datetime.strptime(reclamo.fecha, '%Y-%m-%d').date(),
            estado=reclamo.estado,
            tiempo_de_resolucion= reclamo.tiempo_de_resolucion if reclamo.tiempo_de_resolucion is not None else 0,
            )
        return modelo_reclamo
    
    def __convertir_Usuario_a_TablaUsuarios(self, usuario: Usuario) -> None:
        modelo_usuario = TablaUsuarios(
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            username=usuario.username,
            rol=usuario.rol,
            email=usuario.email,
            password=usuario.password,
        )
        return modelo_usuario

    def __convertir_TablaReclamos_a_Reclamo(self, modelo_reclamo: TablaReclamos) -> Reclamo:
        reclamo = Reclamo({
            "id_usuario": modelo_reclamo.usuario_id,
            "asunto": modelo_reclamo.asunto,
            "contenido": modelo_reclamo.contenido,
            "imagen": modelo_reclamo.imagen,
            "departamento": modelo_reclamo.departamento_correspondiente,
            "fecha": modelo_reclamo.fecha,
            "estado": modelo_reclamo.estado,
            "tiempo_de_resolucion": modelo_reclamo.tiempo_de_resolucion,
            "usuarios_adheridos":[usuario.id for usuario in modelo_reclamo.usuarios_adheridos]})    

        return reclamo
    
    def obtener_primer_coincidencia_en_tabla(self, p_nombre_tabla: str, p_nombre_columna: str, p_atributo_a_buscar) -> dict:
        """Método que devuelve los datos de la primera coincidencia en una tabla de la base de datos
        en donde el valor de la columna es igual a p_atributo_a_buscar.

        Argumentos:
        - p_nombre_tabla: str
        - p_nombre_columna: str
        - p_atributo_a_buscar: AnyType

        Returns:
        - dict(keys: str, values: AnyType) or None       
        """
        if p_nombre_tabla not in [table.__tablename__ for table in self.__tablas]:
            raise ValueError("Error: nombre de tabla inexistente")
        
        tabla = next((table for table in self.__tablas if table.__tablename__ == p_nombre_tabla), None)
        if tabla is None:
            raise ValueError("Error: tabla no encontrada")

        instancia = db.session.query(tabla).filter(getattr(tabla, p_nombre_columna) == p_atributo_a_buscar).first()
        if instancia is None:
            return None

        instancia_atributos = {columna.name: getattr(instancia, columna.name) for columna in instancia.__table__.columns}
        return instancia_atributos

    def obtener_instancias_por_atributo(self, nombre_tabla: str, nombre_atributo: str, valor) -> list:
        """Obtener todas las instancias de una tabla que coinciden con un atributo y valor específicos.

        Argumentos:
        - nombre_tabla: str
        - nombre_atributo: str
        - valor: AnyType

        Returns:
        - list(dict) con las instancias encontradas
        """
        if nombre_tabla not in [table.__tablename__ for table in self.__tablas]:
            raise ValueError(f"Error: nombre de tabla '{nombre_tabla}' inexistente")
        
        tabla = next((table for table in self.__tablas if table.__tablename__ == nombre_tabla), None)
        if tabla is None:
            raise ValueError(f"Error: tabla '{nombre_tabla}' no encontrada")

        instancias = db.session.query(tabla).filter(getattr(tabla, nombre_atributo) == valor).all()
        return [instancia.__dict__ for instancia in instancias]

    def obtener_reclamo_por_id(self, id: int) -> Reclamo:
        modelo_reclamo = db.session.query(TablaReclamos).filter_by(id=id).first()
        if modelo_reclamo is None:
            raise ValueError("No se encuentra un reclamo con el ID proporcionado")
        reclamo = self.__convertir_TablaReclamos_a_Reclamo(modelo_reclamo)
        return reclamo
    
    def obtener_instancias_por_usuario_adherido(self, nombre_tabla: str, usuario_id: int) -> list:
        """Obtener todas las instancias de una tabla donde el usuario esté adherido.
        - list(dict) con las instancias encontradas
        """
        if nombre_tabla not in [table.__tablename__ for table in self.__tablas]:
            raise ValueError(f"Error: nombre de tabla '{nombre_tabla}' inexistente")
        
        tabla = next((table for table in self.__tablas if table.__tablename__ == nombre_tabla), None)
        if tabla is None:
            raise ValueError(f"Error: tabla '{nombre_tabla}' no encontrada")

        instancias = db.session.query(tabla).filter(tabla.usuarios_adheridos.any(id=usuario_id)).all()
        return [instancia.__dict__ for instancia in instancias]

    
    def actualizar_atributo_en_instancia_en_tabla(self, TablaReclamos, p_id_reclamo, nombre_atributo, nuevo_valor):
        """
        Método para actualizar el valor de un atributo específico de una instancia en la tabla de reclamos.
        
        :param TablaReclamos: La clase de la tabla donde se actualizará el atributo
        :param p_id_reclamo: El ID de la instancia que se desea actualizar
        :param nombre_atributo: El nombre del atributo que se desea actualizar
        :param nuevo_valor: El nuevo valor del atributo
        """
        with app.app_context():
            try:
                # Obtener la instancia a actualizar
                instancia = db.session.query(TablaReclamos).filter_by(id=p_id_reclamo).one()
                # Actualizar el atributo
                setattr(instancia, nombre_atributo, nuevo_valor)
                # Guardar los cambios en la base de datos
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print(e)
    
    def obtener_todas_las_instancias_de_la_tabla(self, p_nombre_tabla: str) -> list:
        """ Método que devuelve los datos de todas las instancias en una tabla de la base de datos.

        Argumentos:
        - p_nombre_tabla: str
        
        Returns:
        - list(dict(keys: str, values: AnyType)) or []
        """
        # Verificar si la tabla existe en las tablas conocidas
        if p_nombre_tabla not in [table.__tablename__ for table in self.__tablas]:
            raise ValueError("Error: nombre de tabla inexistente")

        # Obtener la tabla
        tabla = next((table for table in self.__tablas if table.__tablename__ == p_nombre_tabla), None)
        if tabla is None:
            raise ValueError(f"Error: tabla '{p_nombre_tabla}' no encontrada")

        # Consultar la base de datos para obtener todas las instancias
        lista_todas_instancias = db.session.query(tabla).all()

        # Convertir las instancias a una lista de diccionarios
        lista_datos_de_instancias = [
            {columna.name: getattr(instancia, columna.name) for columna in instancia.__table__.columns}
            for instancia in lista_todas_instancias
        ]

        return lista_datos_de_instancias

#instancias = db.session.query(TablaReclamos).filter(getattr(TablaReclamos, 'departamento_correspondiente') == 'Departamento A').all()
#return [instancia.__dict__ for instancia in instancias]


#if __name__ == "__main__":
