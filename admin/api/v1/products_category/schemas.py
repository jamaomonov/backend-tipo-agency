from pydantic import BaseModel
from typing import Optional

class ProductCategoryBase(BaseModel):
    name: str

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategoryUpdate(BaseModel):
    name: Optional[str] = None

class ProductCategoryRead(ProductCategoryBase):
    id: int
    slug: str

    class Config:
        orm_mode = True
