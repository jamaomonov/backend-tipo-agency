from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal


class ProductImageRead(BaseModel):
    id: int
    url: str
    is_main: bool

    class Config:
        from_attributes = True


class ProductVariantRead(BaseModel):
    id: int
    color: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    stock_quantity: int
    price: Decimal
    images: List[ProductImageRead] = []

    class Config:
        from_attributes = True


class ProductCategoryRead(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True


class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    slug: str
    is_active: bool
    is_new: bool
    is_discounted: bool
    category: ProductCategoryRead
    variants: List[ProductVariantRead] = []

    class Config:
        from_attributes = True


class ProductsResponse(BaseModel):
    products: List[ProductRead]
    total: int


class CategoriesResponse(BaseModel):
    categories: List[ProductCategoryRead]
