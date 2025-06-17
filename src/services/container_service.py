# src/services/container_service.py

import mysql.connector
from typing import List, Optional
from src.models.container import ContainerCreate, ContainerUpdate, ContainerResponse

class ContainerService:
    """
    Clase de servicio para manejar las operaciones CRUD de los contenedores.
    Actúa como una capa de abstracción sobre la base de datos.
    """
    def __init__(self, db_connection: mysql.connector.connection.MySQLConnection):
        """
        Inicializa el servicio con una conexión a la base de datos.
        Esta conexión será inyectada por FastAPI.
        """
        self.db_connection = db_connection

    def get_all_containers(self) -> List[ContainerResponse]:
        """
        Obtiene todos los contenedores de la base de datos.
        """
        containers = []
        cursor = self.db_connection.cursor(dictionary=True) # dictionary=True para obtener resultados como diccionarios
        try:
            query = "SELECT id, code, type, status, current_location, owner, last_updated FROM containers"
            cursor.execute(query)
            for row in cursor.fetchall():
                containers.append(ContainerResponse(**row))
        except mysql.connector.Error as err:
            print(f"Error al obtener todos los contenedores: {err}")
            raise # Propaga el error
        finally:
            cursor.close()
        return containers

    def get_container_by_id(self, container_id: int) -> Optional[ContainerResponse]:
        """
        Obtiene un contenedor por su ID.
        """
        cursor = self.db_connection.cursor(dictionary=True)
        try:
            query = "SELECT id, code, type, status, current_location, owner, last_updated FROM containers WHERE id = %s"
            cursor.execute(query, (container_id,))
            row = cursor.fetchone()
            if row:
                return ContainerResponse(**row)
            return None # No se encontró el contenedor
        except mysql.connector.Error as err:
            print(f"Error al obtener contenedor por ID: {err}")
            raise
        finally:
            cursor.close()

    def create_container(self, container: ContainerCreate) -> ContainerResponse:
        """
        Crea un nuevo contenedor en la base de datos.
        """
        cursor = self.db_connection.cursor(dictionary=True) # dictionary=True para poder obtener el lastrowid
        try:
            query = """
            INSERT INTO containers (code, type, status, current_location, owner)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                container.code,
                container.type,
                container.status,
                container.current_location,
                container.owner
            ))
            self.db_connection.commit() # Asegura que los cambios se guarden

            # Obtener el ID del nuevo registro y luego el registro completo para la respuesta
            new_container_id = cursor.lastrowid
            if new_container_id:
                return self.get_container_by_id(new_container_id)
            else:
                # Esto es un fallback, lastrowid debería funcionar con AUTO_INCREMENT
                raise Exception("No se pudo obtener el ID del contenedor recién creado.")

        except mysql.connector.IntegrityError as err:
            # Manejo específico para errores de unicidad (ej. código duplicado)
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                raise ValueError("El código de contenedor ya existe.")
            raise # Re-lanza otros errores de integridad
        except mysql.connector.Error as err:
            print(f"Error al crear contenedor: {err}")
            self.db_connection.rollback() # Revierte la transacción en caso de error
            raise
        finally:
            cursor.close()

    def update_container(self, container_id: int, container_update: ContainerUpdate) -> Optional[ContainerResponse]:
        """
        Actualiza un contenedor existente por su ID.
        Solo actualiza los campos proporcionados en container_update.
        """
        # Filtrar solo los campos que tienen un valor (no None)
        updates = {k: v for k, v in container_update.model_dump(exclude_unset=True).items()}

        if not updates:
            # Si no hay campos para actualizar, simplemente devuelve el contenedor existente
            return self.get_container_by_id(container_id)

        set_clauses = [f"{key} = %s" for key in updates.keys()]
        query = f"UPDATE containers SET {', '.join(set_clauses)} WHERE id = %s"
        values = list(updates.values()) + [container_id]

        cursor = self.db_connection.cursor()
        try:
            cursor.execute(query, tuple(values))
            self.db_connection.commit()

            if cursor.rowcount == 0:
                return None # No se encontró el contenedor para actualizar
            
            return self.get_container_by_id(container_id) # Devuelve el contenedor actualizado
        except mysql.connector.IntegrityError as err:
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                raise ValueError("El código de contenedor actualizado ya existe.")
            raise
        except mysql.connector.Error as err:
            print(f"Error al actualizar contenedor: {err}")
            self.db_connection.rollback()
            raise
        finally:
            cursor.close()

    def delete_container(self, container_id: int) -> bool:
        """
        Elimina un contenedor por su ID.
        Retorna True si se eliminó, False si no se encontró.
        """
        cursor = self.db_connection.cursor()
        try:
            query = "DELETE FROM containers WHERE id = %s"
            cursor.execute(query, (container_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0 # Retorna True si se eliminó al menos 1 fila
        except mysql.connector.Error as err:
            print(f"Error al eliminar contenedor: {err}")
            self.db_connection.rollback()
            raise
        finally:
            cursor.close()