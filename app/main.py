
from fastapi import FastAPI, HTTPException
from app.config.database import test_connection
from app.modules.businesses.routes import router as businesses_router

app = FastAPI(
    title="ReservaFlow API",
    description="API para gestión de negocios, servicios y reservaciones",
    version="1.0.0"
)

app.include_router(businesses_router)

@app.get("/api/database/health")
def database_health():
    try:
        test_connection()

        return {
            "success": True,
            "message": "MongoDB conectado correctamente"
        }

    except Exception as error:
        print(f"Error de conexión MongoDB: {error}")

        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con MongoDB"
        )


@app.get("/api/health")
def health_check():
    return {
        "success": True,
        "message": "ReservaFlow API funcionando correctamente"
    }
