from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Base para los esquemas de contenedor
class ContainerBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=255, description="Identificador único del contenedor")
    type: str = Field(..., min_length=1, max_length=255, description="Tipo de contenedor (ej: 20ft, 40ft, etc)")
    status: str = Field(..., min_length=1, max_length=255, description="Estado actual del contenedor (ej: Disponible, En tránsito, En almacen)")
    current_location: str = Field(..., min_length=1, max_length=255, description="Ubicación actual del contenedor")
    owner: str = Field(..., min_length=1, max_length=255, description="Nombre del propietario del contenedor")

    class Config:
        from_attributes = True

class ContainerCreate(ContainerBase):
    pass

class ContainerUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=255, description="Código único del contenedor")
    type: Optional[str] = Field(None, min_length=1, max_length=255, description="Tipo de contenedor (ej: 20ft, 40ft, Refrigerado)")
    status: Optional[str] = Field(None, min_length=1, max_length=255, description="Estado actual del contenedor")
    current_location: Optional[str] = Field(None, min_length=1, max_length=255, description="Ubicación actual del contenedor")
    owner: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre del propietario del contenedor")

    class Config:
        from_attributes = True

class ContainerResponse(ContainerBase):
    id: int = Field(..., description="Identificador único del contenedor")
    last_updated: datetime = Field(..., description="Fecha y hora de la última actualización")

    class Config:
        from_attributes = True