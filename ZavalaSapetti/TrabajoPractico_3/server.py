from datetime import datetime
import logging
import os
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, abort, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user #pip install flask-login
                                                                              #pip install email-validator
from functools import wraps
from modules.forms import LoginForm, RegisterForm, ReclamoForm
from modules.config import app, login_manager # 4) importamos login_manager de modules.config
from modules.generador_estadistica import GeneradorDeEstadisticas
from modules.models import TablaUsuarios, TablaReclamos
from modules.entidades import Usuario, Reclamo
from modules.repositorio_concreto import RepositorioSQL
from modules.gestor_de_reclamos import GestorDeReclamos
from modules.gestor_de_usuarios import GestorUsuarios
from modules.clasificador_de_reclamos import ClasificadordeReclamos
from modules.gestor_de_reclamos import GestorDeReclamos
from modules.gestor_de_usuarios import GestorUsuarios
from modules.graficador import GraficadorNubeDePalabras, GraficadorPastelYBarras
from modules.monticulo_mediana import MonticuloMediana
from modules.generador_informe import GeneradorHTML, GeneradorPDF

departamentos_jefes = {
    1: 'Soporte Informático',
    2: 'Maestranza',
    3: 'Secretaría Técnica'
}

with app.app_context():
    repositorio = RepositorioSQL()
    gestor_reclamos  = GestorDeReclamos(repositorio)
    gestor_usuarios = GestorUsuarios(repositorio)
    clasificador_reclamos = ClasificadordeReclamos()

logging.basicConfig(level=logging.DEBUG)
# 4) Flask-login también requiere definir una función "user_loader",
# dado un ID de usuario, devuelve el objeto usuario asociado.
# Esta función se llama de forma automática por Flask-login cada vez
# que el usuario se loguea.
@login_manager.user_loader  
def user_loader(user_id):
    print(f"Acción del usuario: {user_id}")
    return gestor_usuarios.obtener_usuario_por_atributo_unico("id", user_id)

# 9)usuarios admin
def is_admin():
    if current_user.is_authenticated and current_user.id in departamentos_jefes:
        return True
    else:
        return False

# https://flask.palletsprojects.com/en/2.3.x/patterns/viewdecorators/
# decorador para restringir el acceso a una vista a usuarios administradores
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id not in departamentos_jefes:
            return abort(403)  # 403 significa "Forbidden"
        return f(*args, **kwargs)
    return decorated_function

def final_user_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != "usuario_final":
            #return abort(403) # la función abort() permite devolver errores HTTP de forma sencilla
                              # 403 significa "Forbidden"
            flash("No está autorizado para acceder a esta página.")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home():
    if 'username' in session:
        username = session['username']
    else:
        username = 'Invitado'
    
    #print(f"Usuario actual: {current_user}")

    if is_admin():
        return redirect(url_for('bienvenido_admin', username=current_user.username))
    elif current_user.is_authenticated:
        return redirect(url_for('bienvenido_usuariofinal', username=current_user.username))

    return render_template('home.html', user=username)

# 6)login
@app.route("/login", methods= ["GET", "POST"])
def login():
    login_form = LoginForm()
    # Acceso a la información ingresada en el formulario
    # cuando el usuario realiza el "submit".
    if login_form.validate_on_submit():
        #hacemos una consulta filtrando por email para
        #saber si hay un usuario registrado con ese email
        user = TablaUsuarios.query.filter_by(email=login_form.email.data).first()
        if not user:
            flash("El email no existe. Inténtalo de nuevo, por favor.")
        elif not check_password_hash(user.password, login_form.password.data):
            flash("Contraseña incorrecta. Inténtalo de nuevo, por favor.")
        else:
            login_user(user)
            session['username'] = user.username
            print(f"Ingresa el usuario: {current_user}")
            print(f"nombre de usuario: {session['username']}")

            if user.id in departamentos_jefes:
                session["departamento_a_cargo"] = departamentos_jefes[user.id] #guardamos en la sesión del usuario el departamento a cargo del usuario actual
                return redirect(url_for('bienvenido_admin'))
            else:
                return redirect(url_for('bienvenido_usuariofinal', username=user.username))        
    return render_template('login.html', form=login_form)


# 5) Register
@app.route("/register", methods= ["GET", "POST"])
def register():
    register_form = RegisterForm()
    # Acceso a la información ingresada en el formulario
    # cuando el usuario realiza el "submit".
    # validate_on_submit verificará si es una solicitud POST y si es válida
    # la información ingresada en el formulario
    if register_form.validate_on_submit():
        # Verifico que no exista usuario con igual email
        if TablaUsuarios.query.filter_by(email=register_form.email.data).first():
            flash("Ya te has registrado con ese email, inicia sesión en su lugar.")
            return redirect(url_for('login'))
        # Si el registro es correcto, se crea un nuevo usuario en la db
        encripted_pass = generate_password_hash(
            password= register_form.password.data,
            method= 'pbkdf2:sha256',
            salt_length=8
        )
     
        nuevo_usuario = Usuario({
            'nombre': register_form.nombre.data,
            'apellido': register_form.apellido.data,
            'nombre_de_usuario': register_form.username.data,
            'email': register_form.email.data,
            'password': encripted_pass,
            'rol': 'usuario_final'
        })
        
        repositorio.guardar_usuario(nuevo_usuario)
        flash("Usuario creado. Por favor, inicia sesión.")
        return redirect(url_for("login"))
        
    return render_template('register.html', reg_form=register_form)

# 8) Bienvenidos. Decoramos la vista con login_required para asegurar de que el usuario actual está conectado
# y autenticado antes de llamar a la función
@app.route("/bienvenido_admin", methods= ["GET", "POST"])
@login_required
@admin_only
def bienvenido_admin():
    if "departamento_a_cargo" not in session:
        flash("Acceso denegado.")
        return redirect(url_for('login'))
    
    departamento = session["departamento_a_cargo"]
    
    if request.method == "POST":
        id_reclamo = request.form['id_reclamo']
        
        # Manejo de cambio de estado
        if 'nuevo_estado' in request.form:
            nuevo_estado = request.form['nuevo_estado']
            tiempo_resolucion = request.form.get('tiempo_resolucion')
            if tiempo_resolucion:
                tiempo_resolucion = int(tiempo_resolucion)
            gestor_reclamos.cambiar_estado_de_reclamo(int(id_reclamo), nuevo_estado, tiempo_resolucion)
        
        # Manejo de derivación
        elif 'departamento' in request.form:
            nuevo_departamento = request.form['departamento']
            repositorio.actualizar_atributo_en_instancia_en_tabla(TablaReclamos, int(id_reclamo), "departamento_correspondiente", nuevo_departamento)
        
        return redirect(url_for('bienvenido_admin'))

    reclamos = gestor_reclamos.obtener_reclamos_por_atributo("departamento_correspondiente", departamento)
    
    return render_template('bienvenido_admin.html', nombre_dep=departamento, reclamos=reclamos)


@app.route("/bienvenido_usuariofinal/<username>")
@login_required 
def bienvenido_usuariofinal(username):           
    return render_template('bienvenido_usuariofinal.html', user=username)

@app.route("/crearreclamo/<username>",methods= ["GET", "POST"])
@login_required
@final_user_only
def crearreclamo(username):
    reclamo_form = ReclamoForm()    
    if reclamo_form.validate_on_submit ():
        if reclamo_form.imagen.data:  # Si se ha proporcionado una imagen
            tiempo_actual = datetime.now().strftime("%Y%m%d%H%M%S%f")
            nombre_imagen = f"{current_user.id}_{tiempo_actual}"
            filename = secure_filename(f"{nombre_imagen}.{reclamo_form.imagen.data.filename.rsplit('.', 1)[1]}")
            reclamo_form.imagen.data.save(os.path.join(app.config['UPLOAD_FOLDER'],  filename))
        else:  # Si no se ha proporcionado ninguna imagen, usa la imagen predeterminada
            filename = "default_image.jpg"

     # Crear una entidad Reclamo pero sin guardarla aún en la base de datos
        nuevo_reclamo = Reclamo({
            "usuario_id": current_user.id,
            "asunto": reclamo_form.asunto.data,
            "contenido": reclamo_form.contenido.data,
            "imagen": filename,
            "departamento": clasificador_reclamos.clasificar_reclamo(reclamo_form.asunto.data),
            "fecha": datetime.now().replace(microsecond=0),
            "estado": "Pendiente",
            "tiempo_de_resolucion": None,
            "usuarios_adheridos": []
        })

        # Verificar si hay reclamos similares antes de guardar el nuevo reclamo
        reclamos_similares = gestor_reclamos.obtener_reclamos_similares_validos_para_adherir_a_creador(nuevo_reclamo)
        if reclamos_similares:
            session['nuevo_reclamo'] = nuevo_reclamo
            session['reclamos_similares'] = reclamos_similares
            return redirect(url_for('reclamos_similares', username=username)) 

        # Si no hay reclamos similares, guardar el nuevo reclamo
        repositorio.guardar_reclamo(nuevo_reclamo)
        flash("Se ha creado el reclamo correctamente")
        return redirect(url_for('mis_reclamos', username=username)) 

    return render_template('crearreclamo.html', reclamo_form=reclamo_form , username=username)

@app.route("/reclamossimilares/<username>", methods= ["GET", "POST"])
@login_required
@final_user_only
def reclamos_similares(username):

    if 'nuevo_reclamo' in session and 'reclamos_similares' in session:
        nuevo_reclamo = session.get('nuevo_reclamo')
        reclamos_similares = session.pop('reclamos_similares', None)

        return render_template('reclamos_similares.html', username=username ,  nuevo_reclamo = nuevo_reclamo,  reclamos_similares = reclamos_similares)
    
    if request.method == 'POST':
        if 'ContinuarCreando' in request.form:
            nuevo_reclamo = session.pop('nuevo_reclamo', None)
            try:
                repositorio.guardar_reclamo(nuevo_reclamo)
                flash("Se ha creado el reclamo, correctamente")
                return redirect(url_for('mis_reclamos', username = username))
            
            except Exception as e:
                print(e)
        
        elif 'adherirse' in request.form:
            session.pop('nuevo_reclamo', None)

            reclamo_id = request.form['adherirse']
            try:
                gestor_reclamos.adherir_usuario_a_reclamo(current_user.id, reclamo_id)
            except Exception as e:
                print(e)

            flash("Se ha adherido correctamente al reclamo")
            return redirect(url_for('mis_reclamos', username = username))
        
    else:
        try:
            return redirect(url_for('crearreclamo', username = username))
        except Exception as e:
            print(e)

@app.route("/listar_reclamos/<username>", methods=["GET", "POST"])
@login_required
@final_user_only
def listar_reclamos(username):
    filtro_departamento = None
    filtro_estado = None
    if request.method == "POST":
        filtro_departamento = request.form.get('filtrar_departamento')
        filtro_estado = request.form.get('filtrar_estado')

        if request.method == "POST":
            if 'adherirse' in request.form:
                reclamo_id = request.form['adherirse']
                try:
                    gestor_reclamos.adherir_usuario_a_reclamo(current_user.id, reclamo_id)
                    flash("Se ha adherido correctamente al reclamo")
                except Exception as e:
                    print(e)
                    flash("Hubo un error al intentar adherirse al reclamo")
            
            elif 'desadherirse' in request.form:
                reclamo_id = request.form['desadherirse']
                try:
                    gestor_reclamos.desadherir_usuario_de_reclamo(current_user.id, reclamo_id)
                    flash("Se ha desadherido correctamente del reclamo")
                except Exception as e:
                    print(e)
                    flash("Hubo un error al intentar desadherirse del reclamo")
    
    reclamos = gestor_reclamos.obtener_todos_los_reclamos()
    ids_reclamos_adheridos = gestor_reclamos.obtener_ids_reclamos_adheridos_por_usuario(current_user.id)

    # Filtrar por departamento
    if filtro_departamento:
        reclamos = [r for r in reclamos if r.departamento_correspondiente == filtro_departamento]

    # Filtrar por estado
    if filtro_estado:
        reclamos = [r for r in reclamos if r.estado == filtro_estado]

    nombres_departamentos = ['Soporte Informático', 'Maestranza', 'Secretaría Técnica']
    return render_template('listar_reclamos.html', 
                           reclamos=reclamos, 
                           username=username, 
                           ids_reclamos_adheridos=ids_reclamos_adheridos, 
                           filtro_departamento=filtro_departamento, 
                           filtro_estado=filtro_estado, 
                           nombres_departamentos=nombres_departamentos)


@app.route("/misreclamos/<username>")
@login_required
@final_user_only
def mis_reclamos(username):
    usuario_id = current_user.id
     # Obtener los reclamos creados por el usuario actual
    mis_reclamos = gestor_reclamos.obtener_reclamos_por_atributo("usuario_id", usuario_id)
    # Obtener los reclamos a los que el usuario está adherido
    reclamos_adheridos = gestor_reclamos.obtener_reclamos_adheridos_por_usuario(usuario_id)
    return render_template('mis_reclamos.html', reclamos=mis_reclamos, reclamos_adheridos=reclamos_adheridos, username=username)

@app.route("/ayuda_admin/<username>")
@login_required
@admin_only
def ayuda_admin(username):
    return render_template('ayuda_admin.html', username=username)


@app.route("/estadisticas", endpoint='estadisticas')
@login_required
@admin_only
def mostrar_graficas_y_mediana():
    usuario_id = current_user.id
    departamento = departamentos_jefes[usuario_id]
    generador_estadistica= GeneradorDeEstadisticas()
    
    #Aqui se genera el grafico pastel
    lista_para_grafico = generador_estadistica.porcentajes_de_estado_reclamos(departamento)
    #logging.debug(f"Lista para gráfico: {lista_para_grafico}")
    GraficadorPastelYBarras("graficopastel", "pastel", lista_para_grafico)

    #Calculos de las medianas
    lista_mediana_resueltos = generador_estadistica.tiempo_resolucion_por_estado(departamento, 'Resuelto')
    logging.debug(f"Lista mediana resueltos: {lista_mediana_resueltos}")
    mediana_resueltos = MonticuloMediana(lista_mediana_resueltos).get_mediana()
    
    lista_mediana_en_proceso = generador_estadistica.tiempo_resolucion_por_estado(departamento, 'En Proceso')
    #print("holaaaa:",lista_mediana_en_proceso)
    #print(lista_mediana_resueltos)
    logging.debug(f"Lista mediana en proceso: {lista_mediana_en_proceso}") 
    mediana_en_proceso = MonticuloMediana(lista_mediana_en_proceso).get_mediana()
    mediana_en_proceso_formateada = f"{mediana_en_proceso:.2f}"

    #Aqui se genera la nube de palabras 
    palabras_frecuentes = generador_estadistica.obtener_palabras_mas_frecuentes(departamento)
    GraficadorNubeDePalabras("nube_palabras", palabras_frecuentes)

    return render_template('estadisticas.html', Mediana_r = mediana_resueltos, Mediana_ep = mediana_en_proceso_formateada)

@app.route("/generar_informe", methods=['POST'])
@login_required
@admin_only
def generar_informe():
    usuario_id = current_user.id
    departamento = departamentos_jefes[usuario_id]
    generador_estadistica = GeneradorDeEstadisticas()
    lista_reclamos_del_depa = gestor_reclamos.obtener_reclamos_por_atributo("departamento_correspondiente", departamento)
    lista_para_grafico = generador_estadistica.porcentajes_de_estado_reclamos(departamento)

    lista_mediana_resueltos = generador_estadistica.tiempo_resolucion_por_estado(departamento, 'Resuelto')
    mediana_resueltos = MonticuloMediana(lista_mediana_resueltos).get_mediana()

    lista_mediana_en_proceso = generador_estadistica.tiempo_resolucion_por_estado(departamento, 'En Proceso')
    mediana_en_proceso = MonticuloMediana(lista_mediana_en_proceso).get_mediana()
    
    # Generar nube de palabras
    palabras_frecuentes = generador_estadistica.obtener_palabras_mas_frecuentes(departamento)
    GraficadorNubeDePalabras("nube_palabras", palabras_frecuentes)

    # Datos para el informe
    datos = {
        'cantidad_reclamos': len(lista_reclamos_del_depa),
        'mediana_resueltos': mediana_resueltos,
        'mediana_en_proceso': mediana_en_proceso
    }

    # Generar la gráfica para el informe
    graficador = GraficadorPastelYBarras("graficopastel", "pastel", lista_para_grafico)

    formato = request.form.get('formato')
    if formato == 'PDF':
        generador = GeneradorPDF()
        #generador.generar_informe(datos)
    elif formato == 'HTML':
        generador = GeneradorHTML()
    else:
        abort(400, description="Formato de informe no soportado")

    generador.generar_informe(datos)

    return redirect(url_for('estadisticas'))
   

# 7)logout
@app.route("/logout")
def logout():   
    print(f"Usuario antes de salir: {current_user}")  
    logout_user()      
    print(f"Usuario después de salir: {current_user}")
    session['username'] = 'Invitado' 
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    #    mis_reclamos = repositorio.obtener_reclamos_por_usuario(current_user.id)
