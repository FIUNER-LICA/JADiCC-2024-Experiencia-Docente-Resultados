from flask import render_template, redirect, request, url_for, flash, abort, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from modules.clasificador import Clasificador
from functools import wraps
from modules.forms import LoginForm, RegisterForm, ReclamoForm, ChangeUserPassword , ChangeUserValues
from modules.config import app, db, login_manager 
from modules.models import Usuario, Reclamo
from modules.inicializador import inicializar

from modules.gestor_de_base_de_datos import GestorDeBaseDeDatos
from modules.gestor_de_usuarios import GestorDeUsuarios , ErrorUsuarioExistenteConMismoAtributoUnico
from modules.gestor_de_reclamos import GestorDeReclamos
from modules.gestor_de_departamentos import GestorDeDepartamentos
from modules.generador_de_analiticos import GeneradorDeAnaliticosDeReclamos
from modules.generador_de_archivos_analiticos import GeneradorDeArchivosAnaliticos
from modules.graficadores_de_datos_de_reclamo import GraficadorDeDiagramaCircularAnimadoDeReclamos, GraficadorDeNubeDePalabrasDeReclamos , GraficadorDeDiagramaDeBarrasDeReclamos
from modules.generadores_de_informes_de_departamento import GeneradorDeInformeHTML , GeneradorDeInformePDF

#-------------------------------------------------------------------
with app.app_context():
    db.create_all()
    gestor_db = GestorDeBaseDeDatos(db)

    gestor_usuarios = GestorDeUsuarios(gestor_db)
    gestor_reclamos = GestorDeReclamos(gestor_db)
    gestor_departamento = GestorDeDepartamentos(gestor_db)

    generador_archivos_analiticos = GeneradorDeArchivosAnaliticos([GraficadorDeDiagramaCircularAnimadoDeReclamos, GraficadorDeNubeDePalabrasDeReclamos, GraficadorDeDiagramaDeBarrasDeReclamos] ,
                                                          [GeneradorDeInformeHTML , GeneradorDeInformePDF])

    inicializar(gestor_usuarios,gestor_departamento )


@login_manager.user_loader  
def user_loader(user_id):
    print(user_id)
    return gestor_usuarios.obtener_usuario_por_atributo_unico("id", user_id)


def is_admin():
    if current_user.is_authenticated and current_user.rol == "administrador":
        return True
    else:
        return False

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != "administrador":
            return abort(403) # la función abort() permite devolver errores HTTP de forma sencilla
                              # 403 significa "Forbidden"
        return f(*args, **kwargs)
    return decorated_function

def final_user_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != "usuario_final":
            return abort(403) # la función abort() permite devolver errores HTTP de forma sencilla
                              # 403 significa "Forbidden"
        return f(*args, **kwargs)
    return decorated_function



@app.route("/")
def home():

    if 'username' in session:
        username = session['username']
    else:
        username = 'Invitado'

    print(current_user)
    return render_template('home.html', user=username, logged_in=current_user.is_authenticated)

# login
@app.route("/login", methods= ["GET", "POST"])
def login():
    login_form = LoginForm()
    # Acceso a la información ingresada en el formulario
    # cuando el usuario realiza el "submit".
    if login_form.validate_on_submit():

        user = gestor_usuarios.obtener_usuario_por_atributo_unico("email", login_form.email.data)

        if not user:
            flash("That email does not exist, please try again")
        elif not check_password_hash(user.password, login_form.password.data):
            flash("Password incorrect, please try again.")
        else:
            login_user(user)
            print(current_user)
            session['username'] = user.nombre_de_usuario
            print(session['username'])

            if is_admin():
                session["departamento_a_cargo"] = gestor_departamento.obtener_departamento_asociado_a_usuario_administrador(current_user.id)
                return redirect(url_for('admin', username=user.nombre_de_usuario)) 
            else:
                return redirect(url_for('bienvenido', username=user.nombre_de_usuario))       
    return render_template('login.html', form=login_form)

# Register
@app.route("/register", methods= ["GET", "POST"])
def register():
    register_form = RegisterForm()
    # Acceso a la información ingresada en el formulario
    # cuando el usuario realiza el "submit".
    if register_form.validate_on_submit():
       
        parametros_usuario = {"p_email" : register_form.email.data,
                  "p_password" : register_form.password.data,
                  "p_nombre_de_usuario" : register_form.username.data,
                  "p_nombre" : register_form.nombre.data,
                  "p_apellido" :  register_form.apellido.data,
                  "p_claustro" :  register_form.claustro.data,
                  "p_rol" : "usuario_final"
                    }
        try:
            gestor_usuarios.crear_nuevo_usuario(**parametros_usuario)

        except ErrorUsuarioExistenteConMismoAtributoUnico as msj_error_que_especifica_tipo_atributo_existente:
            flash(msj_error_que_especifica_tipo_atributo_existente)
            return redirect(url_for('register'))


        return redirect(url_for("login"))
    return render_template('register.html', form=register_form)


@app.route("/bienvenido/<username>")
@login_required
def bienvenido(username):
    if current_user.rol == "administrador":
         return redirect(url_for('admin', username = username))
    else:
        return render_template('bienvenido_usuario_final.html', username=username)
    
@app.route("/ayuda_usuario_final/<username>")
@final_user_only
def ayuda_usuario_final(username):  
    return render_template('ayuda_usuario_final.html', username=username )


@app.route("/crearreclamo/<username>", methods= ["GET", "POST"])
@login_required
@final_user_only
def crearreclamo(username):
    reclamo_form = ReclamoForm()    
    if reclamo_form.validate_on_submit ():

        if reclamo_form.imagen.data:  # Si se ha proporcionado una imagen
            tiempo_actual = datetime.now().strftime("%Y%m%d%H%M%S%f")
            nombre_imagen = str(current_user.id) + str("_") + tiempo_actual 
            filename = secure_filename(f"{nombre_imagen}.{reclamo_form.imagen.data.filename.rsplit('.', 1)[1]}")
            reclamo_form.imagen.data.save(os.path.join(app.config['UPLOAD_FOLDER'],  filename))
  
        else:  # Si no se ha proporcionado ninguna imagen, usa la imagen predeterminada
            filename = "default_image.jpg"

        parametros_reclamo ={
        "p_id_creador" : current_user.id,
        "p_asunto" : reclamo_form.asunto.data,
        "p_nombre_imagen" : filename, 
        "p_contenido" : reclamo_form.contenido.data,
        }
        
        nuevo_reclamo = gestor_reclamos.crear_reclamo(**parametros_reclamo)

        if gestor_reclamos.existe_reclamo_similar_del_mismo_creador(nuevo_reclamo):
            flash("Ya has creado un reclamo similar anteriormente")
            return redirect(url_for('crearreclamo', username = username))

        reclamos_similares = gestor_reclamos.obtener_reclamos_similares_validos_para_adherir_a_creador(nuevo_reclamo)

        if reclamos_similares != []:
            session['nuevo_reclamo'] = nuevo_reclamo
            session['reclamos_similares'] = reclamos_similares
            return redirect(url_for('reclamos_similares', username = username))

        else:
            gestor_reclamos.guardar_reclamo(nuevo_reclamo)
            flash("Se ha creado el reclamo, correctamente")
            return redirect(url_for('misreclamos', username = username))

    return render_template('crear_reclamo.html', reclamo_form=reclamo_form , username=username)


@app.route("/reclamossimilares/<username>", methods= ["GET", "POST"])
@login_required
@final_user_only
def reclamos_similares(username):

    if 'nuevo_reclamo' in session and 'reclamos_similares' in session:
        nuevo_reclamo = session.get('nuevo_reclamo')
        reclamos_similares = session.pop('reclamos_similares', None)

        return render_template('reclamos_similares.html', username=username ,  nuevo_reclamo = nuevo_reclamo,  reclamos_similares = reclamos_similares)
    
    elif request.method == 'POST':
        if 'ContinuarCreando' in request.form:
            nuevo_reclamo = session.pop('nuevo_reclamo', None)
            gestor_reclamos.guardar_reclamo(nuevo_reclamo)
            flash("Se ha creado el reclamo, correctamente")
            return redirect(url_for('misreclamos', username = username))
        
        if 'adherirse' in request.form:
            session.pop('nuevo_reclamo', None)

            reclamo_id = request.form['adherirse']
            gestor_reclamos.adherir_usuario_a_reclamo(current_user.id, reclamo_id)

            flash("Se ha adherido correctamente al reclamo")
            return redirect(url_for('misreclamos', username = username))
        
    else:
         return redirect(url_for('crearreclamo', username = username))

        
@app.route("/misreclamos/<username>", methods= ["GET", "POST"])
@login_required
@final_user_only
def misreclamos(username):

    #Obtengo los reclamos creados por usuario
    reclamos_del_usuario = gestor_reclamos.obtener_reclamos_por_atributo("usuario_id", current_user.id)
    
    #Obtengo los reclamos adheridos por usuario
    reclamos_adheridos = gestor_reclamos.obtener_reclamos_adheridos_por_usuario(current_user.id)
    filtro = ""

    #Obtengo el nombre de los departamentos 
    nombres_departamentos = gestor_departamento.obtener_nombre_de_todos_los_departamento()

    if request.method == 'POST':
        if 'desadherirse' in request.form:
            reclamo_id = request.form['desadherirse']
            gestor_reclamos.desadherir_usuario_a_reclamo(current_user.id , reclamo_id)

            flash("Se ha desadherido del reclamo")
            return redirect(url_for('misreclamos', username = username))
        
        elif 'filtrar_departamento' in request.form:
            nombre_departamento = request.form['filtrar_departamento']
            reclamos_del_usuario = [reclamo for reclamo in reclamos_del_usuario if reclamo.departamento_correspondiente == nombre_departamento]
            #Lista de reclamos adheridos por usuario con el filtro
            reclamos_adheridos = [reclamo for reclamo in reclamos_adheridos if reclamo.departamento_correspondiente == nombre_departamento]

            filtro = "- Departamento: " + nombre_departamento

        elif 'filtrar_estado' in request.form:
            estado = request.form['filtrar_estado']
            reclamos_del_usuario = [reclamo for reclamo in reclamos_del_usuario if reclamo.estado == estado]
            #Lista de los reclamos adheridos por usuario con el filtro
            reclamos_adheridos = [reclamo for reclamo in reclamos_adheridos if reclamo.estado == estado]
            filtro = "- Estado: " + estado
    
    return render_template('mis_reclamos.html', username=username , reclamos_del_usuario = reclamos_del_usuario , reclamos_adheridos = reclamos_adheridos, filtro = filtro , nombres_departamentos = nombres_departamentos)

@app.route("/listarreclamos/<username>" , methods= ["GET", "POST"])
@login_required
@final_user_only
def listarreclamos(username):

    ids_reclamos_adheridos = gestor_reclamos.obtener_ids_reclamos_adheridos_por_usuario(current_user.id)
    nombres_departamentos = gestor_departamento.obtener_nombre_de_todos_los_departamento()

    reclamos = gestor_reclamos.obtener_todos_los_reclamos()
    filtro = "Todos los Reclamos"

    if request.method == 'POST':
        if 'adherirse' in request.form:
            reclamo_id = request.form['adherirse']
            gestor_reclamos.adherir_usuario_a_reclamo(current_user.id, reclamo_id)

            flash("Se ha adherido correctamente al reclamo")
            return redirect(url_for('listarreclamos', username = username))
            
        elif 'desadherirse' in request.form:
            reclamo_id = request.form['desadherirse']
            gestor_reclamos.desadherir_usuario_a_reclamo(current_user.id , reclamo_id)

            flash("Se ha desadherido del reclamo")
            return redirect(url_for('listarreclamos', username = username))
        
        elif 'filtrar_departamento' in request.form:
            nombre_departamento = request.form['filtrar_departamento']
            reclamos = [reclamo for reclamo in reclamos if reclamo.departamento_correspondiente == nombre_departamento]
            filtro = "Reclamos de Departamento: " + nombre_departamento

        elif 'filtrar_estado' in request.form:
            estado = request.form['filtrar_estado']
            reclamos = [reclamo for reclamo in reclamos if reclamo.estado == estado]
            filtro = "Reclamos con Estado: " + estado

    return render_template('listar_reclamos.html', reclamos = reclamos, ids_reclamos_adheridos = ids_reclamos_adheridos,
                             username= username, user = current_user,  nombres_departamentos = nombres_departamentos, filtro = filtro)

@app.route("/miperfil/<username>" , methods= ["GET", "POST"])
@login_required
def miperfil(username):

    editar_form = ChangeUserValues()

    if request.method == 'GET':
        editar_form.nombre.data = current_user.nombre
        editar_form.apellido.data = current_user.apellido
        editar_form.username.data = current_user.nombre_de_usuario
        editar_form.claustro.data = current_user.claustro
        editar_form.email.data = current_user.email

    if editar_form.validate_on_submit():
        parametros_usuario = {
            "nombre": editar_form.nombre.data,
            "apellido": editar_form.apellido.data,
            "claustro": editar_form.claustro.data,
            "email": editar_form.email.data,
            "nombre_de_usuario": editar_form.username.data
        }

        for parametro, valor in parametros_usuario.items():
            if valor != getattr(current_user, parametro):
                try:
                    gestor_usuarios.modificar_atributo_usuario(current_user, parametro, valor)

                except ErrorUsuarioExistenteConMismoAtributoUnico as msj_error_que_especifica_tipo_atributo_existente:
                    flash(msj_error_que_especifica_tipo_atributo_existente)
                    return redirect(url_for('miperfil', username=current_user.nombre_de_usuario))
        
                
        flash("Los datos se han actualizado correctamente")
        return redirect(url_for('miperfil', username=current_user.nombre_de_usuario))
           
    return render_template('mi_perfil.html', username=username , form = editar_form, usuario_rol = current_user.rol)

@app.route("/cambiarcontraseña/<username>" , methods= ["GET", "POST"])
@login_required
def cambiarcontraseña(username):

    editar_form = ChangeUserPassword()

    if request.method == 'GET':
        editar_form.password.render_kw = {"placeholder": "Ingrese Nueva Contraseña"}
        editar_form.confirm.render_kw = {"placeholder": "Repita Nueva Contraseña"}

    if editar_form.validate_on_submit ():
        
        gestor_usuarios.cambiar_password_de_usuario(current_user , p_nuevo_password = editar_form.password.data)
        
        flash("La contraseña se ha actualizado correctamente")
        return redirect(url_for('miperfil', username=username))
    
    return render_template('cambiarcontraseña.html', username=username , form = editar_form, usuario_rol = current_user.rol)


# ADMIN PAGES -----------------------------------------------
@app.route("/admin/<username>")
@admin_only
def admin(username):           
    return render_template('bienvenido_admin.html', username=username, nombre_dep = session.get('departamento_a_cargo').nombre_departamento)

@app.route("/analitica/<username>" , methods= ["GET", "POST"])
@admin_only
def analitica(username):

    departamento_a_cargo = session.get('departamento_a_cargo')
    ruta = "static/Departamentos/"
    generador_analiticos = GeneradorDeAnaliticosDeReclamos(gestor_reclamos.obtener_reclamos_por_atributo("departamento_correspondiente", departamento_a_cargo.nombre_departamento))
    generador_archivos_analiticos.generar_graficos_analiticos(departamento_a_cargo , generador_analiticos , ruta)

    if 'GenerarInforme' in request.form:
            formato = request.form['GenerarInforme']
            generador_archivos_analiticos.generar_archivo_informe_analitico(formato, departamento_a_cargo , generador_analiticos , ruta)
            ruta_archivo = "static/Departamentos/" + departamento_a_cargo.nombre_departamento + "/Informes/reporte_reclamos." + formato.lower()
            return send_file(ruta_archivo, as_attachment=True)

    
    porcentaje_por_estado = generador_analiticos.obtener_porcentaje_de_reclamos_por_estado() 

    return render_template('analitica.html', username=username, nombre_departamento = departamento_a_cargo.nombre_departamento , formatos_informes_disponibles = generador_archivos_analiticos.formatos_de_informe , porcentaje_por_estado = porcentaje_por_estado)

@app.route("/manejarreclamos/<username>" , methods= ["GET", "POST"])
@admin_only
def manejarreclamos(username):

    nombres_departamentos = gestor_departamento.obtener_nombre_de_todos_los_departamento()
    departamento_a_cargo = session.get('departamento_a_cargo')

    reclamos = gestor_reclamos.obtener_reclamos_por_atributo("departamento_correspondiente", departamento_a_cargo.nombre_departamento)
    dict_reclamos_users = {}
    
    for reclamo in reclamos:
        dict_reclamos_users[reclamo.id]={"reclamo":reclamo, "usuario":gestor_usuarios.obtener_usuario_por_atributo_unico("id", reclamo.usuario_id)
                                        ,"usuarios_adheridos": [gestor_usuarios.obtener_usuario_por_atributo_unico("id", u_id) for u_id in 
                                                                gestor_reclamos.obtener_ids_usuarios_adheridos_a_reclamo(reclamo)]}
    filtro = "Todos los Reclamos"

    if request.method == 'POST':
        if 'cambiar_estado' in request.form:
            id_reclamo = request.form['id_reclamo']
            nuevo_estado = request.form.get('nuevo_estado')
            if nuevo_estado != "":
                gestor_reclamos.cambiar_estado_de_reclamo(id_reclamo,nuevo_estado)
                flash("Se ha cambiado el estado del reclamo de manera correcta")
                return redirect(url_for('manejarreclamos', username = username))
            else:
                flash("El estado seleccionado ya corresponde con el estado actual del reclamo")
                return redirect(url_for('manejarreclamos', username = username)) 
            
        elif 'derivar_reclamo' in request.form:
            id_reclamo = request.form['id_reclamo']
            nombre_departamento_a_derivar = request.form['nuevo_departamento']
            gestor_reclamos.cambiar_departamento_correspondiente_de_reclamo(id_reclamo,  nombre_departamento_a_derivar )
            flash("Se ha derivado el reclamo al departamento: "+ nombre_departamento_a_derivar)
            return redirect(url_for('manejarreclamos', username = username))
        
        elif 'filtrar_estado' in request.form:
            estado = request.form['filtrar_estado']
            dict_reclamos_users = {key: value for key, value in dict_reclamos_users.items() if value["reclamo"].estado == estado}
            filtro = "Reclamos " + estado

    return render_template('manejarreclamos.html', reclamos = reclamos,username= username , nombres_departamentos = nombres_departamentos, filtro = filtro, nombre_departamento_a_cargo = departamento_a_cargo.nombre_departamento , dict_reclamos_users=dict_reclamos_users)


@app.route("/ayuda_admin/<username>")
@admin_only
def ayuda_admin(username): 
    departamento_a_cargo = session.get('departamento_a_cargo') 
    return render_template('ayuda_admin.html', username=username, nombre_departamento = departamento_a_cargo.nombre_departamento )

# logout
@app.route("/logout")
def logout():   
    print(current_user)  
    logout_user()      
    print(current_user)
    session['username'] = 'Invitado' 
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


   