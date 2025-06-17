from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints import containers

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Container Catalog API",
    description="API RESTful para gestionar un catálogo de contenedores, implementada con FastAPI y MySQL.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- Configuración CORS ---
# Orígenes permitidos (para desarrollo y luego para producción)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(containers.router, prefix="/api/v1")

@app.get("/", tags=["Root"], summary="Punto de entrada de la API", description="Mensaje de bienvenida y estado de la API.")
async def read_root():
    return {"message": "Bienvenido a la API del Catálogo de Contenedores!"}