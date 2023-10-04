import os
import mysql.connector

class Conexion():

    # Configura los detalles de conexión
    config = {
        'user': os.environ.get("MYSQL_USER"),
        'password': os.environ.get("MYSQL_PASSWORD"),
        'host': os.environ.get("MYSQL_HOST"),
        'database': os.environ.get("MYSQL_DATABASE")
    }

    _conn:any

    def conectar(self):
        # Intenta crear la conexión
        self._conn = mysql.connector.connect(**self.config)
        return self._conn
    
    def desconectar(self):
        self._conn.close()

    def ProbarConexion(self)->bool:
        try:
            # Intenta crear la conexión
            conn = mysql.connector.connect(**self.config)

            if conn.is_connected():
                print("¡Conexión a la base de datos MySQL establecida!")

            # Cierra la conexión
            conn.close()
            return TRUE
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return False
    """
    docstring
    """
    pass




