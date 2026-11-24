from pydantic import BaseModel, Field
from typing import Optional

class BusinessCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    slug: str = Field(
    min_length=3,
    max_length=100,
    pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
)
    description: str = Field(default="", max_length=200)
    phone: str = Field(default="", max_length=10)
    isActive: bool = Field(default=True)


class BusinessUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    slug: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
    )

    description: Optional[str] = None
    phone: Optional[str] = None
    isActive: Optional[bool] = None
