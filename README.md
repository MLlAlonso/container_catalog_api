# Container Catalog API

![Python](https://img.shields.io/badge/Python-3.x-blue.svg?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

## Descripción

Esta es una API RESTful desarrollada con **FastAPI** (Python) y **MySQL** que gestiona un catálogo de contenedores. El objetivo principal es proporcionar una interfaz robusta y eficiente para realizar operaciones **CRUD** (Crear, Leer, Actualizar, Eliminar) sobre los registros de contenedores, siguiendo los principios de diseño **SOLID** y **KISS**, y adoptando una estructura modular que emula el patrón **MVC** para APIs.

Este proyecto ha sido desarrollado demostrando habilidades en el desarrollo de APIs, gestión de bases de datos y adherencia a buenas prácticas de ingeniería de software.

## Características

* **API RESTful Completa:** Endpoints para Listar, Consultar por ID, Crear, Actualizar y Eliminar contenedores.
* **Validación de Datos:** Uso de Pydantic para una validación de esquemas robusta y automática.
* **Documentación Interactiva:** Generación automática de Swagger UI y ReDoc para una fácil exploración y prueba de la API.
* **Configuración Flexible:** Uso de variables de entorno (`.env`) para la configuración de la base de datos.
* **MySQL como Base de Datos:** Persistencia de datos en una base de datos relacional robusta.
* **Principios de Diseño:** Implementado con un enfoque en **SOLID** y **KISS** para un código limpio, mantenible y escalable.

## Requisitos

* Python 3.x
* MySQL 8.x
* `pip` (gestor de paquetes de Python)
* Un entorno virtual de Python

## Instalación y Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/container_catalog_api.git](https://github.com/tu-usuario/container_catalog_api.git)
    cd container_catalog_api
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    # En Linux/macOS
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la base de datos:**
    * Crea una base de datos MySQL llamada `container_catalog`.
    * Ejecuta el siguiente script SQL para crear la tabla `containers`:
        ```sql
        USE container_catalog;

        CREATE TABLE IF NOT EXISTS containers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(255) UNIQUE NOT NULL,
            type VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL,
            current_location VARCHAR(255) NOT NULL,
            owner VARCHAR(255) NOT NULL,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        ```

5.  **Configurar variables de entorno:**
    * Crea un archivo `.env` en la raíz del proyecto, basándote en `.env.example`.
    * Asegúrate de reemplazar los valores de las credenciales de MySQL con los tuyos:
        ```dotenv
        # .env
        MYSQL_HOST=localhost
        MYSQL_PORT=3306
        MYSQL_USER=your_mysql_user
        MYSQL_PASSWORD=your_mysql_password
        MYSQL_DATABASE=container_catalog
        ```

6.  **Ejecutar la aplicación:**
    ```bash
    uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
    ```
    La API estará disponible en `http://localhost:8000`.

## Endpoints de la API

Una vez la API esté corriendo, puedes acceder a la documentación interactiva en:
* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`

Los endpoints principales incluyen:

* `GET /api/v1/containers/`: Listar todos los contenedores.
* `GET /api/v1/containers/{container_id}`: Consultar un contenedor por ID.
* `POST /api/v1/containers/`: Crear un nuevo contenedor.
* `PUT /api/v1/containers/{container_id}`: Actualizar un contenedor existente.
* `DELETE /api/v1/containers/{container_id}`: Eliminar un contenedor.

## Estructura del Proyecto
├── src/
│   ├── main.py                     # Aplicación FastAPI principal
│   ├── database.py                 # Configuración de la conexión a la base de datos
│   ├── models/                     # Esquemas Pydantic y modelos de datos
│   │   ├── container.py
│   ├── services/                   # Lógica de negocio y abstracción de la base de datos
│   │   ├── container_service.py
│   └── api/                        # Controladores/Rutas de la API
│       ├── v1/
│           └── endpoints/
│               └── containers.py
├── .env.example                    # Ejemplo de variables de entorno
├── .env                            # Variables de entorno (con tus credenciales)
└── requirements.txt                # Dependencias del proyecto