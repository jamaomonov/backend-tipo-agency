from pydantic import BaseModel
from typing import Optional

class Order(BaseModel):
    article: str
    name: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    price: Optional[float] = None
    count: int

class OrderNotify(BaseModel):
    orders: list[Order]
    total_count: int
    total_price: float
    client_name: str
    client_phone: str
    client_email: Optional[str] = None
    client_address: Optional[str] = None
    client_comment: Optional[str] = None
    