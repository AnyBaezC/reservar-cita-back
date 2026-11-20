
from fastapi import FastAPI

app = FastAPI(
    title="ReservaFlow API",
    description="API para gestión de negocios, servicios y reservaciones",
    version="1.0.0"
)


@app.get("/api/health")
def health_check():
    return {
        "success": True,
        "message": "ReservaFlow API funcionando correctamente"
    }
