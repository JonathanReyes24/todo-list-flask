# Desde este archivo, vamos a correr la aplicación que se configuró en __init__.py
from todor import create_app     # Al indicar "todor" estamos refiriendonos al archivo __init__.py, es decir vamos a importar la función create_app() del archivo principal (__init__.py) que esta dentro de la carpeta "todor" para correr la aplicación desde aquí

if __name__ == '__main__':
    app = create_app()      # Donde app tiene la aplicación configurada desde __init__.py de la carpeta "todor"
    app.run()               # Se corre la aplicación

# Con todo esto, al tener la configuración importada junto a la aplicación en este archivo, en vez de escribir en el CMD:
#   flask --app todor --debug run
# Simplemente ubicándonos en la carpeta del proyecto podemos escribir en el CMD:
#   py run.py