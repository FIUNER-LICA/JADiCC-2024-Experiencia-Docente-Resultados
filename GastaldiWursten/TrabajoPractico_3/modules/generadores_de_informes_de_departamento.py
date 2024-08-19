from abc import ABC, abstractmethod 
from jinja2 import Template
from modules.graficadores_de_datos_de_reclamo import GraficadorDeDiagramaCircularDeReclamos , GraficadorDeDiagramaDeBarrasDeReclamos
import base64
from pathlib import Path
import shutil
from datetime import datetime
from xhtml2pdf import pisa


class GeneradorDeInformeDeDepartamento(ABC):
    """ Clase que modela un generador de informes de dapartamento.
    ------------------------------------------------
    Atributos:
    * generador_de_analiticos_de_reclamos: GeneradorDeAnaliticosDeReclamos
    * ruta: String
    * nombre_de_departamento: String

    """
    def __init__(self, p_generador_de_analiticos_de_reclamos , p_ruta , p_nombre_de_departamento ) -> None:

        self.__generador_de_analiticos_de_reclamos = p_generador_de_analiticos_de_reclamos
        self.__ruta = p_ruta
        self.__nombre_de_departamento = p_nombre_de_departamento


    @property
    def generador_de_analiticos_de_reclamos(self):
        return self.__generador_de_analiticos_de_reclamos
    
    @property
    def ruta(self):
        return self.__ruta
    
    @property
    def nombre_de_departamento(self):
        return self.__nombre_de_departamento
    
    
    @abstractmethod   
    def generar_informe(self):
        """ Metodo que genera un archivo de informe de departamento y lo guarda en self.ruta """
        pass

    @abstractmethod   
    def get_formato():
        """ Metodo para obtener el nombre del formato"""
        pass



class GeneradorDeInformeHTML(GeneradorDeInformeDeDepartamento):
    """ Clase que modela un generador de informes de dapartamento en formato html.
    ------------------------------------------------
    Atributos:
    * generador_de_analiticos_de_reclamos: GeneradorDeAnaliticosDeReclamos
    * ruta: String
    * nombre_de_departamento: String

    """

    def __init__(self, p_generador_de_analiticos_de_reclamos, p_ruta, p_nombre_de_departamento) -> None:
        super().__init__(p_generador_de_analiticos_de_reclamos, p_ruta, p_nombre_de_departamento)
 
    def generar_informe(self):
        """ Metodo que genera un archivo de informe html de departamento y lo guarda en self.ruta """

        #Creo una carpeta temporal
        path = Path(self.ruta + "temp")
        path.mkdir(parents=True, exist_ok=True)

        #Realizo las imagenes
        graficador_circular = GraficadorDeDiagramaCircularDeReclamos(self.generador_de_analiticos_de_reclamos , self.ruta + "temp/")
        graficador_circular.graficar_y_guardar()

        graficador_histograma = GraficadorDeDiagramaDeBarrasDeReclamos(self.generador_de_analiticos_de_reclamos, self.ruta + "temp/")
        graficador_histograma.graficar_y_guardar()

        #Armo el html
        with open( self.ruta + "temp/" + "grafica_circular.png", "rb") as image_file:
            imagen_1 = base64.b64encode(image_file.read()).decode('utf-8')

        with open( self.ruta + "temp/" + "diagrama_de_barras.png", "rb") as image_file:
            imagen_2 = base64.b64encode(image_file.read()).decode('utf-8')

        template = Template('''<html>
        <head>
            <title>Reporte de Reclamos</title>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                .img-container {
                    text-align: center;
                }
                .img-container img {
                    width: 70%;
                    height: auto;
                }
            </style>
        </head>
        <body>
            <table style="width:100%">
                <tr bgcolor="#E3E0E0">
                    <td colspan="2" style="text-align:center"><h1>Reporte de Reclamos: {{nombre_departamento}}</h1></td>
                </tr>
                <tr bgcolor="#F5F3F3">
                    <td colspan="2" ><p><b>Descripción:</b> Este reporte se ha generado a partir de los reclamos realizados por los usuarios y que han sido catalogados bajo la dirección del departamento "{{nombre_departamento}}" para su tratamiento correspondiente.</p></td>
                </tr>
                <tr bgcolor="#F5F3F3">
                    <td colspan="2" ><b>Fecha y Hora de Creación del Reporte:</b> {{ fecha_creacion }}</td>
                </tr>
                <tr bgcolor="#E3E0E0">
                    <td colspan="2">
                        <table>
                            <h3 style="text-align: center;">Cantidad Por Estado Del Reclamo</h3> 
                        </table>
                    </td>
                </tr>
                <tr bgcolor="#F1F1F1">
                    <td colspan="2">
                        <table >
                            <tr bgcolor="#E6E6E6">
                                <th>Total de Reclamos</th>
                                <th>Reclamos En Proceso</th>
                                <th>Reclamos Pendientes</th>
                                <th>Reclamos Inválidos</th>
                                <th>Reclamos Resueltos</th>
                            </tr>
                            <tr bgcolor="#F5F3F3">
                                <td>{{ cantidad_total }}</td>
                                <td>{{ cantidad_en_proceso }}</td>
                                <td>{{ cantidad_pendientes }}</td>
                                <td>{{ cantidad_invalido }}</td>
                                <td>{{ cantidad_resueltos}}</td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr bgcolor="#E3E0E0">
                    <td colspan="2">
                        <table>
                            <h3 style="text-align: center;">Porcentajes</h3> 
                        </table>
                    </td>
                </tr>
                 <tr bgcolor="#F1F1F1">
                    <td colspan="2">
                        <table>
                            <tr  bgcolor="#E6E6E6">
                                <th>% Total de Reclamos</th>
                                <th>% Reclamos En Proceso</th>
                                <th>% Reclamos Pendientes</th>
                                <th>% Reclamos Inválidos</th>
                                <th>% Reclamos Resueltos</th>
                            </tr>
                            <tr bgcolor="#F5F3F3">
                                <td>{{ porcentaje_total }}</td>
                                <td>{{ porcentaje_en_proceso }}</td>
                                <td>{{ porcentaje_pendientes }}</td>
                                <td>{{ porcentaje_invalido }}</td>
                                <td>{{ porcentaje_resueltos }}</td>
                            </tr>
                        </table>
                    </td>
                </tr>
                 <tr bgcolor="#E3E0E0">
                    <td colspan="2">
                        <table>
                            <h3 style="text-align: center;">Palabras con más apariciones en los reclamos</h3> 
                        </table>
                    </td>
                </tr>
                <tr bgcolor="#F1F1F1">
                    <td colspan="2">
                        <table>
                            <tr bgcolor="#F5F3F3">
                                <th>Palabra</th>
                                <th>Cantidad de Apariciones</th>
                            </tr>
                            {% for palabra, frecuencia in palabras_mas_frecuentes.items() %}
                            <tr bgcolor="#F7F6F6">
                                <th>{{palabra}}</th>
                                <th>{{frecuencia}}</th>
                            </tr>
                            {% endfor %}
                        </table>
                    </td>
                </tr>
                
                <tr bgcolor="#E3E0E0">
                    <td colspan="2">
                        <table>
                            <h3 style="text-align: center;">Gráficas Analíticas</h3> 
                        </table>
                    </td>
                </tr>
                            
                            

                 <tr bgcolor="#F5F3F3">
                    <td class="img-container" style="padding: 15px; width: 50%;">
                        
                        <img src="data:image/png;base64,{{ imagen_1 }}" alt="Imagen del reclamo">
                    </td>
                    <td class="img-container" style="padding: 15px; width: 50%;">
                        
                        <img src="data:image/png;base64,{{ imagen_2 }}" alt="Imagen del reclamo">
                    </td>
                </tr>
            </table>
        </body>
        </html>
    ''')

        # Aquí se pueden calcular los valores necesarios para rellenar la plantilla
        # y pasarlos como variables al renderizar la plantilla.

        # Obtener las 15 palabras más frecuentes
        palabras_mas_frecuentes_frecuencias = self.generador_de_analiticos_de_reclamos.obtener_palabras_mas_frecuentes()
        
        cantidad_por_estado = self.generador_de_analiticos_de_reclamos.obtener_cantidad_de_reclamos_por_estado()
        porcentaje_por_estado = self.generador_de_analiticos_de_reclamos.obtener_porcentaje_de_reclamos_por_estado()
        #Guardo el archivo html
        with open(self.ruta + 'reporte_reclamos.html', 'w') as f:
            f.write(template.render(
                fecha_creacion= datetime.now().replace(microsecond=0),  # Agregar la fecha actual aquí
                cantidad_total= sum(cantidad_por_estado.values()),  
                cantidad_en_proceso= cantidad_por_estado["En Proceso"], 
                cantidad_pendientes= cantidad_por_estado["Pendiente"],  
                cantidad_invalido= cantidad_por_estado["Inválido"],  
                cantidad_resueltos= cantidad_por_estado["Resuelto"], 
                porcentaje_total= 100,  
                porcentaje_en_proceso= porcentaje_por_estado["En Proceso"],  
                porcentaje_pendientes= porcentaje_por_estado["Pendiente"],  
                porcentaje_invalido= porcentaje_por_estado["Inválido"],  
                porcentaje_resueltos= porcentaje_por_estado["Resuelto"],   
                imagen_1 = imagen_1,
                imagen_2 = imagen_2,
                nombre_departamento = self.nombre_de_departamento,
                palabras_mas_frecuentes = palabras_mas_frecuentes_frecuencias
            ))

        #Borro la carpeta temporal y su contenido
        shutil.rmtree(path, ignore_errors=True)

    def get_formato():
        """ Metodo que retorna el nombre del formato"""
        return "HTML"



class GeneradorDeInformePDF(GeneradorDeInformeDeDepartamento):
    """ Clase que modela un generador de informes de dapartamento en formato pdf.
    ------------------------------------------------
    Atributos:
    * generador_de_analiticos_de_reclamos: GeneradorDeAnaliticosDeReclamos
    * ruta: String
    * nombre_de_departamento: String

    """

    def __init__(self, p_generador_de_analiticos_de_reclamos, p_ruta, p_nombre_de_departamento) -> None:
        super().__init__(p_generador_de_analiticos_de_reclamos, p_ruta, p_nombre_de_departamento)
 
    def generar_informe(self):
        """ Metodo que genera un archivo de informe pdf de departamento y lo guarda en self.ruta """

        path = Path(self.ruta + "temp")
        path.mkdir(parents=True, exist_ok=True)

        generador_informe_html = GeneradorDeInformeHTML(self.generador_de_analiticos_de_reclamos, self.ruta + "temp/", self.nombre_de_departamento)
        generador_informe_html.generar_informe()
        
        # Abre y lee el archivo HTML
        with open(self.ruta + "temp/reporte_reclamos.html", 'r') as f:
            contenido_html = f.read()

        # Convierte HTML a PDF
        
        with open(self.ruta + "reporte_reclamos.pdf", 'w+b') as archivo_pdf:
            pisa.CreatePDF(
            contenido_html,
            dest=archivo_pdf,
            page_size='A4',
            margin=0.25,
            scale='1'
            )
        #Borro la carpeta temporal y su contenido
        shutil.rmtree(path, ignore_errors=True)
    
    def get_formato():
        """Metodo que retorna el nombre del formato"""
        return "PDF"



