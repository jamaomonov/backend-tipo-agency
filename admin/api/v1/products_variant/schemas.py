from pydantic import BaseModel
from typing import Optional, List
from admin.api.v1.products.schemas import ProductRead
from admin.api.v1.products_images.schemas import ProductImageRead

class ProductVariantBase(BaseModel):
    product_id: int
    color: Optional[str] = None
    size: Optional[str] = None
    stock_quantity: Optional[int] = 0
    price: float

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariantUpdate(BaseModel):
    product_id: Optional[int] = None
    color: Optional[str] = None
    size: Optional[str] = None
    stock_quantity: Optional[int] = None
    price: Optional[float] = None

class ProductVariantRead(ProductVariantBase):
    id: int
    product: ProductRead
    images: List[ProductImageRead] = []

    class Config:
        orm_mode = True
