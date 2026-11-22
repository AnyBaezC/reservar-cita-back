
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import PyMongoError

from app.config.database import database
from .models import BusinessCreate
from .service import create_business
from .service import create_business, get_businesses

router = APIRouter(
    prefix="/api/businesses",
    tags=["Businesses"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def register_business(business: BusinessCreate):
    try:
        result = create_business(db=database, business=business)

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=result["message"]
            )

        return result

    except HTTPException:
        raise

    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo guardar el negocio"
        )


@router.get("")
def list_businesses():
    try:
        return get_businesses(database)

    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudieron consultar los negocios"
        )
