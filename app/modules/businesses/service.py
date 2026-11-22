
from pymongo.errors import DuplicateKeyError
from .models import BusinessCreate


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
