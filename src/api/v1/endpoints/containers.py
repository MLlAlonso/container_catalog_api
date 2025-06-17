from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import mysql.connector

from src.models.container import ContainerCreate, ContainerUpdate, ContainerResponse
from src.services.container_service import ContainerService
from src.database import get_db_connection

router = APIRouter(
    prefix="/containers",
    tags=["Containers"] 
)

def get_container_service(db: mysql.connector.connection.MySQLConnection = Depends(get_db_connection)) -> ContainerService:
    return ContainerService(db)

@router.get(
    "/",
    response_model=List[ContainerResponse],
    summary="Listar todos los contenedores",
    description="Lista de todos los contenedores disponibles en el catálogo."
)
async def list_containers(
    service: ContainerService = Depends(get_container_service)
):
    return service.get_all_containers()

@router.get(
    "/{container_id}",
    response_model=ContainerResponse,
    summary="Obtener un contenedor por ID",
    description="Detalles de un contenedor específico utilizando su ID."
)
async def get_container(
    container_id: int,
    service: ContainerService = Depends(get_container_service)
):
    container = service.get_container_by_id(container_id)
    if not container:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contenedor con ID '{container_id}' no encontrado"
        )
    return container

@router.post(
    "/",
    response_model=ContainerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo contenedor",
    description="Crea un nuevo registro de contenedor en el catálogo."
)
async def create_container(
    container_data: ContainerCreate,
    service: ContainerService = Depends(get_container_service)
):
    try:
        new_container = service.create_container(container_data)
        return new_container
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, # Conflict para recursos duplicados
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear contenedor: {e}"
        )

@router.put(
    "/{container_id}",
    response_model=ContainerResponse,
    summary="Actualizar contenedor existente",
    description="Actualiza los detalles de un contenedor específico utilizando su ID"
)
async def update_container(
    container_id: int,
    container_data: ContainerUpdate,
    service: ContainerService = Depends(get_container_service)
):

    # Verificamos si el contenedor existe
    existing_container = service.get_container_by_id(container_id)
    if not existing_container:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contenedor con ID '{container_id}' no encontrado"
        )

    try:
        updated_container = service.update_container(container_id, container_data)
        if not updated_container:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contenedor con ID '{container_id}' no encontrado durante la actualización"
            )
        return updated_container
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar contenedor: {e}"
        )

@router.delete(
    "/{container_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un contenedor",
    description="Elimina un contenedor utilizando su ID."
)
async def delete_container(
    container_id: int,
    service: ContainerService = Depends(get_container_service)
):

    deleted = service.delete_container(container_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contenedor con ID '{container_id}' no encontrado"
        )
    return