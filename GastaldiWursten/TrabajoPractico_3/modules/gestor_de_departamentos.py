from modules.gestor_de_base_de_datos import GestorDeBaseDeDatos
from modules.models import Departamento


class GestorDeDepartamentos():
    """ Clase que modela un gestor de departamentos que interactua con un gestor de base de datos para obtener 
    y crear departamentos.
    ------------------------------------------------
    Atributos:
    * gestor_db: GestorDeBaseDeDatos

    """

    def __init__(self, p_gestor_base_de_datos) -> None:
        self.__gestor_db = p_gestor_base_de_datos

    def crear_nuevo_departamento(self, p_nombre, p_id_usuario_jefe):
        """ Método que crea una nueva instancia de un departamento y guarda sus datos en la base de datos.

        Argumentos:
        * p_nombre: String
        * p_id_usuario_jefe: int
        
        Returns:
        * Departamento       
        """ 

        if self.__gestor_db.obtener_primer_coincidencia_en_tabla("Departamentos", "nombre_departamento", p_nombre) != None:
            raise ValueError("Ya existe departamento con el mismo nombre")

        self.__gestor_db.guardar_fila_en_tabla("Departamentos", {"nombre_departamento" : p_nombre , "usuario_jefe_id":p_id_usuario_jefe} )

        p_departamento = self.__gestor_db.obtener_primer_coincidencia_en_tabla("Departamentos", "nombre_departamento", p_nombre)

        return Departamento(**p_departamento)
    
    def obtener_departamento_asociado_a_usuario_administrador(self, p_id_usuario_admin):
        """ Método que devuelve una instancia de un departamento a partir del id del usuario administrador
        asignado en la creación como usuarios_jefe_id .

        Argumentos:
        * p_id_usuario_admin: int
        
        Returns:
        * Departamento or None       
        """ 
        departamento = None
        p_departamento = self.__gestor_db.obtener_primer_coincidencia_en_tabla(  "Departamentos" , "usuario_jefe_id", p_id_usuario_admin) 
        if p_departamento != None:
            departamento = Departamento(**p_departamento)
        
        return departamento
    
    def obtener_departamento_por_nombre(self, p_nombre):
        """ Método que devuelve una instancia de un departamento a partir de su nombre.

        Argumentos:
        * p_nombre: String
        
        Returns:
        * Departamento or None       
        """ 
        departamento = None
        p_departamento = self.__gestor_db.obtener_primer_coincidencia_en_tabla("Departamentos", "nombre_departamento", p_nombre)
        
        if p_departamento != None:
            departamento = Departamento(**p_departamento)
            
        return departamento


    def obtener_nombre_de_todos_los_departamento(self):
        """ Método que devuelve todos los nombres de los departamentos existentes en la base de datos.

        Returns:
        * list(String) or []       
        """ 
        return self.__gestor_db.obtener_valores_presentes_en_columna_de_tabla("Departamentos", "nombre_departamento")
