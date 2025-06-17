import mysql.connector
from mysql.connector import pooling
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Cargar variables de entorno
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

# Acceder a las variables de entorno
settings = Settings()

# Configuración del Pool de Conexiones
db_config = {
    "host": settings.MYSQL_HOST,
    "port": settings.MYSQL_PORT,
    "user": settings.MYSQL_USER,
    "password": settings.MYSQL_PASSWORD,
    "database": settings.MYSQL_DATABASE,
    "autocommit": True
}

try:
    db_connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="container_pool",
        pool_size=5,
        **db_config
    )
    print("Pool de conexiones a MySQL inicializado exitosamente.")
except mysql.connector.Error as err:
    print(f"Error al inicializar el pool de conexiones: {err}")
    print("Asegúrate de que MySQL esté corriendo y las credenciales sean correctas.")
    exit(1) 

def get_db_connection():
    conn = None
    try:
        conn = db_connection_pool.get_connection()
        yield conn
    except mysql.connector.Error as err:
        print(f"Error al obtener conexión del pool: {err}")
        raise
    finally:
        if conn:
            conn.close() 