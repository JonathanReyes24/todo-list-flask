# __init__.py va a tener la configuración inicial de la aplicación, vamos a configurar:
#   importar flask
#   modo debug
#   SECRET_KEY
#   Configuración de la base de datos

from flask import Flask, render_template, redirect,g,url_for
from flask_sqlalchemy import SQLAlchemy      #Se importa del módulo flask_sqlalchemy el objeto SQLAlchemy para crear la base de datos

db = SQLAlchemy()        # Se crea el objeto que tendrá la base de datos
def create_app():        # Vamos a crear la aplicación usando esta función que retorna app
    app = Flask(__name__)    

    app.config.from_mapping(
        DEBUG = False,         # Con esto determinamos el modo debug True en la configuración inicial del proyecto, para evitar escribir --debug al correr el proyecto
        SECRET_KEY = "devtod",   # Usamos el SECRET_KEY en la configuración inicial del proyecto
        SQLALCHEMY_DATABASE_URI = "sqlite:///todolist.db"       # Se establece el nombre de la base de datos "todolist.db" que tiene el formato de una base de datos de sqlite (es disinto cuando es de una base de datos de posgress o mysql)  
    )
    db.init_app(app)          # Se configura el objeto que tendrá la base de datos para que corra en la aplicación

    from . import todo                 # Se importa el módulo todo.py
    app.register_blueprint(todo.bp)    # Se registra blueprint bp desde el módulo todo.py
    from . import auth                 # Se importa el módulo todo.py
    app.register_blueprint(auth.bp)    # Se registra blueprint bp desde el módulo auth.py

    @app.route("/")           # Aqui en __init__.py podemos tener la ruta y su vista inicial y con Blueprint importamos las vistas de otros módulos
    def index():
        if g.user is not None:
            return redirect(url_for('todo.index'))
        return render_template("index.html")
    
    with app.app_context():   # Si hay modelos que hicieran falta por migrar a la base de datos, con esto se logra
        db.create_all()

    return app

# Al usar url_for() para crear la ruta para una vista que se creó mediante Blueprint, entonces se debe colocar el nombre de 
# blueprint definido en Blueprint("NombreBlueprint",__name__,url_prefix="/prefijo") y después la vista, de la siguiente manera, 
# ejemplo:
#   url_for(nombreBlueprint.nombreVista)
#   {{url_for(nombreBlueprint.nombreVista)}}

# <!-- Al colocarse el {% block bloque%}Contenido{% endblock %} dentro de una parte del HTML de una plantilla que no es "base-html", 
# lo que va a hacer es que el Contenido se colocará en "base.html" y tambien estará dentro de este elemento -->

# Flask-SQLAlchemy, proporciona una integración con SQLAlchemy, el cual permite interactuar con base de datos relacionales, usando
# objetos de Python, en lugar de código SQL.
# Para usar en un proyecto Flask-SQLAlchemy debemos tener el entorno virtual activado y escribir en el CMD:
#   pip install flask-sqlalchemy

# Al correr la aplicación y haber instanciado "db" se va a crear una carpeta "var" con una subcarpeta "todor-instance" que tiene
# la base de datos nombreDeBaseDeDatos.db

# Para que los modelos se importen a la base de datos basta con importarlos colocando este código en alguna página que se vaya a 
# ejecutar:
#   from . import models
# Esta línea solo se ejecuta una vez, para solo importar los modelos, una vez importados debemos eliminarla