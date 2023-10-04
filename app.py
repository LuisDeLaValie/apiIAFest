# save this as app.py
from flask import Flask
from utils.initdata import crear_tablas, llenar_tablas, validarTablas

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/pollo")
def hellopolo():
    return "Hello, pollo!"


if __name__ == '__main__':
    
    val =validarTablas();
    if val :
        pass
    else:
        crear_tablas()
        llenar_tablas()

    app.run(debug=True,port=80)