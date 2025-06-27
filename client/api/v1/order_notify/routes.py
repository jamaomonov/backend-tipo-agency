from fastapi import APIRouter
from .shemas import OrderNotify
from services.telegram.handlers import notify_order_handler

router = APIRouter(tags=["Order Notify"])

@router.post("/order_notify")
async def order_notify(order_notify: OrderNotify):
    await notify_order_handler(order_notify)
    return {"message": "Order notified"}