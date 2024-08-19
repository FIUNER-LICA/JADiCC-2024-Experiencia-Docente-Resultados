from abc import ABC, abstractmethod
from fpdf import FPDF

class GeneradorInformeDepartamento(ABC):

    @abstractmethod
    def generar_informe(self, datos):
        pass



class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Informe', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, text):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln(10)

class GeneradorPDF(GeneradorInformeDepartamento):

    def generar_informe(self, datos):
        pdf = PDF()
        pdf.add_page()
        pdf.chapter_title('Análisis de Datos de Reclamos')
        pdf.chapter_body(f"Cantidad de Reclamos: {datos['cantidad_reclamos']}")
        pdf.chapter_body(f"Mediana de Reclamos Resueltos: {datos['mediana_resueltos']:.2f} días")
        pdf.chapter_body(f"Mediana de Reclamos En Proceso: {datos['mediana_en_proceso']:.2f} días")
        pdf.image('static/estadistica/graficopastel.png', x=10, y=100, w=80)
        pdf.add_page()
        pdf.chapter_title('Nube de Palabras de los Reclamos')
        pdf.image('static/estadistica/nube_palabras.png', x=10, y=30, w=190)
        pdf.output('informe.pdf')


class GeneradorHTML(GeneradorInformeDepartamento):

    def generar_informe(self, datos):
        html = f"""
        <html>
            <head>
                <title>Informe de Reclamos</title>
            </head>
            <body>
                <h1>Análisis de Datos de Reclamos</h1>
                <p>Cantidad de Reclamos: {datos['cantidad_reclamos']}</p>
                <p>Mediana de Reclamos Resueltos: {datos['mediana_resueltos']:.2f} días</p>
                <p>Mediana de Reclamos En Proceso: {datos['mediana_en_proceso']:.2f} días</p>
                <img src="static/estadistica/graficopastel.png" alt="Gráfico Pastel">
                <h1>Nube de Palabras de los Reclamos</h1>
                <img src="static/estadistica/nube_palabras.png" alt="Nube de Palabras">          
            </body>
        </html>
        """
        with open('informe.html', 'w') as file:
            file.write(html)

if __name__== "__main__": 
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    pdf.output('hello_world.pdf')