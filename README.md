
# ReservaFlow API

Backend de ReservaFlow, una plataforma de gestión de citas y reservaciones diseñada para negocios como barberías, salones de belleza, estéticas y estudios de uñas.

El proyecto está diseñado para evolucionar hacia una arquitectura multi-tenant, permitiendo que múltiples negocios administren sus servicios, clientes y reservaciones de manera independiente.

## Estado del proyecto

🚧 En desarrollo.

Actualmente se encuentra implementado y probado manualmente el módulo de gestión de negocios (Businesses).

## Tecnologías

- Python
- FastAPI
- Uvicorn
- MongoDB Atlas
- PyMongo
- Pydantic
- Python-dotenv
- Swagger UI
- Git y GitHub

## Arquitectura del proyecto

El backend utiliza una arquitectura modular para facilitar el mantenimiento, la escalabilidad y la incorporación de nuevas funcionalidades.

```text
reservar-cita-back/
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── modules/
│   │   ├── __init__.py
│   │   └── businesses/
│   │       ├── __init__.py
│   │       ├── models.py
│   │       ├── routes.py
│   │       └── service.py
│   ├── __init__.py
│   └── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Responsabilidades

| Archivo | Responsabilidad |
|---|---|
| main.py | Configuración principal de FastAPI y registro de rutas. |
| database.py | Configuración y conexión con MongoDB Atlas. |
| models.py | Modelos de datos y validaciones con Pydantic. |
| routes.py | Definición de endpoints y manejo de respuestas HTTP. |
| service.py | Lógica de negocio y operaciones con MongoDB. |

## Instalación y configuración

### 1. Requisitos previos

- Python 3.9 o compatible con las dependencias.
- Git.
- Cuenta de MongoDB Atlas.
- Acceso a un cluster de MongoDB.

### 2. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd reservar-cita-back
```

### 3. Crear un entorno virtual

```bash
python3 -m venv .venv
```

Activar el entorno virtual en macOS o Linux:

```bash
source .venv/bin/activate
```

En Windows:

```bash
.venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto.

```env
MONGODB_URI=mongodb+srv://<usuario>:<password>@<cluster>/
```

La base de datos utilizada actualmente es:

```text
reservaflow
```

El archivo `.env` no debe incluirse en el repositorio.

### 6. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en:

http://localhost:8000

## Documentación de la API

FastAPI genera automáticamente la documentación interactiva de los endpoints.

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI: http://localhost:8000/openapi.json

## Endpoints disponibles

### Health Check

| Método | Endpoint | Descripción |
|---|---|---|
| GET | /api/health | Verificar el funcionamiento de la API. |
| GET | /api/database/health | Verificar la conexión con MongoDB. |

### Businesses

| Método | Endpoint | Descripción |
|---|---|---|
| POST | /api/businesses | Registrar un negocio. |
| GET | /api/businesses | Consultar todos los negocios. |
| GET | /api/businesses/{business_id} | Consultar un negocio por ID. |
| GET | /api/businesses/slug/{slug} | Consultar un negocio activo por slug. |
| PATCH | /api/businesses/{business_id} | Actualizar parcialmente un negocio. |
| DELETE | /api/businesses/{business_id} | Desactivar un negocio. |

## Módulo de negocios (Businesses)

Permite administrar el registro, consulta, actualización, desactivación y reactivación de negocios.

### Colección de MongoDB

```text
businesses
```

### Modelo de datos

| Campo | Tipo | Descripción |
|---|---|---|
| _id | ObjectId | Identificador único generado por MongoDB. |
| name | String | Nombre del negocio. |
| slug | String | Identificador único utilizado en URLs. |
| description | String | Descripción del negocio. |
| phone | String | Teléfono de contacto. |
| isActive | Boolean | Estado del negocio. |

El campo `_id` se transforma en `id` de tipo String en las respuestas de la API.

### Registrar un negocio

POST `/api/businesses`

Request body:

```json
{
    "name": "Barbería BlackCut",
    "slug": "barberia-blackcut",
    "description": "Barbería especializada en cortes de cabello",
    "phone": "5512345678",
    "isActive": true
}
```

Respuesta esperada: `201 Created`.

```json
{
    "success": true,
    "message": "Negocio creado correctamente",
    "data": {
        "id": "ID_DEL_NEGOCIO",
        "name": "Barbería BlackCut",
        "slug": "barberia-blackcut",
        "description": "Barbería especializada en cortes de cabello",
        "phone": "5512345678",
        "isActive": true
    }
}
```

### Consultar negocios

GET `/api/businesses`

Devuelve todos los negocios registrados, incluyendo negocios activos e inactivos.

### Consultar negocio por ID

GET `/api/businesses/{business_id}`

Devuelve la información del negocio asociado al identificador proporcionado.

### Consultar negocio por slug

GET `/api/businesses/slug/barberia-blackcut`

Devuelve únicamente negocios activos.

Este endpoint está diseñado para consultar la información pública de cada negocio.

### Actualizar un negocio

PATCH `/api/businesses/{business_id}`

Permite actualizar únicamente los campos enviados en la solicitud.

Request body:

```json
{
    "name": "Barbería BlackCut Premium",
    "phone": "5598765432"
}
```

Los campos que no se incluyen en la solicitud conservan sus valores originales.

Respuesta esperada: `200 OK`.

### Desactivar un negocio

DELETE `/api/businesses/{business_id}`

El sistema utiliza eliminación lógica para conservar la información del negocio y permitir mantener sus futuras relaciones con servicios y reservaciones.

En lugar de eliminar físicamente el documento, se actualiza su estado:

```json
{
    "isActive": false
}
```

Características:

- El documento permanece almacenado en MongoDB.
- El negocio deja de estar disponible mediante la consulta por slug.
- Puede seguir consultándose por ID.
- Desactivar nuevamente un negocio inactivo devuelve una respuesta exitosa.
- El negocio puede reactivarse posteriormente.

### Reactivar un negocio

PATCH `/api/businesses/{business_id}`

```json
{
    "isActive": true
}
```

Una vez reactivado, el negocio vuelve a estar disponible mediante su slug.

## Validaciones

### Nombre del negocio

- Mínimo de 2 caracteres.
- Máximo de 100 caracteres.

### Slug

- Mínimo de 3 caracteres.
- Máximo de 100 caracteres.
- Únicamente letras minúsculas, números y guiones como separadores.
- No permite espacios.
- Debe ser único.

Ejemplos válidos:

```text
barberia-blackcut
studio-nails
estetica-2026
```

Ejemplos inválidos:

```text
Barberia BlackCut
barberia_blackcut
barberia--blackcut
```

La unicidad del slug se garantiza mediante un índice único en MongoDB.

### Identificadores

- Validación del formato ObjectId.
- Validación de existencia del negocio.

### Actualizaciones

- No se permiten objetos JSON vacíos.
- No se permiten valores nulos explícitos.
- Se validan los campos proporcionados.
- No se permite utilizar el slug de otro negocio.

## Manejo de respuestas HTTP

| Código | Descripción |
|---|---|
| 200 | Operación realizada correctamente. |
| 201 | Recurso creado correctamente. |
| 400 | Solicitud incorrecta o ID inválido en PATCH y DELETE. |
| 404 | Negocio no encontrado o no disponible. |
| 409 | Conflicto por slug duplicado. |
| 422 | Error de validación de datos. |
| 503 | Error de conexión u operación con la base de datos. |

Ejemplo de respuesta de error:

```json
{
    "detail": "Negocio no encontrado"
}
```

## Arquitectura multi-tenant

ReservaFlow está diseñado para soportar múltiples negocios dentro de una misma plataforma.

Cada negocio tendrá sus propios:

- Servicios.
- Clientes.
- Reservaciones.
- Horarios.
- Configuraciones.
- Usuarios administrativos.

Las futuras colecciones estarán relacionadas mediante el identificador `businessId`.

```text
ReservaFlow
│
├── Negocio A
│   ├── Servicios
│   ├── Clientes
│   └── Reservaciones
│
└── Negocio B
    ├── Servicios
    ├── Clientes
    └── Reservaciones
```

El módulo Businesses representa la base de esta arquitectura.

La autenticación, autorización y el aislamiento efectivo de datos entre negocios se encuentran pendientes de implementación.

## Pruebas

Las pruebas actuales se realizaron manualmente mediante Swagger UI y MongoDB Compass.

### Businesses

- [x] Registro de negocios.
- [x] Consulta general de negocios.
- [x] Consulta por ID.
- [x] Consulta por slug.
- [x] Validación de slug duplicado.
- [x] Validación de formato de slug.
- [x] Actualización parcial de información.
- [x] Validación de solicitudes vacías.
- [x] Validación de valores nulos.
- [x] Validación de identificadores incorrectos.
- [x] Validación de negocios inexistentes.
- [x] Eliminación lógica.
- [x] Desactivación de negocios previamente inactivos.
- [x] Restricción de consulta pública de negocios inactivos.
- [x] Reactivación de negocios.
- [x] Verificación de persistencia en MongoDB.
- [ ] Pruebas unitarias automatizadas.
- [ ] Pruebas de integración automatizadas.

## Roadmap

### Fase 1 - Configuración inicial

- [x] Creación del proyecto backend.
- [x] Configuración de FastAPI.
- [x] Configuración de MongoDB Atlas.
- [x] Variables de entorno.
- [x] Arquitectura modular.
- [x] Health checks.
- [x] Documentación inicial.

### Fase 2 - Gestión de negocios

- [x] Modelo de negocios.
- [x] Registro de negocios.
- [x] Consulta de negocios.
- [x] Consulta por ID.
- [x] Consulta por slug.
- [x] Actualización de negocios.
- [x] Eliminación lógica.
- [x] Reactivación.
- [x] Validaciones y manejo de errores.
- [x] Pruebas manuales.

### Fase 3 - Gestión de servicios

- [ ] Modelo de servicios.
- [ ] Relación entre negocios y servicios.
- [ ] Registro de servicios.
- [ ] Consulta de servicios por negocio.
- [ ] Actualización de servicios.
- [ ] Desactivación de servicios.
- [ ] Validación de precios y duración.

### Fase 4 - Gestión de reservaciones

- [ ] Modelo de reservaciones.
- [ ] Registro de clientes.
- [ ] Creación de reservaciones.
- [ ] Disponibilidad de horarios.
- [ ] Validación de horarios ocupados.
- [ ] Cancelación de reservaciones.
- [ ] Historial de reservaciones.

### Fase 5 - Seguridad

- [ ] Registro de usuarios.
- [ ] Inicio de sesión.
- [ ] Autenticación mediante JWT.
- [ ] Roles y permisos.
- [ ] Protección de endpoints.
- [ ] Aislamiento de datos entre negocios.

### Fase 6 - Integración y despliegue

- [ ] Configuración de CORS.
- [ ] Integración con el frontend de ReservaFlow.
- [ ] Pruebas automatizadas.
- [ ] Configuración de CI/CD.
- [ ] Despliegue del backend.
- [ ] Monitoreo y registro de errores.

## Seguridad

- Las credenciales se almacenan en variables de entorno.
- El archivo `.env` está excluido del control de versiones.
- No se deben almacenar contraseñas ni credenciales en el código fuente.
- Los datos de entrada se validan mediante Pydantic.
- La eliminación lógica permite conservar la información registrada.
- Los endpoints administrativos todavía no cuentan con autenticación ni autorización.
- La API se encuentra en desarrollo y no está preparada para producción.

## Control de versiones

El proyecto utiliza Git y GitHub para administrar el código fuente.

Convenciones de commits propuestas:

| Prefijo | Descripción |
|---|---|
| feat | Nueva funcionalidad. |
| fix | Corrección de errores. |
| docs | Cambios en documentación. |
| refactor | Reestructuración del código. |
| test | Incorporación o modificación de pruebas. |
| chore | Configuración y mantenimiento. |

## Proyecto

ReservaFlow es una plataforma independiente orientada a digitalizar la administración de citas y reservaciones para pequeños y medianos negocios.

---

**ReservaFlow API | En desarrollo**
