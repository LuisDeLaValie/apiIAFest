import pandas as pd
import logging


from provedores.conexion import Conexion

def crear_tablas():
    entidad_res="""
        CREATE TABLE Entidades_Residencia (
            ID_ENTIDAD INT PRIMARY KEY auto_increment,
            NOMBRE_ENTIDAD VARCHAR(255)
        );"""
    tipo_pasiente="""
        CREATE TABLE Tipo_Paciente (
            ID_TIPO_PACIENTE INT PRIMARY KEY auto_increment,
            TIPO VARCHAR(255)
        );"""
    resultados="""
        CREATE TABLE Resultados (
            ID_RESULTADO INT PRIMARY KEY auto_increment,
            RESULTADO VARCHAR(255)
        );"""
    pasiente="""
        CREATE TABLE Pacientes (
            ID_REGISTRO VARCHAR(255),
            ID_ENTIDAD INT,
            SEXO  CHAR(1),
            EDAD INT,
            ID_TIPO_PACIENTE INT,
            INTUBADO BOOLEAN,
            OTRO_CASO BOOLEAN,
            ID_RESULTADO INT,
            FOREIGN KEY (ID_ENTIDAD) REFERENCES Entidades_Residencia(ID_ENTIDAD),
            FOREIGN KEY (ID_TIPO_PACIENTE) REFERENCES Tipo_Paciente(ID_TIPO_PACIENTE),
            FOREIGN KEY (ID_RESULTADO) REFERENCES Resultados(ID_RESULTADO)
        );"""
    

    conexion =Conexion()
    conn = conexion.conectar()
    cursor = conn.cursor()

    try:

        cursor.execute(entidad_res)
        cursor.execute(tipo_pasiente)
        cursor.execute(resultados)
        cursor.execute(pasiente)

        # Asegúrate de confirmar los cambios en la base de datos
        conn.commit()


    except Exception as err:
        print(f"Error al crear las tablas datos: {err}")



    # Cierra el cursor y la conexión
    cursor.close()
    conn.close()

def crear_procedures():
    consuta_procedure="""
        CREATE PROCEDURE Covid.consulta(
            in edad_parametro int,
            in sexo_parametro char(1),
            in entidad_parametro varchar(255)
        )
        BEGIN
            SELECT 
                p.ID_REGISTRO, 
                er.NOMBRE_ENTIDAD, 
                p.SEXO, 
                p.EDAD, 
                tp.TIPO, 
                p.INTUBADO, 
                p.OTRO_CASO, 
                r.RESULTADO  
            from Pacientes p 
            inner join Entidades_Residencia er on er.ID_ENTIDAD = p.ID_ENTIDAD 
            inner JOIN Tipo_Paciente tp on tp.ID_TIPO_PACIENTE  = p.ID_TIPO_PACIENTE 
            inner join Resultados  r on r.ID_RESULTADO = p.ID_REGISTRO
            WHERE 
                (
                    (edad_parametro = -1 AND p.EDAD < 12)
                    or (edad_parametro = -2 AND p.EDAD BETWEEN 12 AND 18)
                    or (edad_parametro = -3 AND p.EDAD BETWEEN 19 AND 25)
                    or (edad_parametro = -4 AND p.EDAD > 60)
                    or (edad_parametro = 0 AND  p.EDAD> 0)
                )
                AND (sexo_parametro = 'T' or p.SEXO=sexo_parametro)
                AND (entidad_parametro = 'Todas' or entidad_parametro = er.NOMBRE_ENTIDAD); 
        END
        """    


    
    conexion =Conexion()
    conn = conexion.conectar()
    cursor = conn.cursor()

    try:

        cursor.execute(consuta_procedure)
        # Asegúrate de confirmar los cambios en la base de datos
        conn.commit()


    except Exception as err:
        print(f"Error al crear las tablas datos: {err}")



    # Cierra el cursor y la conexión
    cursor.close()
    conn.close()

def llenar_tablas():
    conexion =Conexion()
    conn = conexion.conectar()
    cursor = conn.cursor()

    try:
        # Especifica la ruta al archivo Excel
        archivo_excel = './50000_Set_de_datos.xlsx'

        # Lee solo las columnas especificadas del archivo Excel
        columnas_deseadas = [
        "FECHA_ACTUALIZACION", 
        "ID_REGISTRO", 
        "ORIGEN", 
        "SEXO", 
        "ENTIDAD_RES", 
        "TIPO_PACIENTE", 
        "FECHA_SINTOMAS", 
        "INTUBADO", 
        "EDAD", 
        "OTRO_CASO", 
        "RESULTADO"]
        data_frame = pd.read_excel(archivo_excel, usecols=columnas_deseadas)


        inserts_entidades="""    
            INSERT INTO Covid.Entidades_Residencia (NOMBRE_ENTIDAD)
            VALUES ('Aguascalientes'),
            ('Baja California'),
            ('Baja California Sur'),
            ('Campeche'),
            ('Chiapas'),
            ('Chihuahua'),
            ('Ciudad de México'),
            ('Coahuila'),
            ('Colima'),
            ('Durango'),
            ('Estado de México'),
            ('Guanajuato'),
            ('Guerrero'),
            ('Hidalgo'),
            ('Jalisco'),
            ('Michoacán'),
            ('Morelos'),
            ('Nayarit'),
            ('Nuevo León'),
            ('Oaxaca'),
            ('Puebla'),
            ('Querétaro'),
            ('Quintana Roo'),
            ('San Luis Potosí'),
            ('Sinaloa'),
            ('Sonora'),
            ('Tabasco'),
            ('Tamaulipas'),
            ('Tlaxcala'),
            ('Veracruz'),
            ('Yucatán'),
            ('Zacatecas');
                """

            # Muestra los primeros 5 registros del DataFrame
        cursor.execute(inserts_entidades)

        insert_resultados="""
            INSERT INTO Covid.Resultados (RESULTADO)
            VALUES
            ('INDRE'),
            ('LESP'),
            ('LAVE');
            """
        cursor.execute(insert_resultados)

        insert_tipo_pasiente="""
            INSERT INTO Covid.Tipo_Paciente (TIPO)
            VALUES ('hospitalizado'), ('ambulatorio');
            """
        cursor.execute(insert_tipo_pasiente)

        
        insert_paciente="""
            INSERT INTO Covid.Pacientes
            (ID_REGISTRO, ID_ENTIDAD, SEXO, EDAD, ID_TIPO_PACIENTE, INTUBADO, OTRO_CASO, ID_RESULTADO)
            VALUES
            """
        
        for item in data_frame.values:
            sex=''
            if item[3]:
                sex='M'
            else:
                sex='F'
            
            id = str(item[1])
            if len(id)>255:
                id=id[0:254]

            insert_paciente+=f"\n('{id}', {item[4]}, '{sex}', {item[8]}, {item[5]}, {item[7]}, {item[9]}, {item[10]}),"

        insert_paciente = insert_paciente[:-1] + ";"
        cursor.execute(insert_paciente)
        conn.commit()

    except Exception as e:
        # Manejo de excepciones
        print(f"error al traer los archivos de exel: {str(e)}")

    # Cierra el cursor y la conexión
    cursor.close()
    conn.close()
    
def validarTablas()->bool:
    # Crea un cursor para ejecutar consultas SQL
    conexion =Conexion()
    conn = conexion.conectar()
    cursor = conn.cursor()
    
    try:
        # Nombre de la tabla que deseas verificar
        nombre_tabla = 'Pacientes'

        # Consulta SQL para verificar si la tabla existe
        consulta = f"SHOW TABLES LIKE '{nombre_tabla}'"

        # Ejecuta la consulta
        cursor.execute(consulta)

        # Obtiene el resultado de la consulta
        resultado = cursor.fetchone()

        # Verifica si la tabla existe
        return resultado
    except Exception as identifier:
        print(f"Error al validar las tablas: {identifier}")

    # Cierra el cursor y la conexión
    cursor.close()
    conn.close()
    

""" if __name__ == '__main__':
    # Configura la configuración de registro
    logging.basicConfig(filename='app.log', level=logging.WARNING)

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
 """




