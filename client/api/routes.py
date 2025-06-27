from fastapi import APIRouter

from .v1.snovidenie.routes import router as snovidenie_router
from .v1.order_notify.routes import router as order_notify_router

router = APIRouter()

router.include_router(snovidenie_router)
router.include_router(order_notify_router)