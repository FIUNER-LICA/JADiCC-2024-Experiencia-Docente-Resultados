from flask import Flask, request, render_template, session
from modules import control
from modules.config import app

#app = Flask("TRIVIA PELICULAS")
#app.config['DEBUG'] = True


@app.route('/', methods=["GET", "POST"])
def menu():
    session['frases_peliculas'], session['peliculas'] = control.cargar_lista_desde_archivo("./data/frases_de_peliculas.txt") #frases_peliculas, session
    #session['registro'] = [] 
    session['lista_registros'] = control.cargar_registro_desde_archivo("data\\jugadas_historicas") 
    if request.method == 'POST':

        boton = request.form['boton']
        if boton == 'inicio':
            preguntas = int(request.form['frases'])
            usuario = request.form['usuario']
            trivia = control.obtener_trivia(preguntas, session['frases_peliculas'])
            print(f"CANTIDAD DE PREGUNTAS {preguntas}")
            print(f"USUARIO {usuario}")
            return render_template('/trivia.html', trivia = trivia, usuario = usuario, date = control.getTime())

        elif boton == 'lista':
            return render_template('lista.html', peliculas = session['peliculas'])

        elif boton == 'resultados':
            return render_template('registros.html', registro = session['lista_registros'])

    return render_template('index.html')


@app.route('/trivia.html', methods=["GET", "POST"])
def procesar_partida():
    if request.method == 'POST':
        respuesta = request.form['respuesta']
        usuario = request.form['usuario']
        date = request.form['date']
        #session['registro'].append([usuario,respuesta,date])
        control.guardar_registro_en_archivo('jugadas_historicas',usuario,respuesta,date) #crear archivo
        session['lista_registros'] = control.cargar_registro_desde_archivo("data\\jugadas_historicas")  #hay un problema acá, no se están cargando las listas
        #print(f"{usuario} {respuesta} {date}")
        #print(session['lista_registro'])
        return render_template('/resultado.html', puntaje=respuesta, usuario=usuario)
    
    return render_template('trivia.html')

@app.route('/resultado.html', methods=["GET", "POST"])
def resultado():
    if request.method == 'POST':
        return render_template('/index.html')
    return render_template('/resultado.html')

@app.route('/registros.html', methods=["GET", "POST"])
def registro():
    if request.method == 'POST':
        pass
    print(len(session['lista_registros']))
    return render_template('registros.html',registro = session['lista_registros'])

@app.route('/graficas.html', methods=["GET","POST"])
def graficas():
    if request.method == 'POST':
        pass
    aciertos,fallos = control.getEstadisticasGlobales(session['lista_registros'])  #ahora recibe la lista de las partidas jugadas hasta el momento
    fechas,arr_aciertos,arr_fallos = control.getEstadistiicasPorFecha(session['lista_registros'])
    print(fechas)
    print(arr_aciertos)
    print(arr_fallos)
    print(f"{aciertos} {fallos}")
    return render_template('/graficas.html', pastel=[aciertos,fallos],fechas=fechas,arr_aciertos=arr_aciertos,arr_fallos=arr_fallos)



if __name__ == '__main__':
    
    app.run(debug=True)
