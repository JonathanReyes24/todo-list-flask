# En este archivo vamos a tener todos los modelos (tablas) que vamos a usar en el proyecto
from . import db    # Importamos db que es el objeto que correrá la base de datos en la aplicación, y lo importaremos para que tenga los modelos (tablas) que necesitaremos en el proyecto

class User(db.Model):   #Es la tabla de Usuarios
    # Vamos agregar las columnas de la tabla
    id = db.Column(db.Integer,primary_key=True)     # La columna id es Integer y es primary key
    username = db.Column(db.String(20), unique=True, nullable=False)   # La columna username es String de 20 caracteres maximo, no se puede repetir valores en esta columna y no puede estar vacio el campo
    password = db.Column(db.Text, nullable=False)   # La columna password es Texto y no puede estar vacio el campo

    def __init__(self,username,password):     # Con el constructor vamos a definir la tabla y su valores
        self.username = username
        self.password = password

    def __repr__(self):        # Forma de imprimir la representación de la tabla, por su username
        return f"<User:{self.username}>"
    
class Todo(db.Model):   #Es la tabla de las Tareas
    # Vamos agregar las columnas de la tabla
    id = db.Column(db.Integer,primary_key=True)     # La columna id es Integer y es primary key
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)   # Creado por va a ser una columna de Enteros, que esta vinculado con el id de la tabla User y no puede estar vacio
    title = db.Column(db.String(100), nullable=False)   # La columna username es String de 100 caracteres maximo y no puede estar vacio el campo
    desc = db.Column(db.Text)
    state = db.Column(db.Boolean, default=False)   # La columna state por default es False, ya que una tarea creada no está terminada

    def __init__(self,created_by,title,desc,state=False):     # Con el constructor vamos a definir la tabla y su valores
        self.created_by = created_by
        self.title = title
        self.desc = desc
        self.state = state

    def __repr__(self):        # Forma de imprimir la representación de la tabla, por su title
        return f"<Todo:{self.title}>"