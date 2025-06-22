from pydantic import BaseModel
from typing import Optional
from admin.api.v1.products_category.schemas import ProductCategoryRead

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    is_active: Optional[bool] = True
    is_new: Optional[bool] = False
    is_discounted: Optional[bool] = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_new: Optional[bool] = None
    is_discounted: Optional[bool] = None

class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    slug: str
    is_active: Optional[bool] = True
    is_new: Optional[bool] = False
    is_discounted: Optional[bool] = False
    category: ProductCategoryRead

    class Config:
        orm_mode = True
