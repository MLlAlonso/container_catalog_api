import os
from dotenv import load_dotenv
import mysql.connector

# Cargar variables de entorno del archivo .env
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

def initialize_database():
    """
    Se conecta a la base de datos MySQL y crea la tabla 'containers' si no existe.
    """
    print(f"Intentando conectar a MySQL en {DB_CONFIG['host']}:{DB_CONFIG['port']}...")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print(f"Conectado exitosamente a la base de datos '{DB_CONFIG['database']}'.")

        # Crea la tabla containers si no existe
        create_table_query = """
        CREATE TABLE IF NOT EXISTS containers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(255) UNIQUE NOT NULL,
            type VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL,
            current_location VARCHAR(255) NOT NULL,
            owner VARCHAR(255) NOT NULL,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Tabla 'containers' verificada/creada exitosamente.")

    except mysql.connector.Error as err:
        print(f"Error al inicializar la base de datos: {err}")
        print("Asegúrate de que la base de datos 'container_catalog' exista.")
        print("Verifica que el usuario tenga permisos para crear tablas.")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    print("Iniciando script...")
    initialize_database()
    print("Script finalizado.")