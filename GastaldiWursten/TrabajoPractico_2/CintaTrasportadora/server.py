from flask import render_template, request, redirect, url_for
from modules.config import app

from modules.cajon import Cajon
from modules.cinta_transportadora import CintaTransportadora
from modules.alimento import Alimento
from modules.fruta import Fruta
from modules.verdura import Verdura
from modules.kiwi import Kiwi
from modules.manzana import Manzana
from modules.papa import Papa
from modules.zanahoria import Zanahoria


cinta_transportadora = CintaTransportadora()

clases_de_alimento = [Fruta,Kiwi,Manzana,Verdura,Papa,Zanahoria,Alimento]

@app.route("/", methods=["GET", "POST"])
def home():

    promedios_aw ={}

    inspeccionar_cajon = False

    if request.method == 'POST':

        nro_alimentos = int (request.form['input_nro_alimentos'])

        cajon = Cajon()

        cinta_transportadora.cargar_alimentos(cajon, nro_alimentos)

        for clase in clases_de_alimento:
            promedios_aw[clase.__name__] = cajon.calcular_aw_prom_tipo(clase) 

        if max(promedios_aw.values()) > 0.95:
            inspeccionar_cajon = True
                

    return render_template('home.html', promedios_aw = promedios_aw, inspeccionar_cajon = inspeccionar_cajon)

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')