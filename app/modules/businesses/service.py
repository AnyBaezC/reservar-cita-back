
from pymongo.errors import DuplicateKeyError
from .models import BusinessCreate, BusinessUpdate
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument


def create_business(db, business: BusinessCreate):
    collection = db["businesses"]

    collection.create_index("slug", unique=True)

    business_data = business.model_dump()

    try:
        result = collection.insert_one(business_data)

    except DuplicateKeyError:
        return {
            "success": False,
            "message": "Ya existe un negocio con el mismo slug"
        }

    return {
        "success": True,
        "message": "Negocio creado correctamente",
        "data": {
            "id": str(result.inserted_id),
            "name": business_data["name"],
            "slug": business_data["slug"],
            "description": business_data["description"],
            "phone": business_data["phone"],
            "isActive": business_data["isActive"]
        }
    }


def get_businesses(db):
    collection = db["businesses"]

    businesses = []

    for business in collection.find():
        business["id"] = str(business.pop("_id"))
        businesses.append(business)

    return {
        "success": True,
        "message": "Negocios obtenidos correctamente",
        "data": businesses
    }


def get_business_by_id(db, business_id: str):
    collection = db["businesses"]

    try:
        object_id = ObjectId(business_id)
    except InvalidId:
        return None

    business = collection.find_one({"_id": object_id})

    if not business:
        return None

    business["id"] = str(business.pop("_id"))

    return business


def get_business_by_slug(db, slug: str):
    collection = db["businesses"]

    business = collection.find_one({
        "slug": slug,
        "isActive": True
    })

    if not business:
        return None

    business["id"] = str(business.pop("_id"))

    return business


def update_business(db, business_id: str, business: BusinessUpdate):
    collection = db["businesses"]

    # Validar el identificador del negocio
    try:
        object_id = ObjectId(business_id)
    except InvalidId:
        return {
            "success": False,
            "message": "Identificador de negocio inválido",
            "status_code": 400
        }

    # Obtener únicamente los campos enviados
    update_data = business.model_dump(exclude_unset=True)

    # Validar que existan campos para actualizar
    if not update_data:
        return {
            "success": False,
            "message": "No se enviaron datos para actualizar",
            "status_code": 400
        }

    # Evitar valores nulos
    if any(value is None for value in update_data.values()):
        return {
            "success": False,
            "message": "Los campos no pueden contener valores nulos",
            "status_code": 400
        }

    try:
        updated_business = collection.find_one_and_update(
            {"_id": object_id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )

    except DuplicateKeyError:
        return {
            "success": False,
            "message": "Ya existe un negocio con el mismo slug",
            "status_code": 409
        }

    # Validar que el negocio exista
    if updated_business is None:
        return {
            "success": False,
            "message": "Negocio no encontrado",
            "status_code": 404
        }

    # Convertir ObjectId a string
    updated_business["id"] = str(updated_business.pop("_id"))

    return {
        "success": True,
        "message": "Negocio actualizado correctamente",
        "data": updated_business
    }


def delete_business(db, business_id: str):
    collection = db["businesses"]

    # Validar el identificador del negocio
    try:
        object_id = ObjectId(business_id)

    except InvalidId:
        return {
            "success": False,
            "message": "Identificador de negocio inválido",
            "status_code": 400
        }

    # Realizar eliminación lógica
    business = collection.find_one_and_update(
        {"_id": object_id},
        {"$set": {"isActive": False}},
        return_document=ReturnDocument.AFTER
    )

    # Validar que el negocio exista
    if business is None:
        return {
            "success": False,
            "message": "Negocio no encontrado",
            "status_code": 404
        }

    # Convertir ObjectId a string
    business["id"] = str(business.pop("_id"))

    return {
        "success": True,
        "message": "Negocio desactivado correctamente",
        "data": business
    }
