from flask import Blueprint, render_template,request,redirect,url_for,g   #Blueprint permite almacenar las rutas y vistas en diferentes archivos y no tenerlo todo concentrado en un solo archivo

bp = Blueprint("todo",__name__,url_prefix="/todo")   # Todas las rutas de "todo" van a tener el prefijo "todo/"

from .auth import login_required
from .models import Todo, User
from . import db

@bp.route("/list")
@login_required
def index():
    todos = Todo.query.all()
    return render_template("todo/index.html",todos=todos)

@bp.route("/create",methods=("GET","POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]

        todo = Todo(g.user.id,title,desc)

        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("todo.index"))
    return render_template("todo/create.html")

def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo

@bp.route("/update/<int:id>",methods=("GET","POST"))
@login_required
def update(id):
    todo = get_todo(id)           # Obtenemos la tarea que vamos a editar, gracias a su id, donde se modificará su title, desc y state

    if request.method == "POST":
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        todo.state = True if request.form.get("state")=="on" else False    # Devuelve True si el checkbox esta "checked" sino devuelve False

        db.session.commit()
        return redirect(url_for("todo.index"))
    return render_template("todo/update.html",todo=todo)

@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    todo = get_todo(id)     # Obtenemos la tarea que vamos a eliminar mediante su selección desde el HTML
    db.session.delete(todo) # Se elimina
    db.session.commit()     # Se lleva a cabo el comando anterior
    return redirect(url_for("todo.index"))     # Una vez eliminado volvemos a la página principal de tareas