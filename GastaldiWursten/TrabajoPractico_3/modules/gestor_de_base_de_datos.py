# from sqlalchemy import inspect
from sqlalchemy import MetaData
class GestorDeBaseDeDatos ():
    """ Clase que modela un gestor de base de datos que interactua con una base de datos y sus tablas
    ------------------------------------------------
    Atributos:
    * db: DataBase
    * tablas: list(String)

    """

    def __init__(self, p_database):
        self.__db = p_database
        self.__tablas = [mapper.class_.__tablename__ for mapper in self.__db.Model.registry.mappers]
    
    @property
    def tablas(self):
        return self.__tablas

    def obtener_primer_coincidencia_en_tabla( self, p_nombre_tabla , p_nombre_columna, p_atributo_a_buscar):
        """ Método que devuelve los datos de la primera coincidencia en una tabla de la base de la base de datos
        en donde valor de columna = p_atributo_a_buscar

        Argumentos:
        * p_nombre_tabla: String
        * p_nombre_columna: String
        * p_atributo_a_buscar: AnyType
        
        Returns:
        * dict(keys:String, values:AnyType) or None       
        """ 

        if p_nombre_tabla not in self.__tablas:
            raise ValueError("Error: nombre de tabla inexistente")
        
        instancia_atributos = None
        
        tabla = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_tabla), None)
        
        instancia = self.__db.session.query(tabla).filter(getattr(tabla, p_nombre_columna) == p_atributo_a_buscar).first()

        if instancia != None:
            instancia_atributos = {columna.name: getattr(instancia, columna.name) for columna in instancia.__table__.columns}
        
        return instancia_atributos

    def obtener_todas_coincidencias_en_tabla(self,p_nombre_tabla , p_nombre_columna, p_atributo_a_buscar):

        """ Método que devuelve los datos de todas las coincidencias en una tabla de la base de la base de datos
        en donde valor de columna = p_atributo_a_buscar

        Argumentos:
        * p_nombre_tabla: String
        * p_nombre_columna: String
        * p_atributo_a_buscar: AnyType
        
        Returns:
        * list(dict(keys:String, values:AnyType)) or []       
        """ 

        if p_nombre_tabla not in self.__tablas:
            raise ValueError("Error: nombre de tabla inexistente")

        lista_datos_de_coincidencias = []
        
        
        tabla = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_tabla), None)
        
        
        lista_instancias_coincidentes = self.__db.session.query(tabla).filter(getattr(tabla, p_nombre_columna) == p_atributo_a_buscar).all()

        if lista_instancias_coincidentes != []:
            
            for instancia in lista_instancias_coincidentes:
                 lista_datos_de_coincidencias.append({columna.name: getattr(instancia, columna.name) for columna in instancia.__table__.columns})
        
        return  lista_datos_de_coincidencias
    
    def guardar_fila_en_tabla(self, p_nombre_tabla, p_datos):

        """ Método que guarda una instancia en la tabla p_nombre_tabla a partir de los p_datos recibidos.

        Argumentos:
        * p_nombre_tabla: String
        * p_datos: dict(keys:String, values:AnyType)  // las claves de los diccionarios deben coincidir con los 
        nombres de las columnas de la tabla y los valores con los tipos de datos permitidos en cada columna.
              
        """ 
        if p_nombre_tabla not in self.__tablas:
            raise ValueError("Error: nombre de tabla inexistente")
        
        tabla = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_tabla), None)
        
        fila_a_guardar = tabla(**p_datos)
        self.__db.session.add(fila_a_guardar)
        self.__db.session.commit()


    def actualizar_atributo_en_instancia_en_tabla(self, p_nombre_tabla, p_id_fila, p_nombre_atributo, p_nuevo_valor):

        """ Método que actualiza un atributo de una instancia existente en la tabla p_nombre_tabla a partir de los 
        p_nuevo_valor recibido.

        Argumentos:
        * p_nombre_tabla: String
        * p_id_fila: int                // primary_key
        * p_nombre_atributo : String    // nombre de la columna
        * p_nuevo_valor: AnyType        // debe coincidir con el tipo de valor aceptado en la columna            
        """ 
        if p_nombre_tabla not in self.__tablas:
            raise ValueError("Error: nombre de tabla inexistente")

        tabla = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_tabla), None)
        

        instancia_a_editar = self.__db.session.get(tabla , p_id_fila)

        if instancia_a_editar == None:
            raise ValueError("Error: p_id_fila inexistente en la tabla")

        setattr(instancia_a_editar, p_nombre_atributo, p_nuevo_valor)

        self.__db.session.commit()

    def obtener_instancias_asociadas_entre_tablas(self, p_nombre_primer_tabla, p_nombre_segunda_tabla, p_id_instancia_primer_tabla):
        """ Método que devuelve los datos de todas las instancias asociadas de p_nombre_segunda_tabla con la 
        instancia de p_nombre_primer_tabla de id = p_id_instancia_primer_tabla .

        Argumentos:
        * p_nombre_primer_tabla: String
        * p_nombre_segunda_tabla: String
        * p_id_instancia_primer_tabla: int
        
        Returns:
        * list(dict(keys:String, values:AnyType)) or []       
        """ 

        if p_nombre_primer_tabla not in self.__tablas:
            raise ValueError("Error: " + p_nombre_segunda_tabla + " nombre de tabla inexistente")
        
        if p_nombre_segunda_tabla not in self.__tablas:
            raise ValueError("Error: " + p_nombre_segunda_tabla + " nombre de tabla inexistente")

        lista_instancias_asociadas = []

        tabla_primer = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_primer_tabla), None)
        
        instancia_primer_tabla = self.__db.session.query(tabla_primer).filter(tabla_primer.id == p_id_instancia_primer_tabla).first()

        if instancia_primer_tabla == None:
            raise ValueError("Error: p_id_instancia_primer_tabla inexistente en la tabla " + p_nombre_primer_tabla)

        if instancia_primer_tabla is not None:
            relacion = getattr(instancia_primer_tabla, p_nombre_segunda_tabla.lower())

            for instancia_segunda_tabla in relacion:
                lista_instancias_asociadas.append({columna.name: getattr(instancia_segunda_tabla, columna.name) for columna in instancia_segunda_tabla.__table__.columns})

        return lista_instancias_asociadas
    
    def asociar_instancias_entre_tablas(self, p_nombre_primer_tabla, p_nombre_segunda_tabla, p_id_instancia_primer_tabla, p_id_instancia_segunda_tabla):
        """ Método que asocia una instancia de p_nombre_primer_tablade id = p_id_instancia_primer_tabla con una 
        instancia de p_nombre_segunda_tabla de id = p_id_instancia_segunda_tabla.

        Argumentos:
        * p_nombre_primer_tabla: String
        * p_nombre_segunda_tabla: String
        * p_id_instancia_primer_tabla: int
        * p_id_instancia_segunda_tabla: int    
        """ 

        if p_nombre_primer_tabla not in self.__tablas:
            raise ValueError("Error: " + p_nombre_segunda_tabla + " nombre de tabla inexistente")
        
        if p_nombre_segunda_tabla not in self.__tablas:
            raise ValueError("Error: " + p_nombre_segunda_tabla + " nombre de tabla inexistente")


        tabla_primer = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_primer_tabla), None)
        tabla_segunda = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_segunda_tabla), None)
        

        instancia_primer_tabla = self.__db.session.query(tabla_primer).filter(tabla_primer.id == p_id_instancia_primer_tabla).first()
        instancia_segunda_tabla = self.__db.session.query(tabla_segunda).filter(tabla_segunda.id == p_id_instancia_segunda_tabla).first()

        if instancia_primer_tabla == None:
            raise ValueError("Error: p_id_instancia_primer_tabla inexistente en la tabla " + p_nombre_primer_tabla)
        
        if instancia_segunda_tabla == None:
            raise ValueError("Error: p_id_instancia_segunda_tabla inexistente en la tabla " + p_nombre_segunda_tabla)


        if instancia_primer_tabla is not None and instancia_segunda_tabla is not None:
            getattr(instancia_primer_tabla, p_nombre_segunda_tabla.lower()).append(instancia_segunda_tabla)
            self.__db.session.commit()

    def desasociar_instancias_entre_tablas(self, p_nombre_primer_tabla, p_nombre_segunda_tabla, p_id_instancia_primer_tabla, p_id_instancia_segunda_tabla):

        """ Método que desasocia una instancia de p_nombre_primer_tablade id = p_id_instancia_primer_tabla con una 
        instancia de p_nombre_segunda_tabla de id = p_id_instancia_segunda_tabla.

        Argumentos:
        * p_nombre_primer_tabla: String
        * p_nombre_segunda_tabla: String
        * p_id_instancia_primer_tabla: int
        * p_id_instancia_segunda_tabla: int    
        """ 

        if p_nombre_primer_tabla not in self.__tablas:
            raise ValueError("Error: " + p_nombre_segunda_tabla + " nombre de tabla inexistente")
        
        if p_nombre_segunda_tabla not in self.__tablas:
            raise ValueError("Error: " + p_nombre_segunda_tabla + " nombre de tabla inexistente")
        
        tabla_primer = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_primer_tabla), None)
        tabla_segunda  = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_segunda_tabla), None)
        

        instancia_primer_tabla = self.__db.session.query(tabla_primer).filter(tabla_primer.id == p_id_instancia_primer_tabla).first()
        instancia_segunda_tabla = self.__db.session.query(tabla_segunda).filter(tabla_segunda.id == p_id_instancia_segunda_tabla).first()
        
        if instancia_primer_tabla == None:
            raise ValueError("Error: p_id_instancia_primer_tabla inexistente en la tabla " + p_nombre_primer_tabla)
        
        if instancia_segunda_tabla == None:
            raise ValueError("Error: p_id_instancia_segunda_tabla inexistente en la tabla " + p_nombre_segunda_tabla)

        if instancia_primer_tabla is not None and instancia_segunda_tabla is not None:
            getattr(instancia_primer_tabla, p_nombre_segunda_tabla.lower()).remove(instancia_segunda_tabla)

            self.__db.session.commit()

    def obtener_atributo_en_instancia_en_tabla(self, p_nombre_tabla, p_id_fila, p_nombre_atributo):
        """ Método que devuelve un atributo de una instancia existente en la tabla p_nombre_tabla.

        Argumentos:
        * p_nombre_tabla: String
        * p_id_fila: int                // primary_key
        * p_nombre_atributo : String    // nombre de la columna

        Returns:

        * AnyType // tipo almacenado en la columna          
        """ 
        if p_nombre_tabla not in self.__tablas:
            raise ValueError("Error: " + p_nombre_tabla + " nombre de tabla inexistente")

        tabla = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_tabla), None)
        
        instancia = self.__db.session.get(tabla , p_id_fila)

        if instancia == None:
            raise ValueError("Error: p_id_instancia inexistente en la tabla " + p_nombre_tabla)
        
        
        return getattr(instancia, p_nombre_atributo)


    def obtener_coincidencia_en_tabla_por_dos_atributos(self, p_nombre_tabla, p_nombre_columna, p_atributo_a_buscar, p_nombre_columna2, p_atributo_a_buscar2):

        """ Método que devuelve los datos de la primera coincidencia en una tabla de la base de la base de datos
        en donde valor de columna = p_atributo_a_buscar y columna2 = p_atributo_a_buscar2

        Argumentos:
        * p_nombre_tabla: String
        * p_nombre_columna: String
        * p_atributo_a_buscar: AnyType
        
        Returns:
        * dict(keys:String, values:AnyType) or None       
        """ 

        if p_nombre_tabla not in self.__tablas:
            raise ValueError("Error: nombre de tabla inexistente")
        

        tabla = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_tabla), None)
        
        return self.__db.session.query(tabla).filter(getattr(tabla, p_nombre_columna) == p_atributo_a_buscar, getattr(tabla, p_nombre_columna2) == p_atributo_a_buscar2).first()

    def obtener_todas_las_instancias_de_la_tabla(self, p_nombre_tabla):

        """ Método que devuelve los datos de todas las instancias en una tabla de la base de la base de datos.

        Argumentos:
        * p_nombre_tabla: String
        
        Returns:
        * list(dict(keys:String, values:AnyType)) or []       
        """ 

        if p_nombre_tabla not in self.__tablas:
            raise ValueError("Error: nombre de tabla inexistente")

        lista_datos_de_instancias = []
        
        tabla = next((mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_tabla), None)
    
        lista_todas_instancias = self.__db.session.query(tabla).all()

        if lista_todas_instancias:
            for instancia in lista_todas_instancias:
                lista_datos_de_instancias.append({columna.name: getattr(instancia, columna.name) for columna in instancia.__table__.columns})
    
        return lista_datos_de_instancias
    
    def obtener_valores_presentes_en_columna_de_tabla(self, p_nombre_tabla, p_nombre_columna):
        """ Método que devuelve los valores, sin repetir, presentes en una columna de la tabla p_nombre_tabla.

        Argumentos:
        * p_nombre_tabla: String
        * p_nombre_columna: String
        
        Returns:
        * list() or []       
        """ 
        if p_nombre_tabla not in self.__tablas:
            raise ValueError("Error: nombre de tabla inexistente")
        
        valores_unicos = []

        tabla = next(
        (mapper.class_ for mapper in self.__db.Model.registry.mappers if mapper.class_.__tablename__ == p_nombre_tabla), None
        )

        if tabla is not None:
            columnas = getattr(tabla, p_nombre_columna)
            query = self.__db.session.query(columnas).distinct().all()
            valores_unicos = [value[0] for value in query]

        return valores_unicos
