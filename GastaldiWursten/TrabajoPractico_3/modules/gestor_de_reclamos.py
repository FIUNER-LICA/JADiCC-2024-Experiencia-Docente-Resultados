import pickle
from modules.comparador_de_strings_en_español import ComparadorDeStrings
from datetime import datetime
from modules.models import Reclamo
from modules.clasificador import Clasificador


class GestorDeReclamos ():
    """ Clase que modela un gestor de reclamos que interactua con un gestor de base de datos para obtener 
    y guardar los datos de reclamos, clasificandolos y realizando la comprobacion de existencia de reclamos similares.
    ------------------------------------------------
    Atributos:
    * clasificador: Clasificador
    * comparador_de_strings: ComparadorDeStrings
    * gestor_db: GestorDeBaseDeDatos

    """
    def __init__(self ,  p_gestor_base_de_datos) -> None:

        with open('.\data\clasificador_svm.pkl' , 'rb') as archivo:
            self.__clasificador = pickle.load(archivo)

        self.__comparador_de_strings = ComparadorDeStrings()
        self.__gestor_db = p_gestor_base_de_datos

    def crear_reclamo(self, p_id_creador, p_asunto, p_nombre_imagen , p_contenido):
        """ Método que crea un nuevo reclamo, sin guardarlo en base de datos.
        
        Argumentos:
        * p_id_creador: int
        * p_asunto: String
        * p_nombre_imagen: String
        * p_contenido: String

        Returns:

        * Reclamo        
        """ 

        parametros_reclamo = {}

        parametros_reclamo["usuario_id" ] = p_id_creador
        parametros_reclamo["asunto" ] = p_asunto
        parametros_reclamo["nombre_imagen" ] = p_nombre_imagen
        parametros_reclamo["contenido" ] = p_contenido
        parametros_reclamo["departamento_correspondiente"] = self.__clasificador.clasificar([p_contenido])[0]
              
        parametros_reclamo["fecha_y_hora"] = datetime.now().replace(microsecond=0)
        parametros_reclamo["estado"] = "Pendiente"
        parametros_reclamo["numero_adheridos"] = 1
        

        return Reclamo (**parametros_reclamo)
    
    def guardar_reclamo(self, p_reclamo):
        """ Método que guarda los datos de un reclamo en la base de datos usando el gestor de base de datos.
        
        Argumentos:
        * p_reclamo: Reclamo
       
        """ 
         
        #Obtengo diccionario con los parametros del reclamo
        dict_parametros_reclamo = {columna.name: getattr(p_reclamo, columna.name) for columna in p_reclamo.__table__.columns}
    
        #Guardo los datos en la base de datos
        self.__gestor_db.guardar_fila_en_tabla("Reclamos", dict_parametros_reclamo)

            
    
    def obtener_reclamos_similares_validos_para_adherir_a_creador(self, p_reclamo):
        """ Método que obtiene reclamos similares del mismo departamento que p_reclamo,
        cuyo creador no sea el mismo que el de p_reclamo y donde el creador de p_reclamo 
        no se encuentre actualmente adherido. 
        
        Argumentos:
        * p_reclamo: Reclamo

        Returns:

        * list(Reclamo) or []  
        
        """
         
        reclamos_similares = []
        

        reclamos_del_departamento = self.obtener_reclamos_por_atributo("departamento_correspondiente", p_reclamo.departamento_correspondiente)
        ids_reclamos_adheridos = self.obtener_ids_reclamos_adheridos_por_usuario(p_reclamo.usuario_id)

        if reclamos_del_departamento != []:
            for reclamo_a_comparar in reclamos_del_departamento:
                 if reclamo_a_comparar.usuario_id != p_reclamo.usuario_id and reclamo_a_comparar.id not in ids_reclamos_adheridos:
                    if (self.__comparador_de_strings.comparar_strings(reclamo_a_comparar.contenido, p_reclamo.contenido) > 0.2):
                        reclamos_similares.append(reclamo_a_comparar)

        return reclamos_similares
    
    
    def obtener_reclamos_adheridos_por_usuario(self, p_usuario_id):
        """ Método que obtiene reclamos actualmente adheridos por el usuario con id = p_usuario_id (sin
        tener en cuenta los creados por él mismo). 
        
        Argumentos:
        * p_usuario_id: int

        Returns:

        * list(Reclamo) or []  
        
        """

        reclamos_adheridos = []
         
        datos_reclamos_vinculados = self.__gestor_db.obtener_instancias_asociadas_entre_tablas("Usuarios","Reclamos",p_usuario_id)
         
        if datos_reclamos_vinculados != []:
             for p_reclamo in datos_reclamos_vinculados:
                  if p_reclamo["usuario_id"] != p_usuario_id:
                    reclamos_adheridos.append(Reclamo(**p_reclamo))
        
        return reclamos_adheridos

    def adherir_usuario_a_reclamo(self, p_id_usuario, p_id_reclamo):
         """ Método que adhiere un usuario con id = p_id_usuario a un reclamo existente con id = p_id_reclamo
         y actualiza el numero de adheridos a dicho reclamo.
        
         Argumentos:
         * p_usuario_id: int
         * p_id_reclamo: int

         """
         self.__gestor_db.asociar_instancias_entre_tablas("Usuarios","Reclamos",p_id_usuario, p_id_reclamo)

         #Actualizo el numero de adheridos
         numero_adheridos =  self.__gestor_db.obtener_atributo_en_instancia_en_tabla( "Reclamos", p_id_reclamo, "numero_adheridos")
         self.__gestor_db.actualizar_atributo_en_instancia_en_tabla("Reclamos", p_id_reclamo, "numero_adheridos", numero_adheridos + 1)

    def desadherir_usuario_a_reclamo(self, p_id_usuario, p_id_reclamo):
         """ Método que desadhiere un usuario con id = p_id_usuario a un reclamo existente con id = p_id_reclamo
         y actualiza el numero de adheridos a dicho reclamo.
        
         Argumentos:
         * p_usuario_id: int
         * p_id_reclamo: int

         """
         self.__gestor_db.desasociar_instancias_entre_tablas("Usuarios","Reclamos",p_id_usuario, p_id_reclamo)

         #Actualizo el número de adheridos
         numero_adheridos =  self.__gestor_db.obtener_atributo_en_instancia_en_tabla( "Reclamos", p_id_reclamo, "numero_adheridos")
         self.__gestor_db.actualizar_atributo_en_instancia_en_tabla("Reclamos", p_id_reclamo, "numero_adheridos", numero_adheridos - 1)


    def cambiar_estado_de_reclamo(self, p_id_reclamo, p_nuevo_estado):
        """ Método que cambia el estado de un reclamo con id = p_id_reclamo en la base de datos
        a partir del gestor de base de datos.
        
         Argumentos:
         * p_id_reclamo: int
         * p_nuevo_estado: String

        """
          
        if p_nuevo_estado not in ['En Proceso','Resuelto', 'Pendiente', 'Inválido']:
            raise ValueError("'En Proceso','Resuelto', 'Pendiente', 'Inválido'.")
          
        #Se actualiza en base de datos
        self.__gestor_db.actualizar_atributo_en_instancia_en_tabla( "Reclamos", p_id_reclamo, "estado", p_nuevo_estado)

 

    def cambiar_departamento_correspondiente_de_reclamo(self, p_id_reclamo, p_nuevo_nombre_departamento ):
        """ Método que cambia el departamento correspondiente de un reclamo con id = p_id_reclamo en la base de datos
        a partir del gestor de base de datos.
        
         Argumentos:
         * p_id_reclamo: int
         * p_nuevo_nombre_departamento: String

        """        
        #Se verifica la existencia de departamento
        if self.__gestor_db.obtener_primer_coincidencia_en_tabla("Departamentos", "nombre_departamento", p_nuevo_nombre_departamento ) == None:
            raise ValueError("nombre de dapartamento no existe")
        
        self.__gestor_db.actualizar_atributo_en_instancia_en_tabla("Reclamos", p_id_reclamo,"departamento_correspondiente", p_nuevo_nombre_departamento)


    def existe_reclamo_similar_del_mismo_creador(self, p_reclamo):
        """ Método que comprueba la existencia de un reclamo con el mismo asunto o contenido,
        creado por el mismo usuario que p_reclamo.
        
         Argumentos:
         * p_reclamo: Reclamo

         Returns:
         * Bool       
        """    

        reclamo_mismo_asunto = self.__gestor_db.obtener_coincidencia_en_tabla_por_dos_atributos("Reclamos", "usuario_id", p_reclamo.usuario_id, "asunto", p_reclamo.asunto)
        reclamo_mismo_contenido = self.__gestor_db.obtener_coincidencia_en_tabla_por_dos_atributos("Reclamos", "usuario_id", p_reclamo.usuario_id, "contenido", p_reclamo.contenido)

        return reclamo_mismo_asunto != None or reclamo_mismo_contenido != None
    
    def obtener_todos_los_reclamos(self):
        """ Método que obtiene todos los reclamos presentes en la base de datos.

        Returns:
        * list(Reclamo) or []  
        
        """
        reclamos = []

        datos_reclamos = self.__gestor_db.obtener_todas_las_instancias_de_la_tabla("Reclamos")
        
        if datos_reclamos != []:
             for p_reclamo in datos_reclamos:
                  reclamos.append(Reclamo(**p_reclamo))
        
        return reclamos
    
    def obtener_ids_reclamos_adheridos_por_usuario(self, p_usuario_id):
        """ Método que obtiene todos los ids de los reclamos adheridos por el usuario con id = p_usuario_id .

        Argumentos:
         * p_usuario_id: int

        Returns:
         * list(int) or []  
        
        """

        ids_reclamos_adheridos = []
         
        datos_reclamos_asocidados = self.__gestor_db.obtener_instancias_asociadas_entre_tablas("Usuarios","Reclamos",p_usuario_id)
         
        if datos_reclamos_asocidados != []:
             for p_reclamo in datos_reclamos_asocidados:
                  if p_reclamo["usuario_id"] != p_usuario_id:
                    ids_reclamos_adheridos.append(p_reclamo["id"])
        
        return ids_reclamos_adheridos

    def obtener_reclamos_por_atributo(self, p_nombre_atributo, p_valor_atributo):
        """ Método que obtiene todos los reclamos con atributo = valor.

        Argumentos:
         * p_nombre_atributo: String
         * p_valor_atributo: int

        Returns:
         * list(Reclamo) or []  
        
        """
         
        if p_nombre_atributo not in ["id", "usuario_id", "asunto", "nombre_imagen", "contenido","fecha_y_hora", 
                                      "departamento_correspondiente", "estado", "numero_adheridos"]:
             
             raise ValueError("El nombre_del_atributo no coincide con los atributos de Reclamo")

        reclamos = []

        datos_reclamos_que_coinciden = self.__gestor_db.obtener_todas_coincidencias_en_tabla("Reclamos", p_nombre_atributo, p_valor_atributo)

        if datos_reclamos_que_coinciden != []:
             for p_reclamo in datos_reclamos_que_coinciden:
                  reclamos.append(Reclamo(**p_reclamo))
        
        return reclamos
    
    def obtener_ids_usuarios_adheridos_a_reclamo(self, p_reclamo):
        """ Método que obtiene todos los ids de los usuarios adheridos a p_reclamo.

        Argumentos:
         * p_reclamo: Reclamo

        Returns:
         * list(int) or []  
        
        """
        
        ids_usuarios_adheridos = []
         
        datos_usuarios_asocidados = self.__gestor_db.obtener_instancias_asociadas_entre_tablas("Reclamos", "Usuarios", p_reclamo.id)
         
        if datos_usuarios_asocidados != []:
             for p_usuario in datos_usuarios_asocidados:
                  ids_usuarios_adheridos.append(p_usuario["id"])
        
        return ids_usuarios_adheridos
    

    

                      