# ReservaFlow API

Backend de **ReservaFlow**, una plataforma de gestión de citas y reservaciones diseñada para negocios como barberías, salones de belleza, estudios de uñas y otros establecimientos que trabajan mediante citas.

El objetivo del proyecto es desarrollar una API REST que permita administrar múltiples negocios, sus servicios, clientes y reservaciones.

## Tecnologías utilizadas

- **Python:** lenguaje de programación del backend.
- **FastAPI:** framework para desarrollar la API REST.
- **Uvicorn:** servidor ASGI para ejecutar la aplicación.
- **MongoDB Atlas:** base de datos NoSQL en la nube.
- **PyMongo:** biblioteca para conectar Python con MongoDB.
- **python-dotenv:** gestión de variables de entorno.
- **Swagger UI:** documentación interactiva de los endpoints.

## Estado actual del proyecto

**En desarrollo — configuración inicial completada.**

Hasta el momento se ha implementado:

- Configuración inicial del backend con Python y FastAPI.
- Entorno virtual de Python.
- Configuración de variables de entorno mediante `.env`.
- Creación de un proyecto y clúster en MongoDB Atlas.
- Conexión entre FastAPI y MongoDB Atlas.
- Endpoint para verificar el funcionamiento de la API.
- Endpoint para comprobar la conexión con MongoDB.
- Documentación automática mediante Swagger UI.
- Configuración de `.gitignore` para excluir archivos sensibles y temporales.

**Importante:** todavía no se han implementado operaciones para crear, consultar, actualizar o eliminar negocios, servicios y reservaciones.

## Estructura del proyecto

Estructura principal de referencia:

```text
reservar-cita-back/
├── app/
│   ├── config/
│   │   └── database.py
│   └── main.py
├── .venv/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

La estructura se ampliará conforme se desarrollen los módulos de negocios, servicios y reservaciones.

## Requisitos previos

Para ejecutar el proyecto localmente necesitas:

- Python 3.9 o una versión compatible con las dependencias instaladas.
- pip.
- Una cuenta de MongoDB Atlas.
- Un clúster de MongoDB configurado.
- Credenciales de acceso a la base de datos.
- Visual Studio Code u otro editor de código.

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd reservar-cita-back
```

Reemplaza `<URL_DEL_REPOSITORIO>` con la dirección de tu repositorio de GitHub.

### 2. Crear un entorno virtual

```bash
python3 -m venv .venv
```

### 3. Activar el entorno virtual

En macOS o Linux:

```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

Si el proyecto cuenta con `requirements.txt`:

```bash
pip install -r requirements.txt
```

Para generar o actualizar este archivo desde el entorno virtual configurado:

```bash
python3 -m pip freeze > requirements.txt
```

### 5. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo de configuración:

```env
MONGODB_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/
MONGODB_DB_NAME=reservaflow
```

Los nombres de las variables deben coincidir con los utilizados en `app/config/database.py`.

Reemplazar los valores de ejemplo con las credenciales y el nombre del clúster correspondiente.

**Seguridad:** nunca subir el archivo `.env` ni las credenciales de MongoDB a GitHub.

### 6. Ejecutar el servidor

Con el entorno virtual activado:

```bash
python3 -m uvicorn app.main:app --reload
```

El servidor estará disponible en:

```text
http://127.0.0.1:8000
```

El parámetro `--reload` permite reiniciar automáticamente el servidor cuando se detectan cambios en el código. Se utiliza durante el desarrollo.

## Endpoints disponibles

Actualmente se encuentran implementados dos endpoints de prueba.

### GET /api/health

Verifica que la API se encuentre funcionando correctamente.

**URL:**

```text
http://127.0.0.1:8000/api/health
```

**Respuesta esperada:**

```json
{
  "success": true,
  "message": "ReservaFlow API funcionando correctamente"
}
```

**Código HTTP:** `200 OK`

### GET /api/database/health

Comprueba que la API puede conectarse correctamente con MongoDB Atlas.

**URL:**

```text
http://127.0.0.1:8000/api/database/health
```

**Respuesta esperada:**

```json
{
  "success": true,
  "message": "MongoDB conectado correctamente"
}
```

**Código HTTP:** `200 OK`

Este endpoint permite comprobar la conectividad con la base de datos, pero no representa una prueba completa de las operaciones de lectura y escritura.

## Documentación de la API

FastAPI genera automáticamente documentación interactiva.

**Swagger UI:**

```text
http://127.0.0.1:8000/docs
```

**OpenAPI JSON:**

```text
http://127.0.0.1:8000/openapi.json
```

Desde Swagger UI es posible visualizar y probar los endpoints disponibles.

## Arquitectura prevista

ReservaFlow está diseñado para evolucionar hacia una arquitectura **multi-tenant**, donde diferentes negocios utilicen la misma plataforma y cada uno gestione sus propios servicios y reservaciones.

Ejemplo:

```text
ReservaFlow
│
├── Barbería BlackCut
│   ├── Servicios
│   └── Reservaciones
│
├── Salón de Belleza
│   ├── Servicios
│   └── Reservaciones
│
└── Estudio de Uñas
    ├── Servicios
    └── Reservaciones
```

La separación de datos entre negocios se implementará y validará durante el desarrollo de los módulos.

## Próximas funcionalidades

- [ ] Crear modelos de datos para negocios.
- [ ] Implementar endpoints de registro y consulta de negocios.
- [ ] Crear el catálogo de servicios por negocio.
- [ ] Implementar el registro de reservaciones.
- [ ] Consultar horarios disponibles.
- [ ] Evitar reservaciones duplicadas.
- [ ] Conectar el frontend desarrollado con React y TypeScript.
- [ ] Implementar autenticación y autorización para administradores.
- [ ] Incorporar pruebas automatizadas.
- [ ] Preparar el despliegue del backend.

## Seguridad

El proyecto utiliza variables de entorno para administrar información sensible.

Se deben excluir del control de versiones:

```gitignore
.venv/
__pycache__/
*.py[cod]
.env
.pytest_cache/
```

Las credenciales de MongoDB deben permanecer privadas. Para entornos de producción será necesario configurar permisos de acceso mínimos, políticas de red y mecanismos de autenticación.

## Frontend

El frontend de ReservaFlow se desarrolla en un repositorio independiente, utilizando:

- React
- TypeScript
- Vite
- Bootstrap
- SCSS
- React Router

El backend proporcionará los endpoints necesarios para integrar los formularios de reservación y las vistas de los negocios.

## Estado de las pruebas

Se ha comprobado manualmente que:

- El servidor FastAPI inicia correctamente.
- Swagger UI muestra los endpoints registrados.
- `GET /api/health` responde correctamente.
- `GET /api/database/health` devuelve `200 OK` y confirma la conexión con MongoDB Atlas.

Las pruebas de persistencia de datos y las pruebas automatizadas quedan pendientes.

---

**ReservaFlow API — Proyecto en desarrollo.**
