from fastapi import APIRouter

from .v1.snovidenie.routes import router as snovidenie_router


router = APIRouter()

router.include_router(snovidenie_router)