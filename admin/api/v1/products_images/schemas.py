from pydantic import BaseModel
from typing import Optional

class ProductImageBase(BaseModel):
    variant_id: int
    url: str

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageUpdate(BaseModel):
    # Обновление только файла, variant_id не меняется
    pass

class ProductImageRead(ProductImageBase):
    id: int

    class Config:
        orm_mode = True
