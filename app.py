# save this as app.py
from flask import Flask, request, jsonify
from initdata import crear_procedures, crear_tablas, llenar_tablas, validarTablas
from provedores.conexion import Conexion
import logging

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    logging.warning("prueba de mensaje")
    return "Hello, World! asd"


@app.route('/consulta', methods=['GET'])
def get_consutas():
    conexion = Conexion()
    conn = conexion.conectar()
    cursor = conn.cursor()

    try:
        # Ejecuta el procedimiento almacenado con un valor de entidad_id
        cursor.callproc("Covid.consulta", (0, 'T', 'Todas'))

        resultados = cursor.stored_results()

        # Procesa los resultados (si el procedimiento devuelve algún conjunto de resultados)
        datos = []
        for resultado in resultados:
            for fila in resultado:
                datos.append(fila)
        logging.warning("todo salio ok")


        respuesta = {
            "length":len(datos),
            "resultado": datos
        }

        return jsonify(respuesta)

    except Exception as identifier:
        logging.warning(identifier)
    finally:
        cursor.close()
        conn.close()
    

@app.route('/consulta', methods=['POST'])
def filtro_consultas():
    datos = request.json  # Obtener los datos en formato JSON del cuerpo de la solicitud
    
    edad = int(datos.get('edad'))
    sexo = datos.get('sexo')
    entidad = datos.get('entidad')


    conexion = Conexion()
    conn = conexion.conectar()
    cursor = conn.cursor()

    try:
        logging.warning(f"edad:{edad} sexo:{sexo} entidad:{entidad}")

        # Ejecuta el procedimiento almacenado con un valor de entidad_id
        cursor.callproc("Covid.consulta", (edad, sexo, entidad))

        resultados = cursor.stored_results()

        # Procesa los resultados (si el procedimiento devuelve algún conjunto de resultados)
        datos = []
        for resultado in resultados:
            for fila in resultado:
                datos.append(fila)
        logging.warning("todo salio ok")


        respuesta = {
            "length":len(datos),
            "resultado": datos
        }

        return jsonify(respuesta)

    except Exception as identifier:
        logging.warning(identifier)
    finally:
        cursor.close()
        conn.close()
    

@app.route('/consulta/crear', methods=['POST'])
def crear_consuta():
    datos = request.json  # Obtener los datos en formato JSON del cuerpo de la solicitud
    
    id_registro = datos.get('id_registro')
    id_entidad = int(datos.get('id_entidad'))  
    sexo = datos.get('sexo')
    edad = int(datos.get('edad')) 
    tipo_paciente = int(datos.get('tipo_paciente')) 
    intubado = int(datos.get('intubado'))
    otro_caso = int(datos.get('otro_caso'))
    id_resultado = int(datos.get('id_resultado'))


    conexion = Conexion()
    conn = conexion.conectar()
    cursor = conn.cursor()

    try:

        # Ejecuta el procedimiento almacenado con un valor de entidad_id
        cursor.callproc("Covid.InsertarPaciente", (id_registro, id_entidad, sexo, edad, tipo_paciente, intubado, otro_caso, id_resultado))
        conn.commit()

        respuesta = {
            "resultado": "Creado"
        }

        return jsonify(respuesta)

    except Exception as identifier:
        logging.warning(identifier)
        respuesta = {
            "msg": f"{identifier}"
        }

        return jsonify(respuesta)
    finally:
        cursor.close()
        conn.close()
    


@app.before_request
def inicializar_aplicacion():
    try:        
        logging.info(">>> Creadond la Base de datos <<<")

        val =validarTablas();
        if val :
            pass
        else:
            crear_tablas()
            llenar_tablas()
            crear_procedures()

        logging.info(">>> Se termino termino de crear la Base de Datos <<<")

    except Exception as identifier:
        logging.warning(f"Error al migrar los datod {identifier}")
    

if __name__ == '__main__':    
    app.run(debug=True)
