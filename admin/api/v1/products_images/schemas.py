from pydantic import BaseModel
from typing import Optional

class ProductImageBase(BaseModel):
    variant_id: int
    url: str
    is_main: bool

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageUpdate(BaseModel):
    url: Optional[str] = None
    is_main: Optional[bool] = None

class ProductImageRead(ProductImageBase):
    id: int

    class Config:
        orm_mode = True
