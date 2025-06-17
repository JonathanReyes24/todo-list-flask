# Blueprint permite almacenar las rutas y vistas en diferentes archivos y no tenerlo todo concentrado en un solo archivo
# redirect redirecciona a otra página (recordemos que url_for solo fabricar rutas que se colocan en href, etc)
# flash es una función que envia mensajes a las plantillas
# session con ello guardaremos la sessión de un usuario
# g sirve para grabar un valor para usarlo en cualquier parte de la aplicación (archivos .py o plantillas)
from flask import Blueprint,render_template,request,url_for,redirect,flash,session,g   
from werkzeug.security import generate_password_hash, check_password_hash    # generate_password_hass nos permite hashear la contraseña y check_password_hash permite verficar la contraseña previamente hasheada

from .models import User   # Importamos el objeto para manipular la tabla de usuarios
from todor import db       # Importamos el objeto de la base de datos

bp = Blueprint("auth",__name__,url_prefix="/auth")

@bp.route("/register", methods=("GET","POST"))
def register():
    if request.method =="POST":
        username = request.form["username"]     # Obtenemos el username del campo del formulario con name="username"
        password = request.form["password"]     # Obtenemos el username del campo del formulario con name="password"
        user = User(username,generate_password_hash(password))   # Colocamos en el Objeto User el nuevo usuario con su contraseña (no se agrega aun a la base de datos), además la contraseña queda encriptada
        
        error = None
        
        user_name = User.query.filter_by(username=username).first()  # Se filtra el usuario para ver si ya existe
        if user_name == None:    # Si resultado que no existe dicho usuario entonces lo agregamos a la base de datos
            db.session.add(user)   # Se agrega el usuario a la base de datos
            db.session.commit()    # Se compromete a realizar la instrucción de arriba
            return redirect(url_for("auth.login"))
        else:
            error = f"El usuario {username} ya está registrado"
        flash(error)  # Con flash mandamos la variable error a la plantilla que se renderiza, flash almacena una lista de mensajes, por lo que se usa for para ver los mensajes
    return render_template("auth/register.html")

@bp.route("/login", methods=("GET","POST"))
def login():
    if g.user is not None:
        return redirect(url_for('todo.index'))
    if request.method =="POST":
        username = request.form["username"]     # Obtenemos el username del campo del formulario con name="username"
        password = request.form["password"]     # Obtenemos el username del campo del formulario con name="password"
        
        error = None
        
        user = User.query.filter_by(username=username).first()  # Se filtra el usuario para ver si ya existe
        if user==None:
            error = "Nombre de usuario incorrecto"
        elif not check_password_hash(user.password,password):    # Va a comparar si el password hasheado "user.password" es igual la "password" que se pasa a través del formulario
            error = "Usuario o Contraseña incorrecta"

        if error == None:    # Si no hay error, debido a que el usuario y contraseña son correctos entonces iniciaremos una session
            session.clear() # Si ya habia una session iniciada la vamos a borrar
            session["user_id"] = user.id    # Iniciamos session con una llave "user_id" que guarda el nombre de usuario que está en la session actual
            return redirect(url_for("todo.index"))    # Al iniciar session redirigimos al usuario a la página principal
        flash(error)  # Con flash mandamos la variable error a la plantilla que se renderiza, flash almacena una lista de mensajes, por lo que se usa for para ver los mensajes
    return render_template("auth/login.html")

@bp.route("/logout")
def logout():     # Al salir cerramos session y redirigimos a la pagina de inicial (fuera del sistema)
    session.clear()           
    return redirect(url_for("index"))

@bp.before_app_request    # Con este decorador hacemos que la función se ejecute en cada petición al servidor
def load_loggued_in_user():            # Esta funcion ayuda a mantener la session iniciada, y se ejecuta cada vez que se realiza una petición al servidor
    user_id = session.get("user_id")   # Obtenemos el id del usuario que ha iniciado session
    if user_id is None:    # Si no ha iniciado session entonces guardamos en el objeto global "g" un atrubuto "user" con valor None
        g.user = None      # El objeto g es global y se encuentra en todo los archivos .py e incluyendo las plantillas, ya que desde las plantillas usando el objeto "g" validaremos la session
    else:          # Si si hay una session iniciada entonces guardamos en el objeto global "g" un atrubuto "user" con valor de dicho usuario y en el caso de no existir devolverá erro 404
        g.user = User.query.get_or_404(user_id)       # El objeto g es global y se encuentra en todo los archivos .py e incluyendo las plantillas, ya que desde las plantillas usando el objeto "g" validaremos la session

import functools     # Este bloque lo que hace es que al ingresar a cada vista de "todo" es decir del sistema, antes va a comprobar mediante g.user que haya iniciado sesión, de ser asi, permitirá el acceso, de no ser así entonces no lo permitirá
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

# Al usar flash(variable), lo que hace es almacenar ese mensaje en una lista, para acceder a dichos mensajes desde las plantillas
# se accede con:
#    {% for message in get_flashed_messages() %}
#       message
#    {% endfor %}