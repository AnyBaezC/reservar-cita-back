
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import PyMongoError

from app.config.database import database
from .models import BusinessCreate
from .service import create_business, BusinessUpdate

from .service import (
    create_business,
    get_businesses,
    get_business_by_id,
    get_business_by_slug,
    update_business,
    delete_business
)


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



@router.get("/{business_id}")
def get_business(business_id: str):
    try:
        business = get_business_by_id(database, business_id)

        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Negocio no encontrado"
            )

        return {
            "success": True,
            "message": "Negocio obtenido correctamente",
            "data": business
        }

    except HTTPException:
        raise

    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo consultar el negocio"
        )



@router.get("/slug/{slug}")
def find_business_by_slug(slug: str):
    try:
        business = get_business_by_slug(
            db=database,
            slug=slug
        )

        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Negocio no encontrado"
            )

        return {
            "success": True,
            "message": "Negocio obtenido correctamente",
            "data": business
        }

    except HTTPException:
        raise

    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo consultar el negocio"
        )


@router.patch("/{business_id}", status_code=status.HTTP_200_OK)
def edit_business(business_id: str, business: BusinessUpdate):
    try:
        result = update_business(
            db=database,
            business_id=business_id,
            business=business
        )

        if not result["success"]:
            raise HTTPException(
                status_code=result["status_code"],
                detail=result["message"]
            )

        return result

    except HTTPException:
        raise

    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo actualizar el negocio"
        )


@router.delete("/{business_id}", status_code=status.HTTP_200_OK)
def remove_business(business_id: str):
    try:
        result = delete_business(
            db=database,
            business_id=business_id
        )

        if not result["success"]:
            raise HTTPException(
                status_code=result["status_code"],
                detail=result["message"]
            )

        return result

    except HTTPException:
        raise

    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo desactivar el negocio"
        )
