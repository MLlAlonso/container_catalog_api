# Container Catalog API

![Python](https://img.shields.io/badge/Python-3.x-blue.svg?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![SASS](https://img.shields.io/badge/Sass-CC6699?style=for-the-badge&logo=sass&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

## Descripción

Esta es una **API RESTful** robusta, desarrollada con **FastAPI** (Python) y **MySQL**, diseñada para gestionar un **catálogo de contenedores marítimos**. Su objetivo principal es proporcionar una interfaz eficiente para realizar operaciones **CRUD** (Crear, Leer, Actualizar, Eliminar) sobre los registros de contenedores.

El proyecto está diseñado siguiendo rigurosamente los principios de **SOLID** y **KISS**, adoptando una estructura modular que emula el patrón **MVC (Modelo-Vista-Controlador)** adaptado para el desarrollo de APIs.

Este desarrollo demuestra habilidades en:
* Diseño y construcción de APIs RESTful.
* Implementación de una interfaz de usuario interactiva para consumir la API.
* Interacción y gestión de bases de datos relacionales.
* Adherencia a buenas prácticas de ingeniería de software para código limpio y mantenible.
* Uso de **inyección de dependencias** y **pools de conexiones** para optimización de recursos.

## Características

* **API RESTful Completa:** Endpoints dedicados para las operaciones fundamentales de Listado, Consulta por ID, Creación, Actualización y Eliminación de contenedores.
* **Interfaz de Usuario Interactiva:** Un frontend simple desarrollado con **HTML, SASS y JavaScript puro** que consume la API, permitiendo la interacción visual con el catálogo.
    * **Barra de Búsqueda:** Funcionalidad de búsqueda en tiempo real para filtrar contenedores por código, tipo, estado, ubicación o propietario.
    * **Modales Personalizados:** Cuadros de diálogo personalizados para confirmaciones de edición/eliminación y visualización de detalles del contenedor, mejorando la experiencia de usuario.
    * **Validaciones:** Implementación de validaciones para una retroalimentación instantánea al usuario.
* **Validación de Datos Sólida:** Integración profunda con **Pydantic** para una validación de esquemas de datos robusta en el backend, garantizando la integridad de las entradas y salidas JSON.
* **Documentación Interactiva Automática:** Generación instantánea de interfaces de documentación como **Swagger UI** (`/docs`) y **ReDoc` (`/redoc`), facilitando la exploración y prueba de la API.
* **Configuración Flexible y Segura:** Gestión de credenciales y parámetros de configuración a través de **variables de entorno (`.env`)** mediante `pydantic-settings`, promoviendo la seguridad y la portabilidad.
* **Persistencia con MySQL:** Utiliza **MySQL 8.x** como base de datos relacional para una gestión de datos fiable y escalable.
* **Pool de Conexiones a Base de Datos:** Implementa un pool de conexiones (`mysql.connector.pooling`) para optimizar el rendimiento y la gestión de recursos de la base de datos.
* **Principios de Diseño Aplicados:** Construido bajo los principios **SOLID** y **KISS** para asegurar un código modular, mantenible, extensible y fácil de entender.
* **Automatización de Base de Datos:** Incluye un script dedicado para la **inicialización y verificación** automática de la base de datos y la tabla necesaria.

---

## Requisitos

Para ejecutar el proyecto localmente, necesitarás:

* **Python 3.x** (versión 3.7 o superior recomendada).
* **MySQL Server 8.x**.
* **`pip`** (el gestor de paquetes estándar de Python).
* **Entorno virtual de Python**.
* **Node.js y npm** (para compilar SASS en el frontend).

---

## Instalación y Ejecución

Sigue estos pasos para poner en marcha la API y la interfaz de usuario en tu entorno local:

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/container_catalog_api.git](https://github.com/tu-usuario/container_catalog_api.git)
    cd container_catalog_api
    ```
    *(Asegúrate de reemplazar `tu-usuario` con tu nombre de usuario de GitHub real).*

2.  **Crear y Activar un Entorno Virtual:**
    ```bash
    python -m venv venv
    # En Windows (Command Prompt/PowerShell):
    .\venv\Scripts\activate
    # En Linux/macOS (o Git Bash en Windows):
    source venv/bin/activate
    ```

3.  **Instalar Dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno para la Base de Datos:**
    * Crea un archivo llamado `.env` en la raíz del proyecto, basándote en el archivo de ejemplo `.env.example`.
    * Reemplazar los valores de las credenciales de MySQL con los tuyos. Estos deben ser credenciales con permisos para crear bases de datos y tablas.
        ```dotenv
        # .env
        MYSQL_HOST=localhost
        MYSQL_PORT=3306
        MYSQL_USER=your_mysql_user
        MYSQL_PASSWORD=your_mysql_password
        MYSQL_DATABASE=container_catalog
        ```

5.  **Inicializar la Base de Datos MySQL:**
    * Este script creará la base de datos `container_catalog` y la tabla `containers`.
    ```bash
    python src/database_initializer.py
    ```

6.  **Compilar SASS para el Frontend:**
    * Asegúrate de tener `sass` instalado globalmente (`npm install -g sass`) o localmente.
    * Ejecuta el comando para compilar tu SASS a CSS:
        ```bash
        sass public/src/styles/index.scss:public/src/styles/index.css
        ```
    * *(Para desarrollo continuo, puedes usar `sass --watch public/src/styles/index.scss:public/src/styles/index.css` en una terminal separada).*

7.  **Ejecutar la Aplicación FastAPI (Servirá la API y el Frontend):**
    ```bash
    uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
    ```
    La aplicación completa (API y frontend) estará operativa y accesible en `http://localhost:8000`.

---

## Endpoints de la API

Una vez que la API esté en ejecución, podrás acceder a su documentación interactiva y probar los endpoints directamente:

* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`

Los endpoints principales disponibles son:

* `GET /api/v1/containers/`: **Listar todos los contenedores**.
* `GET /api/v1/containers/{container_id}`: **Consultar un contenedor específico** por su identificador único.
* `POST /api/v1/containers/`: **Crear un nuevo registro de contenedor**.
* `PUT /api/v1/containers/{container_id}`: **Actualizar los detalles** de un contenedor existente.
* `DELETE /api/v1/containers/{container_id}`: **Eliminar un contenedor** del catálogo.

---

## Estructura del Proyecto

```dotenv
── src/
│   ├── main.py                     # Archivo principal de la aplicación FastAPI y servidor de archivos estáticos.
│   ├── database.py                 # Configuración del pool de conexiones a la base de datos.
│   ├── database_initializer.py     # Script para crear/verificar la base de datos y la tabla.
│   ├── models/                     # Definiciones de esquemas de datos Pydantic para la API.
│   │   ├── init.py
│   │   └── container.py
│   ├── services/                   # Lógica de negocio y capa de abstracción para la interacción con la base de datos.
│   │   ├── init.py
│   │   └── container_service.py
│   └── api/                        # Módulos que contienen los controladores/rutas de la API.
│       ├── v1/                     # Versionado de la API (v1).
│           └── endpoints/          # Definición de los endpoints específicos.
│               └── containers.py
├── public/                         # Directorio para los archivos del frontend.
│   ├── index.html                  # Página principal de la interfaz de usuario.
│   └── src/
│       ├── img/                    # Imágenes para el frontend.
│       ├── js/
│       │   └── main.js             # Lógica JavaScript para la interacción con la API y la UI.
│       └── styles/
│           ├── _variables.scss     # Definición de variables globales de SASS.
│           ├── index.scss          # Estilos principales de SASS.
│           └── index.css           # CSS compilado desde SASS.
├── .env.example                    # Ejemplo de configuración de variables de entorno.
├── .env                            # Archivo con las variables de entorno de tu configuración local.
└── requirements.txt                # Lista de dependencias de Python del proyecto.
```
