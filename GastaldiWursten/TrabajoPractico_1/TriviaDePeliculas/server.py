from flask import render_template, request, redirect, url_for 
from modules.config import app
from modules.funciones import cargar_diccionario_frases_desde_archivo ,obtener_partida_trivia_frases , guardar_puntaje_en_archivo, cargar_resultados_historicos_de_archvio
from flask import session
import datetime


RUTA = "./data/"
ARCHIVO_FRASES = "frases_de_peliculas.txt"
ARCHIVO_RESULTADOS= "resultados_historicos.txt"
diccionario_frases = {}

try:
    diccionario_frases = cargar_diccionario_frases_desde_archivo(RUTA + ARCHIVO_FRASES)            
except FileNotFoundError:
    with open(RUTA + ARCHIVO_FRASES, "w") as archi:
        pass


@app.route("/")
def home():
    
    session['juego_iniciado'] = False
    
    nro_partida_incorrecto = session.get('nro_partida_incorrecto') if session.get('nro_partida_incorrecto') != None else False         

    return render_template('home.html', nro_partida_incorrecto = nro_partida_incorrecto)

@app.route("/trivia", methods=["GET", "POST"])
def trivia():

    if request.method == 'POST':


        if not session.get('juego_iniciado'):

            try:
                session['nro_partidas']  = int(request.form['input_nro_partidas'])
            except:
                session['nro_partida_incorrecto'] = True
                return redirect( url_for('home') )  

            nro_partidas = session.get('nro_partidas')  

            if 3 > nro_partidas or nro_partidas > 10:
                session['nro_partida_incorrecto'] = True 
                return redirect( url_for('home') )
            else:
                session['nro_partida_incorrecto'] = False

                nombre = request.form['input_nombre']
                session['nombre'] = nombre if nombre != "" else "JugadorSinNombre"

                session['juego_iniciado'] = True
                session['fecha_hora_inicio_partida'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
                session['frases_disponibles'] = list(diccionario_frases.keys())
                session['nro_partida_actual'] = 1
                session['aciertos'] = 0

        frases_disponibles = session.get('frases_disponibles')
        
        frase_en_juego, lista_opciones = obtener_partida_trivia_frases(diccionario_frases, frases_disponibles)

        session['frase_en_juego'] = frase_en_juego

    return render_template('trivia.html', frase_en_juego = frase_en_juego , lista_opciones = lista_opciones)

@app.route("/resultados", methods=["GET", "POST"])
def resultados():

    try:
        resultados = cargar_resultados_historicos_de_archvio(RUTA + ARCHIVO_RESULTADOS)            
    except FileNotFoundError:
        with open(RUTA +ARCHIVO_RESULTADOS, "w") as archi:
            pass
    
    lista_resultados = []

    for resultado in resultados:
        linea = resultado.split(' ')
        if linea != ["\n"]:
            lista_resultados.append( [ linea[0],  linea[1] , linea[2] , linea[3] ])

    if lista_resultados == []:
       lista_resultados = [["-", "-","-","-"]]


    return render_template('resultados.html', resultados = lista_resultados)

@app.route("/evaluador", methods=["GET", "POST"])
def evaluador():
    if request.method == 'POST':

        #Se disminuye numero de partida
        session['nro_partida_actual'] = int(session.get('nro_partida_actual')) + 1

        #Se determina si la respuesta es correcta o no
        es_correcta = False
        respuesta_correcta = diccionario_frases[session.get('frase_en_juego')]

        if respuesta_correcta == request.form['respuesta']:
            es_correcta = True
            session['aciertos']  = session.get('aciertos') + 1
        
        nro_partidas_restantes = session.get('nro_partidas') - session.get('nro_partida_actual') + 1
    
    return render_template('evaluador.html', es_correcta = es_correcta , respuesta_correcta = respuesta_correcta , 
                           nro_partidas_restantes = nro_partidas_restantes)


@app.route("/puntuacion", methods=["GET", "POST"])
def puntuacion():

    puntaje = str(session.get('aciertos')) + "/" + str(session.get('nro_partidas'))

    guardar_puntaje_en_archivo( RUTA + ARCHIVO_RESULTADOS , puntaje, session.get('nombre'), session.get('fecha_hora_inicio_partida'))

    #Se remueven las variables de la session
    session.pop('nombre', None)
    session.pop('nro_partida_actual', None)
    session.pop('juego_iniciado', None)
    session.pop('fecha_hora_inicio_partida', None)
    session.pop('frases_disponibles', None)
    session.pop('aciertos', None)



    return render_template('puntuacion.html', puntaje = puntaje)



if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
