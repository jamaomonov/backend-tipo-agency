import asyncio
from .notify import notify_telegram
from client.api.v1.order_notify.shemas import OrderNotify




async def notify_order_handler(order_notify: OrderNotify):

    text = "🛒 НОВЫЙ ЗАКАЗ С САЙТА\n\n"
    
    if len(order_notify.orders) == 1:
        text += "📦 Товар:\n"
    else:
        text += "📦 Товары в заказе:\n"
    
    for i, order in enumerate(order_notify.orders, 1):
        text += f"{i}.\n"
        if order.article:
            text += f"   Артикул: {order.article}\n"
        if order.name:
            text += f"   Название: {order.name}\n"
        if order.color:
            text += f"   Цвет: {order.color}\n"
        if order.size:
            text += f"   Размер: {order.size}\n"
        if order.price:
            text += f"   Цена: {order.price} сум\n"
        text += f"   Количество: {order.count} шт.\n\n"
    
    text += f"📦 Количество товаров: {order_notify.total_count} шт.\n"
    text += f"💰 Итого: {order_notify.total_price} сум\n\n"
    
    text += "📋 Данные клиента:\n\n"
    text += f"    Имя: {order_notify.client_name}\n"
    text += f"    Телефон: {order_notify.client_phone}\n"
    if order_notify.client_email:
        text += f"    Email: {order_notify.client_email}\n"
    if order_notify.client_address:
        text += f"    Адрес: {order_notify.client_address}\n"
    
    if order_notify.client_comment:
        text += f"    Комментарий: {order_notify.client_comment}\n"
    asyncio.create_task(notify_telegram(text))


