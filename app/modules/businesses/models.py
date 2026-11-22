from pydantic import BaseModel, Field

class BusinessCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    slug: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=200)
    phone: str = Field(default="", max_length=10)
    isActive: bool = Field(default=True)