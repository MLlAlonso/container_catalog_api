from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

app.mount("/static", StaticFiles(directory="public"), name="static")
app.include_router(containers.router, prefix="/api/v1")

from fastapi.responses import FileResponse

@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse("public/index.html")