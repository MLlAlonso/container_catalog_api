from fastapi import FastAPI
from src.api.v1.endpoints import containers

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Container Catalog API",
    description="API RESTful para gestionar un catálogo de contenedores, implementada con FastAPI y MySQL.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(containers.router, prefix="/api/v1")

@app.get("/", tags=["Root"], summary="Punto de entrada de la API", description="Mensaje de bienvenida y estado de la API.")
async def read_root():
    """
    Punto de entrada de la API para verificar que está funcionando.
    """
    return {"message": "Bienvenido a la API del Catálogo de Contenedores!"}