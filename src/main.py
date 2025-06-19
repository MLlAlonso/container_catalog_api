from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.v1.endpoints import containers

import os 

app = FastAPI(
    title="Container Catalog API",
    description="API RESTful para gestionar un catálogo de contenedores, implementada con FastAPI y MySQL.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- Configuración CORS ---
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000,http://localhost:8000,http://localhost:8080").split(',')

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

origins.extend(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin).strip() for origin in origins], # Asegúrate de limpiar espacios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="public"), name="static")

from fastapi.responses import FileResponse

@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse("public/index.html")

app.include_router(containers.router, prefix="/api/v1")