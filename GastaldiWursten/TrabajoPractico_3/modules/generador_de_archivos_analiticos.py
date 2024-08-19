from modules.generador_de_analiticos import GeneradorDeAnaliticosDeReclamos
from modules.graficadores_de_datos_de_reclamo import GraficadorDeDatosDeReclamo
from modules.generadores_de_informes_de_departamento import GeneradorDeInformeDeDepartamento
from modules.models import Departamento
from pathlib import Path

class GeneradorDeArchivosAnaliticos():
    """ Clase que modela un generador de archivos analiticos.
    ------------------------------------------------
    Atributos:
    * tipos_graficadores_de_datos_de_reclamos: list(GraficadorDeDatosDeReclamo)
    * tipos_generadores_de_informes_de_reclamos_de_departamento: list(GeneradorDeInformeDeDepartamento)
    * formatos_de_informe: list(String)

    """

    def __init__(self, p_list_tipos_graficadores_de_datos_de_reclamos = [],p_lista_tipos_generadores_de_informes_de_reclamos_de_departamento =[] ) -> None:
        
        
        # Compruebo los tipos de graficadores
        for tipo_graficador in p_list_tipos_graficadores_de_datos_de_reclamos:
            if not issubclass(tipo_graficador, GraficadorDeDatosDeReclamo):
                raise ValueError(f"{tipo_graficador.__name__} no es un tipo compatible.")
        
        # Compruebo los tipos de generadores de informes
        for tipo_informe in p_lista_tipos_generadores_de_informes_de_reclamos_de_departamento:
            if not issubclass(tipo_informe, GeneradorDeInformeDeDepartamento):
                raise ValueError(f"{tipo_informe.__name__} no es un tipo compatible.")
            

        self.__tipos_graficadores_de_datos_de_reclamos = p_list_tipos_graficadores_de_datos_de_reclamos
            
        self.__tipos_generadores_de_informes_de_reclamos_de_departamento = p_lista_tipos_generadores_de_informes_de_reclamos_de_departamento

        self.__formatos_de_informe = [tipo.get_formato() for tipo in  self.__tipos_generadores_de_informes_de_reclamos_de_departamento]

    @property
    def formatos_de_informe(self):
        return self.__formatos_de_informe


    def añadir_nuevo_tipo_de_graficador_de_datos_de_reclamos(self, p_graficador_de_datos_de_reclamos):
        """ Método que añade un nuevo tipo de graficador de datos de reclamos a la lista.

        Argumentos:
        * p_graficador_de_datos_de_reclamos: GraficadorDeDatosDeReclamo

        """

        #Compruebo tipo
        if not issubclass(p_graficador_de_datos_de_reclamos, GraficadorDeDatosDeReclamo):
                raise ValueError(f"{p_graficador_de_datos_de_reclamos.__name__} no es un tipo compatible.")
        
        self.__tipos_graficadores_de_datos_de_reclamos.append(p_graficador_de_datos_de_reclamos)

    def añadir_nuevo_tipo_de_generador_de_informe_de_reclamos_de_departamento(self, p_generador_de_informe_de_reclamos_de_departamento):
        """ Método que añade un nuevo tipo de generador de informe de departamento a la lista.
        
        Argumentos:
        * p_generador_de_informe_de_reclamos_de_departamento: GeneradorDeInformeDeDepartamento

        """
        if not issubclass(p_generador_de_informe_de_reclamos_de_departamento, GeneradorDeInformeDeDepartamento):
                raise ValueError(f"{p_generador_de_informe_de_reclamos_de_departamento.__name__} no es un tipo compatible.")
        
        self.__tipos_generadores_de_informes_de_reclamos_de_departamento.append(p_generador_de_informe_de_reclamos_de_departamento)
        self.formatos_de_informe.append(p_generador_de_informe_de_reclamos_de_departamento.get_formato())

    def generar_graficos_analiticos(self, p_departamento, p_generador_de_analiticos_de_reclamos, p_ruta):
        """ Método que crea una instancia de cada tipo de graficador de la lista, hace que se grafiquen y se guarden
        en una carpeta con el nombre del departamento en la ruta indicada.
        
        Argumentos:
        * p_departamento: Departamento
        * p_generador_de_analiticos_de_reclamos: GeneradorDeAnaliticosDeReclamos
        * p_ruta: String

        """

        if  not isinstance(p_departamento, Departamento):
             raise ValueError("Error: p_departamento no es de tipo Departamento")
        
        if not isinstance(p_generador_de_analiticos_de_reclamos, GeneradorDeAnaliticosDeReclamos):
             raise ValueError("Error: p_generador_de_analiticos_de_reclamos no es de tipo GeneradorDeAnaliticosDeReclamos")

        ruta = p_ruta + p_departamento.nombre_departamento + "/Graficos/" 
        path = Path(ruta)
        path.mkdir(parents=True, exist_ok=True)

        for tipo_graficador in self.__tipos_graficadores_de_datos_de_reclamos:
            graficador = tipo_graficador(p_generador_de_analiticos_de_reclamos, ruta)
            graficador.graficar_y_guardar()


    def generar_archivo_informe_analitico(self, p_formato, p_departamento, p_generador_de_analiticos_de_reclamos, p_ruta):
        """ Método que crea una instancia del tipo de generador de archivo de informe indicado en el formato y llama a su metodo
        para generar el informe en una carpeta con el nombre del departamento en la ruta indicada.
        
        Argumentos:
        * p_departamento: Departamento
        * p_generador_de_analiticos_de_reclamos: GeneradorDeAnaliticosDeReclamos
        * p_ruta: String

        """
        if p_formato not in self.formatos_de_informe:
            raise ValueError ("El formato no es admitido")
        
        clase_del_formato = next((clase for clase in self.__tipos_generadores_de_informes_de_reclamos_de_departamento if clase.get_formato() == p_formato), None)
        ruta = p_ruta + p_departamento.nombre_departamento + "/Informes/" 
        path = Path(ruta)
        path.mkdir(parents=True, exist_ok=True)

        generador_informe_formato_indicado = clase_del_formato(p_generador_de_analiticos_de_reclamos, ruta, p_departamento.nombre_departamento)
        generador_informe_formato_indicado.generar_informe()